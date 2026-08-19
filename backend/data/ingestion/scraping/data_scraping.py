

from backend.data.ingestion.api.ine import INE
from backend.data.ingestion.api.open_street_map import OpenStreetMap
from backend.data.ingestion.api.european_central_bank import EuropeanCentralBank
from backend.data.ingestion.api.eurostat import Eurostat
from backend.data.ingestion.api.banco_de_portugal import BancoDePortugal
from backend.data.ingestion.api.gov_data import GovData
from dotenv import load_dotenv


def aggregate_external_data():

    ine = INE(url="https://www.ine.pt/ine/json_indicador/pindica.jsp",
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
    
    
    # API Reference: https://ec.europa.eu/eurostat/web/user-guides/data-browser/api-data-access/api-detailed-guidelines/api-statistics
    
    eurostat = Eurostat(url="https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/nama_10_gdp",
            params={
                "format": "JSON",
                "lang": "EN",       # Only three possible values: "EN" (English), "FR" (French) and "DE" (German)
                "time": "2026"
            },
            headers={
                    "User-Agent": "Mozilla/5.0",
                    "Content-Type": "application/json"
                }
            )
    
    eurostat_data = eurostat.get_api_data()
    
    # References: https://publicapis.io/open-street-map-api
    osm = OpenStreetMap(url="https://api.openstreetmap.org/api/0.6/map",
            headers={
                    "User-Agent": "Mozilla/5.0",
                    "Content-Type": "application/json"
                }
            )

    osm_data = osm.get_api_data(min_lon=-0.15, min_lat=51.50, max_lon=-0.14, max_lat=51.51)
    
    # References: https://data.ecb.europa.eu/help/api/data 
    # https://fgeerolf.com/data/ecb/api.html
    # https://analisemacro.com.br/data-science/como-coletar-dados-do-banco-central-europeu-ecb-usando-a-api-com-o-python/
    # TODO review the URI according to the type of data that is supposed to be returned
    ecb = EuropeanCentralBank(url="https://data-api.ecb.europa.eu/service/data/FM/M.U2.EUR.RT.MM.EURIBOR1YD_.HSTA",
                              params={
                                  "startPeriod": "2010",
                                  "format": "jsondata",
                              },
                            headers={'Accept':'application/json'})

    ecb_data = ecb.get_api_data()
    
    #print(ecb_data)
    
    
    # References: https://bpstat.bportugal.pt/api-de-dados
    # TODO: redefine the URI according to the correct domain and dataset
    pt_bank = BancoDePortugal(url="https://bpstat.bportugal.pt/data/v1/domains/29/datasets/23e0cdd56bddb4ad3016a9c3ad63a539",
                                params={
                                    "lang": "PT",
                                    "series_ids": "12531971",
                                },
                            headers={'Accept':'application/json'})

    pt_bank_data = pt_bank.get_api_data()
    
    #print(pt_bank_data)
    
    # TODO review the URI, the Swagger UI contains several GET requests, consider those in the class GovData implementation
    # References: https://dados.gov.pt/pt/dataservices
    # https://dados.gov.pt/pt/recursos/desenvolvimento/referencia-api 
    gov = GovData(url="https://dados.gov.pt/api/1/",
                    headers={'Accept':'application/json'})
    
    #gov_data = gov.get_api_data()


    load_dotenv(dotenv_path="./compose/.env")
    
    
def aggregate_internal_data():
    # TODO Idealista and Imovirtual
    pass
    
    
# TODO remove this when no longer needed    
if __name__ == "__main__":
    aggregate_external_data()