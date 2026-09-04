
from backend.data.ingestion.api.base_api_data_retrieval import BaseApiDataRetrieval

"""
This class is used to retrieve relevant data from the API of Open Street Map

"""
class OpenStreetMap(BaseApiDataRetrieval):
    
    """Retrieve JSON data from the API of INE and return dataframe with relevant data"""
    def get_api_data(self, datasets_format):
        
        coordinates_list = [
            {
                "portugal_continent": {
                    "min_lon": -9.5,
                    "min_lat": 36.5,
                    "max_lon": 41.5,
                    "max_lat": 42.5
                },
            },
            {
                "portugal_azores": {
                    "min_lon": -31.5,
                    "min_lat": 36.5,
                    "max_lon": -24.5,
                    "max_lat": 40.5
                }
            },
            {
                "portugal_madeira": {
                    "min_lon": -17.5,
                    "min_lat": 32.5,
                    "max_lon": -12.5,
                    "max_lat": 37.5
                }
            }
        ]
        
        for coordinates in coordinates_list:
            
            region = next(iter(coordinates))
            coords = coordinates[region]
            
            self._params = {
                "bbox": f'{coords["min_lon"]},{coords["min_lat"]},{coords["max_lon"]},{coords["max_lat"]}'
            }
    
            response = super().get_api_data()
            
            data = response.text
            
            # Write XML file with data from the API (NOTE: optional, for visualization)
            # NOTE uncomment if you want to generate the dataset with data from the API in raw format
            # (XML for visualization)
            with open(f"./backend/datasets/external/open_street_map_data_v0_{region}.xml", 
                    "w",
                    encoding="utf-8") as f:
                f.write(data)
                
        # TODO extract relevant parameters from the data
        
        return data