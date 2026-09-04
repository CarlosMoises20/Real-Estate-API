
from backend.data.ingestion.api.base_api_data_retrieval import BaseApiDataRetrieval
from backend.utils import *
import pandas as pd
import json         # If you want to generate the dataset with data from the API in raw format (JSON for visualization)

"""This class is used to retrieve relevant data from the API of INE (Instituto Nacional de Estatística)"""
class INE(BaseApiDataRetrieval):
    
    """Retrieve JSON data from specific 'varcd' of the API of INE"""
    def __extract_data_from_varcd(self, varcd, cols, value_attr_old_name, datasets_format, value_attr_name=None):
        
        self._params = {
            "op": 2, 
            "varcd": varcd, 
            "lang": "PT"
        }
        
        # Here we don't convert this to dataframe yet, because data has a nested structure and this would add extra complexity in the dataframe pre-processing
        # Instead, we will extract relevant data from the JSON and then convert it to dataframe
        data = super().get_api_data().json()

        # NOTE uncomment if you want to generate the dataset with data from the API in raw format, for visualization
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
            
        final_df = pd.DataFrame(final_data)
        
        # NOTE optional
        # generate the dataset that will be later used to train the model after being joined with other datasets
        generate_dataset_from_df(df=final_df, 
                                 file_path_base=f"./backend/datasets/external/ine_data_{value_attr_name}", 
                                 dataset_format=datasets_format)
        
        return final_df
        
    

    """Retrieve JSON data from the API of INE and return a pandas dataframe with extracted relevant data"""
    def get_api_data(self, datasets_format):
        
        # Inflation
        # https://www.ine.pt/xportal/xmain?xpid=INE&xpgid=ine_api_db
        # https://smi.ine.pt/Indicador
        
        # Inflation (absolute value)
        df_inflation_abs_value = self.__extract_data_from_varcd(varcd="0014639",
                                        value_attr_name="inflation_absolute_value",
                                        value_attr_old_name="valor",
                                        cols=["geocod", "geodsg", "dim_3", "dim_3_t"],
                                        datasets_format=datasets_format)

        # Inflation (homologous variation)
        df_inflation_homologous_variable = self.__extract_data_from_varcd(varcd="0014647", 
                                        value_attr_name="inflation_homologous_variable",  
                                        value_attr_old_name="valor",   
                                        cols=["geocod", "geodsg", "dim_3", "dim_3_t"],
                                        datasets_format=datasets_format)
        
        # Inflation (monthly variation)
        df_inflation_monthly_variable = self.__extract_data_from_varcd(varcd="0014645", 
                                        value_attr_name="inflation_monthly_variable",  
                                        value_attr_old_name="valor", 
                                        cols=["geocod", "geodsg", "dim_3", "dim_3_t"],
                                        datasets_format=datasets_format)
        
        # Inflation (yearly variation)
        df_inflation_yearly_variable = self.__extract_data_from_varcd(varcd="0014649", 
                                        value_attr_name="inflation_yearly_variable",  
                                        value_attr_old_name="valor", 
                                        cols=["geocod", "geodsg", "dim_3", "dim_3_t"],
                                        datasets_format=datasets_format)
        
         # Inflation (yearly variation)
        df_housing_credit_rate = self.__extract_data_from_varcd(varcd="0001972", 
                                        value_attr_name="housing_credit_rate",  
                                        value_attr_old_name="valor", 
                                        cols=["geocod", "geodsg", "dim_3", "dim_3_t"],
                                        datasets_format=datasets_format)
                
        # Average salary (euros)
        df_avg_salary_euros = self.__extract_data_from_varcd(varcd="0014751", 
                                        value_attr_name="avg_salary_euros",  
                                        value_attr_old_name="valor", 
                                        cols=["geocod", "geodsg", "dim_3", "dim_3_t", 
                                            "dim_4", "dim_4_t"],
                                        datasets_format=datasets_format)
                
        # Gross disposable income (euros) 
        df_gross_disposable_income_euros = self.__extract_data_from_varcd(varcd="0014133", 
                                        value_attr_name="gross_disposable_income_euros",  
                                        value_attr_old_name="valor",
                                        cols=["geocod", "geodsg"],
                                        datasets_format=datasets_format)
        
        # Unemployment rate (%)
        df_unemployment_rate_percentage = self.__extract_data_from_varcd(varcd="0012136", 
                                        value_attr_name="unemployment_rate_percentage",  
                                        value_attr_old_name="valor", 
                                        cols=["geocod", "geodsg", "dim_3", "dim_3_t"],
                                        datasets_format=datasets_format)
          
        # Housing price per square meter (euros)
        df_housing_price_per_m2_euros = self.__extract_data_from_varcd(varcd="0012255", 
                                        value_attr_name="housing_price_per_m2_euros",  
                                        value_attr_old_name="valor", 
                                        cols=["geocod", "geodsg", "dim_3", "dim_3_t"],
                                        datasets_format=datasets_format)
              
        # Number of sold houses & transactions
        df_housing_sold_num_transactions = self.__extract_data_from_varcd(varcd="0012785",
                                        value_attr_name="housing_sold_num_transactions",  
                                        value_attr_old_name="valor", 
                                        cols=["geocod", "geodsg", "dim_3", "dim_3_t", 
                                                "dim_4", "dim_4_t", "dim_5", "dim_5_t"],
                                        datasets_format=datasets_format)
        
        
        df_list = [df_inflation_abs_value, 
                   df_inflation_homologous_variable, 
                   df_inflation_monthly_variable, 
                   df_inflation_yearly_variable, 
                   df_housing_credit_rate,
                   df_avg_salary_euros, 
                   df_gross_disposable_income_euros, 
                   df_unemployment_rate_percentage, 
                   df_housing_price_per_m2_euros, 
                   df_housing_sold_num_transactions]
        
        return pd.concat(df_list, ignore_index=True)