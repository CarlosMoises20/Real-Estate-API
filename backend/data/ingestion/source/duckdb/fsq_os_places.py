
import pandas as pd
from backend.data.ingestion.source.duckdb.base_duckdb_data_source import BaseDuckDBDataSource      # Access FSQ OS Places data using DuckDB SQL queries; see https://duckdb.org/docs/current/sql/introduction for more details
from backend.common.utils import *
import os, duckdb                                                                                        # If you want to generate the dataset with data in raw format (JSON for visualization)

"""This class is used to retrieve relevant data from Foursquare OS Places"""
class FSQOSPlaces(BaseDuckDBDataSource):
    
    """Constructor for the FSQOSPlaces class"""
    def __init__(self, access_token, country_code, db_file_path, places_dataset_path, datasets_format=None):
        
        super().__init__(datasets_format=datasets_format, 
                         connection=duckdb.connect(db_file_path))
        
        self.__access_token = access_token
        self.__country_code = country_code
        self.__places_dataset_path = places_dataset_path
        
        self._initial_setup()                         # Setup the environment before fetching data from Foursquare OS Places
    
        
    """
    Setup the environment before fetching data from 
    Foursquare OS Places API, using the DuckDB connection
    
    """    
    def _initial_setup(self):
        
        self._connection.execute("INSTALL iceberg; LOAD iceberg;")      # Install and load the iceberg extension
        
        self._connection.execute("LOAD httpfs;")                        # Load the httpfs extension to enable HTTP access to files in DuckDB
        
        # Create a secret for FSQ OS Places using the Iceberg extension and the temporary access token from the .env file 
        self._connection.execute(f"""CREATE OR REPLACE SECRET fsq_secret(
            TYPE iceberg,
            TOKEN '{self.__access_token}'
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
        
        
    """Retrieve JSON data from Foursquare OS Places and return dataframe with relevant data"""
    def get_source_data(self):
        
        datasets_format = self._datasets_format if self._datasets_format else "parquet"
        
        dataset_full_path = f"{self.__places_dataset_path}/fsq_{self.__country_code.lower()}_places.{datasets_format}"
        
        # verify local .parquet dataset with places from FSQ OS Places
        if not os.path.exists(dataset_full_path):
            
            query = f"""
                        COPY (SELECT p.fsq_place_id, p.name, p.latitude, p.longitude, p.address,
                                p.country, p.locality, p.region, p.postcode, p.date_created,
                                p.date_refreshed, p.date_closed, p.fsq_category_ids, p.fsq_category_labels,
                                p.bbox
                            FROM fsq.datasets.places_os AS p
                            WHERE p.country = '{self.__country_code}') 
                            TO '{dataset_full_path}'
                    """
        
            # even if the user does not define self._datasets_format, the dataset will always be created (by default, in parquet format),
            # to increase the solution's efficiency on data processing        
            formatter = "WITH CSV DELIMITER ','" if datasets_format == "csv" else "(FORMAT PARQUET)"
            
            self._connection.sql(f"{query} {formatter};")
        
        # TODO if possible, implement logic to update local dataset when remote dataset is updated
        
        # Read and return the dataset
        return pd.read_parquet(dataset_full_path) if datasets_format == "parquet" else pd.read_csv(dataset_full_path)
        
    