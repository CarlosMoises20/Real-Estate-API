

from backend.data.ingestion.api.base_api_data_retrieval import BaseApiDataRetrieval


class OpenStreetMap(BaseApiDataRetrieval):
    
    """Retrieve JSON data from the API of INE"""
    def get_api_data(self):
        
        # TODO set the 'bbox' parameter before re-affecting the URL; review this
        #self._url = "https://api.openstreetmap.org/api/0.6/map?bbox=-0.0,-0.0,0.236,51.569"
        
        response = super().get_api_data()
        
        data = response.json()
                
        # TODO extract relevant parameters from the data
        
        return data