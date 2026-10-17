
from backend.data.ingestion.source.api.base_api_data_source import BaseAPIDataSource
import pandas as pd

"""
This class is used to retrieve relevant data from the API of Idealista

"""
class Idealista(BaseAPIDataSource):
    # TODO extract necessary data from the API
    
    def __init__(self, datasets_format, datasets_path):
            
        super().__init__(
            url="",         # TODO define URL
            headers={},     # TODO define headers 
            datasets_format=datasets_format, 
            datasets_path=datasets_path
        )
    
    """Retrive JSON data from the API of INE and return dataframe with relevant data"""
    def get_api_data(self):
        data = super().get_source_data().json()
        
        # TODO extract relevant parameters from the data
        
        df = pd.DataFrame(data).drop_duplicates()
        
        return df