
from backend.data.ingestion.source.api.base_api_data_source import BaseAPIDataSource
from backend.common.utils import *
from backend.common.dataset_names import get_ine_dataset_name
import pandas as pd
import json, glob
from pathlib import Path

"""This class is used to retrieve relevant data from the API of INE (Instituto Nacional de Estatística)"""
class INE(BaseAPIDataSource):
    
    def __init__(self, datasets_format, datasets_path):
        
        super().__init__(
            url="https://www.ine.pt/ine/json_indicador/pindica.jsp", 
            headers={
                "User-Agent": "Mozilla/5.0",
                "Content-Type": "application/json"
            },
            datasets_format=datasets_format, 
            datasets_path=datasets_path
        )
    
    
    """Retrieve JSON data from specific 'varcd' of the API of INE"""
    def __extract_data_from_varcd(self, varcd, cols, value_attr_old_name, value_attr_name):
        
        self._params = {
            "op": 2, 
            "varcd": varcd, 
            "lang": "PT"
        }
        
        # Here we don't convert this to dataframe yet, because data has a nested structure and this would add extra complexity in the dataframe pre-processing
        # Instead, we will extract relevant data from the JSON and then convert it to dataframe
        data = super().get_source_data().json()
    
        period = next(iter(data[0]["Dados"]))
        
        last_period_start, last_period_end = transform_data_to_range(period)
        
        dataset_name = get_ine_dataset_name(value_attr_name)
        
        # NOTE uncomment this if you want to save the data in raw format
        """with open(f"{self._datasets_path}/{dataset_name}_from_{last_period_start}_to_{last_period_end}.json", "w") as f:
            json.dump(data, f, indent=2)"""
            
        extracted_data = data[0]["Dados"][period]
        
        final_data = []
        
        for elem in extracted_data:

            if not elem.get(value_attr_old_name):
                continue  
            
            final_data.append({
                "date_start": last_period_start,
                "date_end": last_period_end,
                **{col: elem.get(col) for col in cols if elem.get(col)},
                value_attr_name: float(elem.get(value_attr_old_name)) if "." in elem.get(value_attr_old_name) \
                    else int(elem.get(value_attr_old_name))
            })
            
        final_df = pd.DataFrame(final_data).drop_duplicates()
        
        # NOTE here it is necessary to generate because the API only stores data from the most recent months
        # generate the dataset that will be later used to train the model after being joined with other datasets
        generate_dataset_from_df(df=final_df, 
                                 file_path_base=f"{self._datasets_path}/{dataset_name}_from_{last_period_start}_to_{last_period_end}", 
                                 dataset_format=self._datasets_format)
        
        # Gather all datasets with name starting with "{dataset_name}", except the final one called "{dataset_name}"
        # and merge them into a single dataset 
        # Because this will include older datasets
        df_list = pd.concat([
            generate_df_from_dataset(file_path_base=f"{self._datasets_path}/{Path(file).stem}", 
                                     dataset_format=self._datasets_format)
            
            for file in glob.glob(
                f"{self._datasets_path}/{dataset_name}*.{self._datasets_format}"
            ) if Path(file).stem != dataset_name
        ])
            
        # Based on all columns, remove duplicated entries
        df_list = df_list.drop_duplicates()
        
        # Save the merged dataset
        generate_dataset_from_df(df=df_list, 
                                 file_path_base=f"{self._datasets_path}/{dataset_name}",
                                 dataset_format=self._datasets_format)
        
        
    """Retrieve JSON data from the API of INE and return a pandas dataframe with extracted relevant data"""
    def get_api_data(self):
        
        # Inflation
        # https://www.ine.pt/xportal/xmain?xpid=INE&xpgid=ine_api_db
        # https://smi.ine.pt/Indicador

        # Inflation (homologous variation; growth rate)
        self.__extract_data_from_varcd(varcd="0014647", 
                                        value_attr_name="inflation_growth_rate",  
                                        value_attr_old_name="valor",   
                                        cols=["geocod", "geodsg", "dim_3_t"])
        
        # Housing credit rate
        # https://smi.ine.pt/Indicador/Detalhes/657
        # 17, "Lisboa": a região (NUTS II)
        # 171, "Grande Lisboa": NUTS III
        # 1711106, "Lisboa": o município
        self.__extract_data_from_varcd(varcd="0001972", 
                                        value_attr_name="housing_credit_rate",  
                                        value_attr_old_name="valor", 
                                        cols=["geocod", "geodsg", "geocod", "dim_3_t"])
                
        # Average salary (euros)
        self.__extract_data_from_varcd(varcd="0014751", 
                                        value_attr_name="avg_salary_euros",  
                                        value_attr_old_name="valor", 
                                        cols=["geocod", "geodsg", "dim_3_t", "dim_4_t"])
                
        # Gross disposable income (euros) 
        self.__extract_data_from_varcd(varcd="0014133", 
                                        value_attr_name="gross_disposable_income_euros",  
                                        value_attr_old_name="valor",
                                        cols=["geocod", "geodsg"])
        
        # Unemployment rate (%)
        # https://smi.ine.pt/Indicador/Detalhes/17432
        self.__extract_data_from_varcd(varcd="0012136", 
                                        value_attr_name="unemployment_rate",  
                                        value_attr_old_name="valor", 
                                        cols=["geocod", "geodsg", "dim_3_t"])
              
        # Number of sold houses & transactions
        self.__extract_data_from_varcd(varcd="0012785",
                                        value_attr_name="housing_sold_num_transactions",  
                                        value_attr_old_name="valor", 
                                        cols=["geocod", "geodsg", "dim_3_t", "dim_4_t", "dim_5_t"])
        
        # Housing price per square meter (euros)
        # https://smi.ine.pt/Indicador/Detalhes/18371
        self.__extract_data_from_varcd(varcd="0012255", 
                                        value_attr_name="housing_price_per_m2_euros",  
                                        value_attr_old_name="valor", 
                                        cols=["geocod", "geodsg", "dim_3_t"])