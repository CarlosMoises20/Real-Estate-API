

from backend.data.ingestion.source.api.base_api_data_source import BaseAPIDataSource

"""
This class is used to retrieve relevant data from the API of Imovirtual

"""
class Imovirtual(BaseAPIDataSource):
    # TODO extract necessary data from the API starting from self.get_json_data    
    
    """Retrive JSON data from the API of INE and return dataframe with relevant data"""
    def get_source_data(self):
        response = super().get_source_data()
        
        data = response.json()
                
        # TODO extract relevant parameters from the data
        
        return data