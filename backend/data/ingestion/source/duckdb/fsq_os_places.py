
from backend.data.ingestion.source.duckdb.base_duckdb_data_source import BaseDuckDBDataSource      # Access FSQ OS Places data using DuckDB SQL queries; see https://duckdb.org/docs/current/sql/introduction for more details
from backend.common.utils import *
from backend.common.dataset_names import get_fsq_places_dataset_name
import os                                                                                        # If you want to generate the dataset with data in raw format (JSON for visualization)

"""This class is used to retrieve relevant data from Foursquare OS Places"""
class FSQOSPlaces(BaseDuckDBDataSource):
    
    """Constructor for the FSQOSPlaces class"""
    def __init__(self, datasets_format, datasets_path):

        super().__init__(datasets_format=datasets_format, 
                         datasets_path=datasets_path,
                         connection=super()._create_connection_from_db_file(
                             "./backend/data/duckdb_source/fsq/fsq_os_places.db"
                        ))
        
        # Setup the environment before fetching data from Foursquare OS Places
        self._initial_setup()                         
    
        
    """
    Setup the environment before fetching data from 
    Foursquare OS Places API, using the DuckDB connection
    
    """    
    def _initial_setup(self):
        
        self._connection.execute("INSTALL iceberg; LOAD iceberg;")      # Install and load the iceberg extension
        
        self._connection.execute("INSTALL spatial; LOAD spatial;")      # Install and load the spatial extension; Spatial Joins are used to combine data based on location
        
        self._connection.execute("LOAD httpfs;")                        # Load the httpfs extension to enable HTTP access to files in DuckDB
        
        # Create a secret for FSQ OS Places using the Iceberg extension and the temporary access token from the .env file 
        self._connection.execute(f"""CREATE OR REPLACE SECRET fsq_secret(
            TYPE iceberg,
            TOKEN '{os.getenv("FSQ_OS_PLACES_ACCESS_TOKEN")}'
        );""")
        
        try:
            # Attach the Huggingface dataset
            self._connection.execute("""ATTACH 'places' AS fsq(
                    TYPE iceberg,
                    SECRET fsq_secret,
                    ENDPOINT 'https://catalog.h3-hub.foursquare.com/iceberg'
            );""")
            
        except:
            print("Failed to connect to FSQ OS Places API. Please check your access token from your .env file and try again.")  
            raise

        
    """
    This method is used to update the dataset with data from Foursquare OS Places
    We can call this method in separate whenever we know that the API data has been updated, hence
    we need to update the local dataset to apply the latest changes
    
    """    
    def get_source_data(self, country_code):
        
        dataset_full_path = f"{self._datasets_path}/{get_fsq_places_dataset_name(country_code)}.{self._datasets_format}"
        
        # Create the directory where the dataset will be created if it does not exist
        os.makedirs(self._datasets_path, exist_ok=True)
        
        query = f"""
            COPY (SELECT p.fsq_place_id, p.name, p.latitude, p.longitude,
                    p.date_created, p.date_closed,
                    array_to_string(p.fsq_category_labels, '|') AS fsq_category_labels
                FROM fsq.datasets.places_os AS p
                WHERE p.country = '{country_code}' AND p.latitude IS NOT NULL)
                TO '{dataset_full_path}'
        """

        # even if the user does not manually define datasets_format, the dataset will always be created (by default, in parquet format),
        # to increase the solution's efficiency on data processing        
        formatter = "WITH CSV DELIMITER ','" if self._datasets_format == "csv" else "(FORMAT PARQUET)"
        
        self._connection.sql(f"{query} {formatter};")
    
        
    