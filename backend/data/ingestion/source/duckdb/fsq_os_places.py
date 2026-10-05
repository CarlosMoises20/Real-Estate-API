
import pandas as pd
from backend.data.ingestion.source.duckdb.base_duckdb_data_source import BaseDuckDBDataSource      # Access FSQ OS Places data using DuckDB SQL queries; see https://duckdb.org/docs/current/sql/introduction for more details
from backend.common.utils import *
import os                                                                                        # If you want to generate the dataset with data in raw format (JSON for visualization)

"""This class is used to retrieve relevant data from Foursquare OS Places"""
class FSQOSPlaces(BaseDuckDBDataSource):
    
    """Constructor for the FSQOSPlaces class"""
    def __init__(self, access_token, db_file_path, datasets_format, datasets_path):

        super().__init__(datasets_format=datasets_format, 
                         datasets_path=datasets_path,
                         connection=super()._create_connection_from_db_file(db_file_path) if db_file_path else None)
        
        self.__access_token = access_token
        
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
        
    """
    This method is used to update the dataset with data from Foursquare OS Places
    We can call this method in separate whenever we know that the API data has been updated, hence
    we need to update the local dataset to apply the latest changes
    
    """    
    def update_data(self, country_code):
        
        dataset_full_path = f"{self._datasets_path}/fsq_{country_code.lower()}_places.{self._datasets_format}"
        
        query = f"""
                    COPY (SELECT p.name, p.latitude, p.longitude, p.address,
                            p.country, p.date_created, p.fsq_category_labels
                        FROM fsq.datasets.places_os AS p
                        WHERE p.country = '{country_code}') 
                        TO '{dataset_full_path}'
                """

        # even if the user does not manually define datasets_format, the dataset will always be created (by default, in parquet format),
        # to increase the solution's efficiency on data processing        
        formatter = "WITH CSV DELIMITER ','" if self._datasets_format == "csv" else "(FORMAT PARQUET)"
        
        self._connection.sql(f"{query} {formatter};")
        
        
    """
    Retrieve JSON data from Foursquare OS Places and return dataframe with relevant data
    Instead of always calling the API to retrieve data, we can call this method to retrieve the local data
    for faster processing ("cache" method), calling the API only when there is no local dataset
    
    """
    def get_source_data(self, country_code):
        
        dataset_full_path = f"{self._datasets_path}/fsq_{country_code.lower()}_places.{self._datasets_format}"
        
        # verify local dataset with places from FSQ OS Places
        if not os.path.exists(dataset_full_path):        
            self.update_data(country_code)      # update the dataset with data from FSQ OS Places API if it does not exist locally
        
        # Read and return the dataset
        return pd.read_parquet(dataset_full_path) if self._datasets_format == "parquet" else pd.read_csv(dataset_full_path)
    
        
    