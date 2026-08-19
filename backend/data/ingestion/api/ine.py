
from backend.data.ingestion.api.base_api_data_retrieval import BaseApiDataRetrieval

"""
This class is used to retrieve relevant data from the API of INE (Instituto Nacional de Estatística)

"""
class INE(BaseApiDataRetrieval):

    """Retrive JSON data from the API of INE"""
    def get_api_data(self):
        response = super().get_api_data()
        
        data = response.json()
        
        # TODO extract relevant parameters from the data
        
        return data