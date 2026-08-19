
from backend.data.ingestion.api.base_api_data_retrieval import BaseApiDataRetrieval

"""
This class is used to retrieve relevant data from the API of Open Street Map

"""
class OpenStreetMap(BaseApiDataRetrieval):
    
    """Retrieve JSON data from the API of INE"""
    def get_api_data(self, min_lon, min_lat, max_lon, max_lat):
        
        self._params = {
            "bbox": f"{min_lon},{min_lat},{max_lon},{max_lat}"
        }
        
        response = super().get_api_data()
        
        data = response.text
                
        # TODO extract relevant parameters from the data
        
        return data