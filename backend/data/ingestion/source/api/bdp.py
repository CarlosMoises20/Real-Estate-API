from backend.data.ingestion.source.api.base_api_data_source import BaseAPIDataSource

"""
This class is used to retrieve relevant data from the API of Banco de Portugal (BdP)

"""
class BancoDePortugal(BaseAPIDataSource):
    
    """Constructor of BdP class, with the default parameters"""
    # TODO add parameters
    def __init__(self, datasets_format, datasets_path):
        
        super().__init__(
            url="",
            params={
                 
            },
            headers={
                
            },
            datasets_format=datasets_format, 
            datasets_path=datasets_path
        )
    
    
    """Retrieve JSON data from the API of BDP and return dataframe with relevant data"""
    def get_api_data(self):
        response = super().get_source_data()
        
        data = response.json()
                
        # TODO extract relevant parameters from the data
        
        return data