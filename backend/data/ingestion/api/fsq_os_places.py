
from backend.data.ingestion.api.base_source_data_retrieval import BaseSourceDataRetrieval
import pandas as pd
from backend.common.utils import *
import json        # If you want to generate the dataset with data from the API in raw format (JSON for visualization)

"""This class is used to retrieve relevant data from the API of Foursquare OS Places"""
class FSQOSPlaces(BaseSourceDataRetrieval):
    
    """Retrieve JSON data from the API of Foursquare OS Places and return dataframe with relevant data"""
    def get_source_data(self, datasets_format):
        
        data = super().get_source_data().json()
        
        # NOTE uncomment if you want to generate the dataset with data from the API in raw format, for visualization
        with open(f"./backend/datasets/external/fsq_os_places_data_v0_facilities.json", "w") as f:
            json.dump(data, f, indent=2)
            
        # TODO pre-processing steps before converting to dataframe, if needed, to extract 
        # relevant data from the JSON and then convert it to dataframe; 
        # it's more simple because of nested structure of the JSON data returned by the API of Foursquare OS Places
        
        # TODO review this after fixing the URL returned in the constructor of the FSQOSPlaces class
        data = data["results"]
        
        df = pd.DataFrame(data)
        
        """ # NOTE uncomment if you want to generate the dataset with data from the API in raw format (CSV for visualization)            
        
        # Save final dataset (NOTE: optional)            
        generate_dataset_from_df(df=df, 
                                file_path_base=f"./backend/datasets/external/fsq_os_places_data_facilities",
                                dataset_format=datasets_format)"""
        
        return df
        
        