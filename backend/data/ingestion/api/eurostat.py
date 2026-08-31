
from backend.data.ingestion.api.base_api_data_retrieval import BaseApiDataRetrieval
import pandas as pd
from io import StringIO
from backend.utils import *


"""This class is used to retrieve relevant data from the API of Eurostat"""
class Eurostat(BaseApiDataRetrieval):
    
    """Retrieve JSON data from the API of INE, from 2010 to the current year"""
    # TODO change to parquet
    def get_api_data(self, datasets_format):
        
        # This dict contains the dataset codes as keys and their abbreviated meaning as values
        datasets_list = {
            "nama_10_gdp": "gdp",                   # GDP per capita
            "ei_cphi_m": "consumer_prices",         # Harmonised index of consumer prices - monthly data
            "ei_hppi_q": "house_price_index"        # House price index (2025 = 100) - quarterly data
        }
        
        base_url = self._url
        
        df_list = []
        
        for dataset_code in list(datasets_list.items()):

            self._url = base_url
            
            self._url += f"{dataset_code[0]}/1.0"
            
            df = pd.read_csv(StringIO(super().get_api_data().text))
            
            # NOTE uncomment if you want to generate the dataset with data from the API in raw format (CSV for visualization)            
            """df.to_csv(
                f"./backend/datasets/external/eurostat_data_v0_{dataset_code[1]}_since_2010.csv", 
                index=False
            )"""
            
            # Remove empty columns
            df = df.dropna(axis=1, how="all")
            
            # Create columns "date_start" and "date_end" from column "TIME_PERIOD"
            
            df["TIME_PERIOD"] = df["TIME_PERIOD"].astype("string")      # Convert to string
            
            df[["date_start", "date_end"]] = pd.DataFrame(
                df["TIME_PERIOD"].apply(transform_data_to_range).tolist(),
                index=df.index
            )
            
            # Remove irrelevant attributes
            df = df.drop(columns=["STRUCTURE", "STRUCTURE_ID", "freq", "TIME_PERIOD"])
            
            # Save final dataset (NOTE: optional)            
            generate_dataset_from_df(df=df, 
                                     file_path_base=f"./backend/datasets/external/eurostat_data_{dataset_code[1]}_since_2010",
                                     dataset_format=datasets_format)
            
            df_list.append(df)
        
        
        return pd.concat(df_list, ignore_index=True)