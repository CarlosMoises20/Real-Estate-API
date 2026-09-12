
import os, kagglehub
import pandas as pd
from backend.data.ingestion.api.ine import INE
from backend.data.ingestion.api.eurostat import Eurostat
from backend.data.ingestion.api.geoapify import Geoapify
from backend.data.ingestion.api.fsq_os_places import FSQOSPlaces
from dotenv import load_dotenv


def aggregate_external_data(datasets_format, external_datasets_path="./backend/datasets/external/"):

    # TODO uncomment after code here is finished
    """ine = INE(url="https://www.ine.pt/ine/json_indicador/pindica.jsp", 
            headers={
                    "User-Agent": "Mozilla/5.0",
                    "Content-Type": "application/json"
                }
            )


    ine_data = ine.get_source_data(datasets_format=datasets_format)"""
    
    
    # API Reference: https://ec.europa.eu/eurostat/web/user-guides/data-browser/api-data-access/api-detailed-guidelines/api-statistics
    # SMDX-2.0 CSV
    # get GDP per capita data from Eurostat API (from 2010 to current year)
    # TODO uncomment after code here is finished
    """eurostat = Eurostat(url="https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/nama_10_gdp/1.0",
            params={
                "format": "csvdata",
                "formatVersion": "2.0",
                "compress": "false",
                "c[GEO]": "PT",                     # Portugal data
                "c[TIME_PERIOD]": "ge:2010"         # From 2010 to current year      
            },
            headers={
                    "User-Agent": "Mozilla/5.0",
                    "Content-Type": "application/json"
                }
            )
    
    eurostat_data = eurostat.get_source_data(datasets_format=datasets_format)"""
    

    # TODO choose an viable alternative to OpenStreetMap API to get facilities data, after a careful study of the available options, and implement it here
    
    # NOTE you need to create a .env file in the compose folder with the variable GEOAPIFY_API_KEY={your_api_key_here}
    
    load_dotenv(dotenv_path="./compose/.env")
    
    # TODO review if routes shouldn't also be included in the data retrieved from Geoapify API, and if so, implement it here
    """# Geoapify API Reference: https://apidocs.geoapify.com/docs/places/#introduction
    
    geoapify = Geoapify(url="https://api.geoapify.com/v2/places",
            params={
                "categories": "accommodation.hotel,accommodation.hostel,accommodation.motel,accommodation.guest_house,accommodation.apartment",
                "limit": 500,
                "apiKey": os.getenv("GEOAPIFY_API_KEY")
            },
            headers={
                    "User-Agent": "Mozilla/5.0",
                    "Content-Type": "application/json"
                }
            )
    
    df_list = geoapify.get_source_data(datasets_format=datasets_format)"""
    
    # Foursquare OS Places API Reference: https://developer.foursquare.com/reference/places-search
    # TODO fix this, the URL below is from FSQ Places API, it must be from FSQ OS Places
    fsq_os_places = FSQOSPlaces(url="https://places-api.foursquare.com/places/search",
            params={
                "ll": "38.7169,-9.1392",  # Lisbon coordinates
                "radius": 10000,          # 10 km radius
                "limit": 50               # 50 results
                #"query": "hotel,hostel,motel,guest house,apartment",
                #"fields": "fsq_id,name,location,categories,geocodes,distance,timezone",
                #"sort": "DISTANCE"
            },
            headers={
                    "accept": "application/json",
                    "X-Places-Api-Version": "2025-06-17",
                    "Authorization": f"Bearer {os.getenv('FSQ_API_KEY')}"
                }
            )
    
    df_fsq_list = fsq_os_places.get_source_data(datasets_format=datasets_format)

    

    
    
    
def aggregate_internal_data(datasets_format, internal_datasets_path="backend/datasets/internal/"):
    
    # Download CSV Kaggle dataset from the link
    # https://www.kaggle.com/datasets/luvathoms/portugal-real-estate-2024
    kaggle_dataset_path = kagglehub.dataset_download(handle="luvathoms/portugal-real-estate-2024", 
                                                     path="portugal_listinigs.csv",
                                                     force_download=True, 
                                                     output_dir=internal_datasets_path)
    
    df_kaggle = pd.read_csv(kaggle_dataset_path, sep=",", encoding="utf-8")
    
    
    # TODO Idealista and Imovirtual
    
    # TODO return list of dataframes, one for each dataset, instead of just returning the Kaggle
    # dataframe, and then implement the logic to join them in the prepare_internal_data function
    return [df_kaggle]
    
    
# TODO remove this when no longer needed    
if __name__ == "__main__":
    
    data_format = "csv"
    
    df_internal_list = aggregate_internal_data(datasets_format=data_format)
    
    df_external_list = aggregate_external_data(datasets_format=data_format)