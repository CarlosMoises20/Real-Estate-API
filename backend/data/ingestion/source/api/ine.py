
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
                "User-Agent": "Mozilla/5.0"
            },
            datasets_format=datasets_format, 
            datasets_path=datasets_path
        )
    
    
    """
    Retrieve JSON data from a specific dataset, based on 'varcd' of the API of INE
    
        varcd: Code of the dataset
        cols: List of columns to extract from the data
        value_attr_old_name: Name of the column that contains the value of the data
        value_attr_name: Name of the column that will be used to store the data
        dim_3_total_code: Code of the total of the Dim3 column
        dim_4_total_code: Code of the total of the Dim4 column
        dim_5_total_code: Code of the total of the Dim5 column
        dataset_name: Name of the dataset (by default, it is set as None and the name of the dataset is passed as 'value_attr_name')
    
    """
    def __extract_data_from_varcd(self, varcd, cols, value_attr_old_name, value_attr_name,
                                  dim_3_total_code="T", dim_4_total_code="T", dim_5_total_code="T",
                                  dataset_name=None):
        
        self._params = {
            "op": 2, 
            "varcd": varcd, 
            "Dim1": "T",
            "lang": "EN"
        }
        
        if "dim_3_t" in cols:
            self._params["Dim3"] = dim_3_total_code
            
        if "dim_4_t" in cols:
            self._params["Dim4"] = dim_4_total_code
            
        if "dim_5_t" in cols:
            self._params["Dim5"] = dim_5_total_code
        
        # Here we don't convert this to dataframe yet, because data has a nested structure and this would add extra complexity in the dataframe pre-processing
        # Instead, we will extract relevant data from the JSON and then convert it to dataframe
        data = super().get_source_data().json()
        
        dataset_name = get_ine_dataset_name(dataset_name if dataset_name else value_attr_name)
        
        # NOTE uncomment this if you want to save the data in raw format
        with open(f"{self._datasets_path}/{dataset_name}.json", "w") as f:
            json.dump(data, f, indent=2)
        
        final_data = []
        
        for period, extracted_period_data in data[0]["Dados"].items():
            
            last_period_start, last_period_end = transform_data_to_range(period)
            
            for elem in extracted_period_data:

                if not elem.get(value_attr_old_name):
                    continue  
                
                final_data.append({
                    "date_start": last_period_start,
                    "date_end": last_period_end,
                    **{col: elem.get(col) for col in cols if elem.get(col)},
                    
                    # Convert to float or integer because "value_attr_name" is originally a string
                    value_attr_name: float(elem.get(value_attr_old_name)) if "." in elem.get(value_attr_old_name) \
                                                                        else int(elem.get(value_attr_old_name))
                })
            
        df_final = pd.DataFrame(final_data).drop_duplicates()
        
        # Save the merged dataset
        generate_dataset_from_df(df=df_final, 
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
                
        # Average salary (euros); from March 2014 to June 2026
        self.__extract_data_from_varcd(varcd="0011132", 
                                        value_attr_name="avg_salary_euros",  
                                        value_attr_old_name="valor", 
                                        cols=["geocod", "geodsg", "dim_3_t", "dim_4_t"])
        
        # Unemployment rate (%)
        # https://smi.ine.pt/Indicador/Detalhes/17432
        self.__extract_data_from_varcd(varcd="0012136", 
                                        value_attr_name="unemployment_rate",  
                                        value_attr_old_name="valor", 
                                        cols=["geocod", "geodsg", "dim_3_t"])
              
        # Number of sold houses & transactions
        self.__extract_data_from_varcd(varcd="0012785",
                                        value_attr_name="housing_num_transactions",  
                                        value_attr_old_name="valor", 
                                        cols=["geocod", "geodsg", "dim_3_t", "dim_4_t", "dim_5_t"],
                                        dim_3_total_code="H1")
        
        # Housing price per square meter (euros)
        # https://smi.ine.pt/Indicador/Detalhes/18371
        self.__extract_data_from_varcd(varcd="0012255", 
                                        value_attr_name="housing_price_per_m2_euros",  
                                        value_attr_old_name="valor", 
                                        cols=["geocod", "geodsg", "dim_3_t"],
                                        dim_3_total_code="H1")
        
        # Crime rate per region (from 1998 to 2013)
        self.__extract_data_from_varcd(varcd="0000849",
                                        value_attr_name="crime_rate",  
                                        value_attr_old_name="valor", 
                                        cols=["geocod", "geodsg", "dim_3_t"],
                                        dataset_name="crime_rate_from_1998_to_2013")
        
        # Crime rate per region (from 2011 to 2022)
        self.__extract_data_from_varcd(varcd="0008074",
                                        value_attr_name="crime_rate",  
                                        value_attr_old_name="valor", 
                                        cols=["geocod", "geodsg", "dim_3_t"],
                                        dataset_name="crime_rate_from_2011_to_2022")
        
        # Crime rate per region (from 2021 to 2025)
        self.__extract_data_from_varcd(varcd="0012260",
                                        value_attr_name="crime_rate",  
                                        value_attr_old_name="valor", 
                                        cols=["geocod", "geodsg", "dim_3_t"],
                                        dataset_name="crime_rate_from_2021_to_2025")
        