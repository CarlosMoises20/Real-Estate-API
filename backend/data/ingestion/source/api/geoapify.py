
from backend.data.ingestion.source.api.base_api_data_source import BaseAPIDataSource
import pandas as pd


"""This class is used to retrieve relevant data from the API of Geoapify"""
class Geoapify(BaseAPIDataSource):
    
    """Retrieve JSON data from the API of Geoapify and return dataframe with relevant data"""
    def get_api_data(self, categories_list, latitude, longitude, radius_meters):
        
        self._params["categories"] = ",".join(categories_list)    
        
        self._params["filter"] = f"circle:{longitude},{latitude},{radius_meters}"

        data = super().get_source_data().json()

        filtered_data = [
            {
                "name": elem["properties"].get("address_line1"),
                "address": elem["properties"].get("formatted"),
                "latitude": elem["properties"].get("lat"),
                "longitude": elem["properties"].get("lon"),
                "country": elem["properties"]["country_code"].upper() if elem["properties"].get("country_code") else None,
                "category": ";".join(elem["properties"]["categories"]) if elem["properties"].get("categories") else None
            } 
            for elem in data.get("features", [])
        ]
        
        return pd.DataFrame(filtered_data)
    
    


"""# NOTE these values are only examples, these must be reviewed before uncommenting the code and implement it

# Latitude of the location
geoapify_latitude = 38.79556645168411

# Longitude of the location
geoapify_longitude = -9.330647695664439

# 50 km radius around place on the indicated latitude and longitude coordinates
geoapify_radius_meters = 50000  

categories_list = [
    "healthcare", "public_transport", "emergency",
    "childcare", "catering", "service", "maritime", "parking",
    "entertainment", "leisure", "low_emission_zone", "natural",
    "national_park"
]

# Geoapify API Reference: https://apidocs.geoapify.com/docs/places/#introduction
geoapify = Geoapify(
                url="https://api.geoapify.com/v2/places",
                params={
                    "limit": 500,
                    "apiKey": os.getenv("GEOAPIFY_API_KEY")
                },
                headers={
                        "User-Agent": "Mozilla/5.0",
                        "Content-Type": "application/json"
                    },
                datasets_format=datasets_format,
                datasets_path=external_datasets_path
            )

geoapify.get_api_data(categories_list=categories_list, 
                        latitude=geoapify_latitude, 
                        longitude=geoapify_longitude, 
                        radius_meters=geoapify_radius_meters)"""