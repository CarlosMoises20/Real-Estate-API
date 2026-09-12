
from backend.data.ingestion.api.base_source_data_retrieval import BaseSourceDataRetrieval
import pandas as pd
from backend.common.constants import PORTUGAL_COORDINATES_LIST


"""This class is used to retrieve relevant data from the API of Geoapify"""
class Geoapify(BaseSourceDataRetrieval):
    
    """Retrieve JSON data from the API of Geoapify and return dataframe with relevant data"""
    def get_source_data(self, datasets_format):
        
        # Return data from Portugal Continent, Azores and Madeira
        # NOTE: in the future, this will be simplified to use countrycode:PT when the parameter is available, but for now,
        # we will use the coordinates of Portugal Continent, Azores and Madeira to get the data from Geoapify API
        
        df_list = []
        
        for coordinates in PORTUGAL_COORDINATES_LIST:
            
            region_name = list(coordinates.keys())[0] 
            
            coords = coordinates[region_name]
            
            self._params["filter"] = f"rect:{coords['min_lon']},{coords['min_lat']},{coords['max_lon']},{coords['max_lat']}"
            
            df = pd.DataFrame(super().get_source_data().json())
            
            # NOTE uncomment if you want to generate the dataset with data from the API in raw format, for visualization
            df.to_json(path_or_buf=f"./backend/datasets/external/geoapify_data_v0_facilities_{region_name}.json",
                        orient="records",
                        indent=2)
            
            df_list.append(df)
        
        
        """# Save final dataset (NOTE: optional)            
        generate_dataset_from_df(df=df_list, 
                                file_path_base=f"./backend/datasets/external/geoapify_data_facilities",
                                dataset_format=datasets_format)"""
        
        return df_list