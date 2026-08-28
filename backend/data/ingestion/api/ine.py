
from backend.data.ingestion.api.base_api_data_retrieval import BaseApiDataRetrieval
from backend.utils import transform_data_to_range
import pandas as pd

"""This class is used to retrieve relevant data from the API of INE (Instituto Nacional de Estatística)"""
class INE(BaseApiDataRetrieval):
    
    """Retrieve JSON data from specific 'varcd' of the API of INE"""
    def __extract_data_from_varcd(self, varcd, cols, value_attr_old_name, value_attr_name=None):
        
        self._params = {
            "op": 2, 
            "varcd": varcd, 
            "lang": "PT"
        }
        
        data = super().get_api_data().json()

        # NOTE draft
        """with open(f"./backend/datasets/external/ine_data_v0_{value_attr_name}.json", "w") as f:
            json.dump(data, f, indent=2)"""
    
        period = next(iter(data[0]["Dados"]))
        
        extracted_data = data[0]["Dados"][period]
        
        last_period_start, last_period_end = transform_data_to_range(period)
        
        final_data = []
        
        for elem in extracted_data:

            if not elem.get(value_attr_old_name):
                continue  
            
            final_data.append({
                "date_start": last_period_start,
                "date_end": last_period_end,
                **{col: elem.get(col) for col in cols if elem.get(col)},
                value_attr_name: float(elem.get(value_attr_old_name)) if "." in elem.get(value_attr_old_name) \
                    else int(elem.get(value_attr_old_name)),
            })
        
        # TODO review if this is necessary
        # generate the dataset that will be later used to train the model after being joined with other datasets
        pd.DataFrame(final_data).to_csv(f"./backend/datasets/external/ine_data_{value_attr_name}.csv", index=False)
        
    

    """Retrieve JSON data from the API of INE and return a CSV file with extracted relevant data"""
    def get_api_data(self):
        
        # Inflation
        # https://www.ine.pt/xportal/xmain?xpid=INE&xpgid=ine_api_db
        # https://smi.ine.pt/Indicador
        
        # Inflation (absolute value)
        self.__extract_data_from_varcd(varcd="0014639",
                                        value_attr_name="inflation_absolute_value",
                                        value_attr_old_name="valor",
                                        cols=["geocod", "geodsg", "dim_3", "dim_3_t"])

        # Inflation (homologous variation)
        self.__extract_data_from_varcd(varcd="0014647", 
                                        value_attr_name="inflation_homologous_variable",  
                                        value_attr_old_name="valor",   
                                        cols=["geocod", "geodsg", "dim_3", "dim_3_t"])
        
        # Inflation (monthly variation)
        self.__extract_data_from_varcd(varcd="0014645", 
                                        value_attr_name="inflation_monthly_variable",  
                                        value_attr_old_name="valor", 
                                        cols=["geocod", "geodsg", "dim_3", "dim_3_t"])
        
        # Inflation (yearly variation)
        self.__extract_data_from_varcd(varcd="0014649", 
                                        value_attr_name="inflation_yearly_variable",  
                                        value_attr_old_name="valor", 
                                        cols=["geocod", "geodsg", "dim_3", "dim_3_t"])
                
        # Average salary (euros)
        self.__extract_data_from_varcd(varcd="0014751", 
                                        value_attr_name="avg_salary_euros",  
                                        value_attr_old_name="valor", 
                                        cols=["geocod", "geodsg", "dim_3", "dim_3_t", 
                                            "dim_4", "dim_4_t"])
                
        # Gross disposable income (euros) 
        self.__extract_data_from_varcd(varcd="0014133", 
                                        value_attr_name="gross_disposable_income_euros",  
                                        value_attr_old_name="valor",
                                        cols=["geocod", "geodsg"])
        
        # Unemployment rate (%)
        self.__extract_data_from_varcd(varcd="0012136", 
                                        value_attr_name="unemployment_rate_percentage",  
                                        value_attr_old_name="valor", 
                                        cols=["geocod", "geodsg", "dim_3", "dim_3_t"])
          
        # Housing price per square meter (euros)
        self.__extract_data_from_varcd(varcd="0012255", 
                                        value_attr_name="housing_price_per_m2_euros",  
                                        value_attr_old_name="valor", 
                                        cols=["geocod", "geodsg", "dim_3", "dim_3_t"])
              
        # Number of sold houses & transactions
        self.__extract_data_from_varcd(varcd="0012785",
                                        value_attr_name="housing_sold_num_transactions",  
                                        value_attr_old_name="valor", 
                                        cols=["geocod", "geodsg", "dim_3", "dim_3_t", 
                                                "dim_4", "dim_4_t", "dim_5", "dim_5_t"])
        
        # TODO gather data from all sources to join with the internal dataset
        
        # TODO review if it's better to generate a final dataset
        # generate the dataset that will be later used to train the model after being joined with other datasets
        #pd.DataFrame(final_data).to_csv(f"./backend/datasets/external/ine_data_final.csv", index=False)