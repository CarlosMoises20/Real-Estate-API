from backend.data.ingestion.source.api.base_api_data_source import BaseAPIDataSource

"""
This class is used to retrieve relevant data from the API of European Central Bank (BCE)

"""
class EuropeanCentralBank(BaseAPIDataSource):
    
    """Constructor of ECB class, with the default parameters"""
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
    
    
    """Retrieve JSON data from the API of ECB and return dataframe with relevant data"""
    def get_api_data(self):
        response = super().get_source_data()
        
        data = response.json()
                
        # TODO extract relevant parameters from the data
        
        return data