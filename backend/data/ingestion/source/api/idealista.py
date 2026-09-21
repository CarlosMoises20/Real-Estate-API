
from backend.data.ingestion.source.api.base_api_data_source import BaseAPIDataSource

"""
This class is used to retrieve relevant data from the API of Idealista

"""
class Idealista(BaseAPIDataSource):
    # TODO extract necessary data from the API
    
    """Retrive JSON data from the API of INE and return dataframe with relevant data"""
    def get_source_data(self):
        response = super().get_source_data()
        
        data = response.json()
                
        # TODO extract relevant parameters from the data
        
        return data