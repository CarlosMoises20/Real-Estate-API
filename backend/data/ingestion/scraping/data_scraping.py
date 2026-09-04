

from backend.data.ingestion.api.ine import INE
from backend.data.ingestion.api.open_street_map import OpenStreetMap
from backend.data.ingestion.api.eurostat import Eurostat
from dotenv import load_dotenv


def aggregate_external_data(datasets_format):

    # TODO uncomment after code here is finished
    """ine = INE(url="https://www.ine.pt/ine/json_indicador/pindica.jsp", 
            headers={
                    "User-Agent": "Mozilla/5.0",
                    "Content-Type": "application/json"
                }
            )


    ine_data = ine.get_api_data(datasets_format=datasets_format)"""
    
    
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
    
    eurostat_data = eurostat.get_api_data(datasets_format=datasets_format)"""
    
    
    # References: https://publicapis.io/open-street-map-api
    # TODO finish extraction of relevant data from the API of Open Street Map
    osm = OpenStreetMap(url="https://api.openstreetmap.org/api/0.6/map",
            headers={
                    "User-Agent": "Mozilla/5.0",
                    "Content-Type": "application/json"
                }
            )

    osm_data = osm.get_api_data(datasets_format=datasets_format)
    


    
    
    
def aggregate_internal_data(datasets_format):
    # TODO Idealista and Imovirtual
    pass
    
    
# TODO remove this when no longer needed    
if __name__ == "__main__":
    
    #load_dotenv(dotenv_path="./compose/.env")
    
    data_format = "csv"
    
    aggregate_internal_data(datasets_format=data_format)
    
    aggregate_external_data(datasets_format=data_format)