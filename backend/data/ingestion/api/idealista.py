
from backend.data.ingestion.api.base_source_data_retrieval import BaseSourceDataRetrieval

"""
This class is used to retrieve relevant data from the API of Idealista

"""
class Idealista(BaseSourceDataRetrieval):
    # TODO extract necessary data from the API starting from self.get_json_data    
    
    """Retrive JSON data from the API of INE and return dataframe with relevant data"""
    def get_source_data(self, datasets_format):
        response = super().get_source_data()
        
        data = response.json()
                
        # TODO extract relevant parameters from the data
        
        return data