import io, os, zipfile, requests
import pandas as pd
from backend.data.ingestion.source.duckdb.base_duckdb_data_source import BaseDuckDBDataSource
from backend.common.utils import generate_dataset_from_df
from backend.common.dataset_names import get_caop_dataset_name


"""
This class is used to retrieve the parish (freguesia) boundaries of Portugal from the CAOP
(Carta Administrativa Oficial de Portugal), published by DGT (Direção-Geral do Território)

The GeoPackage files are kept in 'geopackages_path' (git-ignored), because the parish polygons
are needed to assign points (e.g. FSQ places) to parishes with DuckDB spatial queries;
the parishes table without geometry (code, names and area) is saved as a regular dataset

"""
class CAOP(BaseDuckDBDataSource):

    # Download URL of each region's GeoPackage; {year} is replaced by the CAOP version
    URL_TEMPLATE = "https://geo2.dgterritorio.gov.pt/caop/CAOP_{region}_{year}-gpkg.zip"

    # (region in the URL, GeoPackage file, parishes layer, CRS of the layer)
    # The Azores have two files because the western group uses a different UTM zone
    LAYERS = [
        ("Continente", "Continente_CAOP{year}.gpkg", "cont_freguesias", "EPSG:3763"),
        ("RAM", "ArqMadeira_CAOP{year}.gpkg", "ram_freguesias", "EPSG:5016"),
        ("RAA", "ArqAcores_GCentral_GOriental_CAOP{year}.gpkg", "raa_cen_ori_freguesias", "EPSG:5015"),
        ("RAA", "ArqAcores_GOcidental_CAOP{year}.gpkg", "raa_oci_freguesias", "EPSG:5014")
    ]


    """
    Constructor for the CAOP class

        year: version of the CAOP; CAOP 2024 is used by default because the listings use the parishes
              defined in 2013, and CAOP 2025 already includes the parish de-aggregation of 2025
        geopackages_path: directory where the GeoPackage files are stored

    """
    def __init__(self, datasets_format, datasets_path, year=2024,
                 geopackages_path="./backend/data/duckdb_source/caop"):

        super().__init__(datasets_format=datasets_format,
                         datasets_path=datasets_path)

        self._year = year
        self._geopackages_path = geopackages_path

        self._initial_setup()


    """Version (year) of the CAOP"""
    @property
    def year(self):
        return self._year


    """Load the DuckDB spatial extension, used to read the GeoPackage files and to run spatial queries"""
    def _initial_setup(self):
        self._connection.execute("INSTALL spatial; LOAD spatial;")


    """Build the SQL query that reads the parishes of every region, with the geometry converted to WGS84 (longitude, latitude)"""
    def _parishes_query(self):

        return " UNION ALL ".join(f"""
            SELECT dtmnfr AS dicofre,
                   designacao_simplificada AS parish,
                   municipio AS municipality,
                   distrito_ilha AS district_island,
                   nuts2,
                   area_ha / 100 AS area_km2,
                   ST_Transform(geom, '{crs}', 'EPSG:4326', always_xy := true) AS geom
            FROM ST_Read('{self._geopackages_path}/{file.format(year=self._year)}', layer='{layer}')
        """ for _, file, layer, crs in self.LAYERS)


    """
    Download the GeoPackage files of every region (mainland, Madeira and Azores) and save
    the parishes table (without geometry) as a dataset

    """
    def get_source_data(self):

        os.makedirs(self._geopackages_path, exist_ok=True)

        for region in dict.fromkeys(region for region, *_ in self.LAYERS):

            response = requests.get(self.URL_TEMPLATE.format(region=region, year=self._year), timeout=(10, 300))
            response.raise_for_status()

            # Extract only the GeoPackage files from the ZIP archive
            with zipfile.ZipFile(io.BytesIO(response.content)) as archive:
                for name in archive.namelist():
                    if name.endswith(".gpkg"):
                        with open(os.path.join(self._geopackages_path, os.path.basename(name)), "wb") as f:
                            f.write(archive.read(name))

        df_parishes = self._connection.sql(f"SELECT * EXCLUDE (geom) FROM ({self._parishes_query()})").df()

        generate_dataset_from_df(df=df_parishes,
                                 file_path_base=f"{self._datasets_path}/{get_caop_dataset_name(self._year)}",
                                 dataset_format=self._datasets_format)


    """
    Assign each point of a dataframe to the parish (freguesia) that contains it, using the CAOP polygons
    Returns a copy of the dataframe with a new column "dicofre" (NaN for points outside every parish, e.g. at sea)

        df: Pandas dataframe with the points
        lat_col, lon_col: names of the latitude and longitude columns (WGS84)

    """
    def assign_parishes(self, df, lat_col="latitude", lon_col="longitude"):

        df_points = df.reset_index(drop=True).copy()
        df_points["_pos"] = range(len(df_points))

        self._connection.register("df_points", df_points[["_pos", lat_col, lon_col]])

        df_assigned = self._connection.sql(f"""
            SELECT p._pos, f.dicofre
            FROM df_points AS p
            JOIN ({self._parishes_query()}) AS f
              ON ST_Contains(f.geom, ST_Point(p.{lon_col}, p.{lat_col}))
            WHERE p.{lat_col} IS NOT NULL AND p.{lon_col} IS NOT NULL
        """).df()

        self._connection.unregister("df_points")

        df_points["dicofre"] = df_points["_pos"].map(df_assigned.drop_duplicates("_pos").set_index("_pos")["dicofre"])

        return df_points.drop(columns=["_pos"])
