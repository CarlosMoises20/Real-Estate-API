

from backend.data.ingestion.api.ine import INE
from backend.data.ingestion.api.open_street_map import OpenStreetMap
from backend.data.ingestion.api.european_central_bank import EuropeanCentralBank
import os
from dotenv import load_dotenv


def aggregate_external_data():

    ine = INE(url="https://www.ine.pt/ine/json_indicador/pindica.jsp?op=2&varcd=0014639&lang=PT",
            params={
                    "op": 2,
                    "varcd": "0014639",
                    "lang": "PT"
                }, 
            headers={
                    "User-Agent": "Mozilla/5.0",
                    "Content-Type": "application/json"
                }
            )


    ine_data = ine.get_api_data()
    
    """osm = OpenStreetMap(url="https://api.openstreetmap.org/api/0.6/map?bbox=-0.489,-0.123,0.236,51.569",
            headers={
                    "User-Agent": "Mozilla/5.0",
                    "Content-Type": "application/json"
                }
            )

    osm_data = osm.get_api_data()"""
    
    
    """ecb = EuropeanCentralBank(url="https://sdw-wsrest.ecb.europa.eu/service/data/",
            headers={'Accept':'application/json'}
            )

    ecb_data = ecb.get_api_data()"""
    
    
    # TODO Idealista and Imovirtual


    load_dotenv(dotenv_path="./compose/.env")
    
    
# TODO remove this when no longer needed    
if __name__ == "__main__":
    aggregate_external_data()