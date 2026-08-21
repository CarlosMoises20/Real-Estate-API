
from backend.data.ingestion.api.base_api_data_retrieval import BaseApiDataRetrieval

"""
This class is used to retrieve relevant data from the API of INE (Instituto Nacional de Estatística)

"""
class INE(BaseApiDataRetrieval):
    
    """Retrieve JSON data from specific 'varcd' of the API of INE"""
    def __extract_data_from_varcd(self, varcd, id, value):
        
        self._params = {"op": 2, "varcd": varcd, "lang": "PT"}
        
        data = super().get_api_data().json()
        
        last_period = data[0]["UltimoPref"]
        
        data = data[0]["Dados"][last_period]  
        
        # TODO this time information is relevant, see how to use this
        last_period_time = data[0]["DataUltimoAtualizacao"] 
       
        return [{"id": id, "value": float(elem.get(value)) if elem.get(value) else None} for elem in data]
    

    """Retrieve JSON data from the API of INE"""
    def get_api_data(self):
        
        # Inflation
        data_inflation = self.__extract_data_from_varcd(varcd="0014639", id="dim_3", value="valor")
                
        # Average salary
        data_average_salary = self.__extract_data_from_varcd(varcd="0014751", id="dim_3", value="valor")
        
        #print(data_average_salary)
                
        # Gross disposable income (TODO review)
        data_gross_disposable_income = self.__extract_data_from_varcd(varcd="0014133", id="dim_3", value="valor")
                
        # Unemployment rate (TODO review)
        data_unemployment_rate = self.__extract_data_from_varcd(varcd="0012136", id="dim_3", value="valor")
          
        # Housing price per square meter (TODO review)
        data_housing_price_per_m2 = self.__extract_data_from_varcd(varcd="0012255", id="dim_3", value="valor")
              
        # Number of sold houses & transactions (TODO review)
        data_housing_sold = self.__extract_data_from_varcd(varcd="0012785", id="dim_3", value="valor")
        
        # TODO gather data from all sources (varcd: 0014639, 0014133, ...)
        final_data = data_inflation
        
        return final_data
    
    
    
"""with open("./backend/datasets/external/ine_data_average_salary.json", "w") as f:
    json.dump(data_average_salary, f, indent=2)"""