
import pandas as pd
import os
from datetime import datetime, timezone
from backend.data.ingestion.source.duckdb.base_duckdb_data_source import BaseDuckDBDataSource      # Access FSQ OS Places data using DuckDB SQL queries; see https://duckdb.org/docs/current/sql/introduction for more details
from backend.common.utils import *
import json        # If you want to generate the dataset with data in raw format (JSON for visualization)
from backend.common.constants import PORTUGAL_COORDINATES_LIST

"""This class is used to retrieve relevant data from Foursquare OS Places"""
# TODO review this (some of these methods) and finish implementation
class FSQOSPlaces(BaseDuckDBDataSource):
    
    """Constructor for the FSQOSPlaces class"""
    def __init__(self, hf_token, datasets_format=None, connection=None):
        super().__init__(datasets_format=datasets_format, connection=connection)
        self.__hf_token = hf_token
        self.__cache_dir = "./backend/datasets/external/cache/fsq_os_places"        # Directory to store the cache of the Foursquare OS Places data
        self.__cache_metadata_file = os.path.join(self.__cache_dir, "metadata.json")
        self.__cache_data_file = os.path.join(self.__cache_dir, "pt_places.parquet")
        self._initial_setup()               # Setup the environment before fetching data from Foursquare OS Places API
    
    
    def __read_cache_metadata(self):
        if not os.path.exists(self.__cache_metadata_file):
            return None
        with open(self.__cache_metadata_file, "r") as f:
            return json.load(f)
        
        
    def __write_cache_metadata(self, release_date):
        os.makedirs(self.__cache_dir, exist_ok=True)
        with open(self.__cache_metadata_file, "w") as f:
            json.dump({
                "release_date": release_date,
                "cached_at": datetime.now(timezone.utc).isoformat(),
            }, f, indent=2)
        
        
    """Setup the environment before fetching data from 
    Foursquare OS Places API, using the DuckDB connection"""    
    def _initial_setup(self):
        
        self._connection.execute("INSTALL httpfs; LOAD httpfs;")        # Install and load the httpfs extension to enable HTTP access to files in DuckDB
        
        self._connection.execute("INSTALL httpfs; LOAD httpfs;")        # Install and load the httpfs extension to enable HTTP access to files in DuckDB
        
        self._connection.execute("SET s3_region='us-east-1';")
        
        self._connection.execute("SET s3_url_style='path';")
        
        self._connection.execute("SET http_retries=5;")

        self._connection.execute("SET http_retry_wait_ms=2000;")

        self._connection.execute("SET http_timeout=120000;")
        
        self._connection.execute(f"""CREATE SECRET hf_token(
            TYPE huggingface,
            TOKEN '{self.__hf_token}'
        )""")
        
        super()._execute_query_with_retries("""
            CREATE VIEW places AS
            SELECT * FROM read_parquet('hf://datasets/foursquare/fsq-os-places/release/dt=*/places/parquet/*.parquet')
        """)
        
        super()._execute_query_with_retries("""
            CREATE VIEW categories AS
            SELECT * FROM read_parquet('hf://datasets/foursquare/fsq-os-places/release/dt=*/categories/parquet/*.parquet')
        """)
        
    
    """Build the SQL query to fetch data from Foursquare OS Places API"""
    def _build_fetch_query(self, min_lat, min_lon, max_lat, max_lon, country):
        return f"""
            WITH places_exploded_categories AS (
                -- Unnest categories array using UNNEST with ordinality
                SELECT fsq_place_id,
                    UNNEST(fsq_category_ids) as fsq_category_id
                FROM places
            ),
            distinct_places AS (
                SELECT 
                DISTINCT(fsq_place_id)
                FROM places_exploded_categories p
                JOIN categories c
                ON p.fsq_category_id = c.category_id 
                WHERE c.level2_category_id = '4d4b7105d754a06374d81259'
            )
            SELECT * FROM places
            WHERE fsq_place_id IN (SELECT fsq_place_id FROM distinct_places)
            AND latitude BETWEEN {min_lat} AND {max_lat}
            AND longitude BETWEEN {min_lon} AND {max_lon}
            AND country = '{country}'
        """
        
        
    def __get_latest_release_date(self):
        result = self._connection.execute("""
            SELECT regexp_extract(file, 'dt=([0-9-]+)', 1) AS dt
            FROM glob('s3://fsq-os-places-us-east-1/release/*/places/parquet/*.parquet')
            ORDER BY dt DESC
            LIMIT 1
        """).fetchone()
        if not result:
            raise RuntimeError("Não foi possível encontrar nenhum release do FSQ OS Places no S3.")
        return result[0]
        
        
    """Retrieve JSON data from Foursquare OS Places and return dataframe with relevant data"""
    def get_source_data(self):
        
        latest_release_date = self.__get_latest_release_date()
        
        cache_metadata = self.__read_cache_metadata()
        
        df_list = []
        
        for coordinates in PORTUGAL_COORDINATES_LIST:
                    
            region_name = list(coordinates.keys())[0] 
            
            coords = coordinates[region_name]
            
            df_region = self._fetch(
                min_lat=coords["min_lat"], 
                min_lon=coords["min_lon"], 
                max_lat=coords["max_lat"], 
                max_lon=coords["max_lon"],
                country="PT"
            )
            
            df_region["region"] = region_name
            
            df_list.append(df_region)
        
        df = pd.concat(df_list, ignore_index=True)
        
        # NOTE uncomment if you want to generate the dataset with data in raw format, for visualization
        with open(f"./backend/datasets/external/fsq_os_places_data_v0_facilities.json", "w") as f:
            f.write(df.to_json(orient="records", indent=2))
            
        self.__write_cache_metadata(latest_release_date)
        
        """# Save final dataset (NOTE: optional)            
        generate_dataset_from_df(df=df, 
                                file_path_base=f"./backend/datasets/external/fsq_os_places_data_facilities",
                                dataset_format=self._datasets_format)"""
        
        return df
        
    