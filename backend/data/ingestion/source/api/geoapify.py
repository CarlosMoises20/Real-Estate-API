
from backend.data.ingestion.source.api.base_api_data_source import BaseAPIDataSource
import pandas as pd
from backend.common.constants import PORTUGAL_COORDINATES_LIST
from backend.common.utils import generate_dataset_from_df


"""This class is used to retrieve relevant data from the API of Geoapify"""
class Geoapify(BaseAPIDataSource):
    
    """Retrieve JSON data from the API of Geoapify and return dataframe with relevant data"""
    def get_api_data(self):
        
        # Return data from Portugal Continent, Azores and Madeira
        # NOTE: in the future, this will be simplified to use countrycode:PT when the parameter is available, but for now,
        # we will use the coordinates of Portugal Continent, Azores and Madeira to get the data from Geoapify API
        
        df_list = []
        
        for coordinates in PORTUGAL_COORDINATES_LIST:
            
            region_name = list(coordinates.keys())[0] 
            
            coords = coordinates[region_name]
            
            self._params["filter"] = f"rect:{coords['min_lon']},{coords['min_lat']},{coords['max_lon']},{coords['max_lat']}"
            
            data = super().get_source_data().json()
    
            data = [
                {
                    "name": elem["properties"].get("address_line1"),
                    "address": elem["properties"].get("formatted"),
                    "latitude": elem["properties"].get("lat"),
                    "longitude": elem["properties"].get("lon"),
                    "country": elem["properties"]["country_code"].upper() if elem["properties"].get("country_code") else None,
                    "category": ";".join(elem["properties"]["categories"]) if elem["properties"].get("categories") else None
                } 
                for elem in data.get("features", [])
                if (
                    elem.get("properties", {}).get("country_code") == "pt"
                    or elem.get("properties", {}).get("country") == "Portugal"
                )
            ]
            
            df_list.append(pd.DataFrame(data))
            
        df_final = pd.concat(df_list, ignore_index=True)
        
        # Save final dataset (NOTE: optional)            
        generate_dataset_from_df(df=df_final, 
                                file_path_base=f"{self._datasets_path}/geoapify_data_facilities",
                                dataset_format=self._datasets_format)
        
        return df_final