
from backend.data.ingestion.api.base_api_data_retrieval import BaseApiDataRetrieval
from backend.utils import transform_data_to_range
from datetime import date
import json

"""
This class is used to retrieve relevant data from the API of INE (Instituto Nacional de Estatística)

"""
class INE(BaseApiDataRetrieval):
    
    """Retrieve JSON data from specific 'varcd' of the API of INE"""
    def __extract_data_from_varcd(self, varcd, data_type, id_cols, name_cols, value):
        
        # TODO this still has to be reviewed
        dim1_values = [f"S7A{year}" for year in range(2010, date.today().year + 1)]
        
        final_data = {
            "Type of Data": data_type, 
            "Data": []
        }
        
        for dim_1 in dim1_values:
        
            self._params = {
                "op": 2, 
                "varcd": varcd, 
                "Dim1": dim_1,
                "lang": "PT"
            }
        
            data = super().get_api_data().json()
        
            # NOTE optional, if you want to generate the dataset
            with open(f"./backend/datasets/external/ine_data_v0_{dim_1}.json", "w") as f:
                json.dump(data, f, indent=2)
            
            #last_update_time = data[0]["DataUltimoAtualizacao"] 
            
            if data[0]["Sucesso"]["Falso"]:
                continue
        
            period = next(iter(data[0]["Dados"]))
            
            extracted_data = data[0]["Dados"][period]
        
            #print(data[0]["Dados"].keys())
            
            last_period_start, last_period_end = transform_data_to_range(period)
            
            for elem in extracted_data:

                if not elem.get(value):
                    continue  
        
                elem_data = {
                    #"Last Update Time": last_update_time,
                    "id": "".join(elem[id] for id in id_cols if elem.get(id)), 
                    "name": " - ".join(elem[name] for name in name_cols if elem.get(name)), 
                    "value": float(elem.get(value)),
                    "Data Period": period,
                    "Data Period Start": last_period_start,
                    "Data Period End": last_period_end
                }
                
                final_data["Data"].append(elem_data)
        
        return final_data
        
    

    """Retrieve JSON data from the API of INE"""
    def get_api_data(self):
        
        # Inflation
        data_inflation = self.__extract_data_from_varcd(varcd="0014639", 
                                                        data_type="Inflation",
                                                        id_cols=["geocod", "dim_3"],
                                                        name_cols=["geodsg", "dim_3_t"],    
                                                        value="valor")
        
        print(data_inflation) 
                
        # Average salary
        data_average_salary = self.__extract_data_from_varcd(varcd="0014751", 
                                                             data_type="Average salary", 
                                                             id_cols=["geocod", "dim_3", "dim_4"],
                                                             name_cols=["geodsg", "dim_3_t", "dim_4_t"],         
                                                             value="valor")
        
        #print(data_average_salary)
                
        # Gross disposable income (TODO review)
        data_gross_disposable_income = self.__extract_data_from_varcd(varcd="0014133", 
                                                                      data_type="Gross disposable income",
                                                                      id_cols=["geocod"], 
                                                                      name_cols=["geodsg"],
                                                                      value="valor")
        
        #print(data_gross_disposable_income)        
        
        # Unemployment rate (TODO review)
        data_unemployment_rate = self.__extract_data_from_varcd(varcd="0012136", 
                                                                data_type="Unemployment rate",
                                                                id_cols=["geocod", "dim_3"],
                                                                name_cols=["geodsg", "dim_3_t"],            
                                                                value="valor")
        
        #print(data_unemployment_rate)
          
        # Housing price per square meter (TODO review)
        data_housing_price_per_m2 = self.__extract_data_from_varcd(varcd="0012255", 
                                                                   data_type="Housing price per square meter",  
                                                                   id_cols=["geocod", "dim_3"],
                                                                   name_cols=["geodsg", "dim_3_t"],    
                                                                   value="valor")
              
        #print(data_housing_price_per_m2)
              
        # Number of sold houses & transactions (TODO review)
        data_housing_sold = self.__extract_data_from_varcd(varcd="0012785", 
                                                           data_type="Number of sold houses & transactions",
                                                           id_cols=["geocod", "dim_3", "dim_4", "dim_5"],
                                                           name_cols=["geodsg", "dim_3_t", "dim_4_t", "dim_5_t"],    
                                                           value="valor")
        
        #print(data_housing_sold)
        
        # TODO gather data from all sources (inflation, average salary, gross disposable income, 
        # unemployment rate, housing price per square meter, number of sold houses & transactions)
        final_data = data_inflation
        
        return final_data
    
    
    
"""with open("./backend/datasets/external/ine_data_average_salary.json", "w") as f:
    json.dump(data_average_salary, f, indent=2)"""