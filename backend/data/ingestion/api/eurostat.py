
from backend.data.ingestion.api.base_source_data_retrieval import BaseSourceDataRetrieval
import pandas as pd
from io import StringIO
from backend.common.utils import *


"""This class is used to retrieve relevant data from the API of Eurostat"""
class Eurostat(BaseSourceDataRetrieval):
    
    """Retrieve JSON data from the API of INE and return dataframe with relevant data"""
    def get_source_data(self, datasets_format):
        
        df = pd.read_csv(StringIO(super().get_source_data().text))
        
        # NOTE uncomment if you want to generate the dataset with data from the API in raw format (CSV for visualization)            
        df.to_csv(
            f"./backend/datasets/external/eurostat_data_v0_gdp_since_2010.csv", 
            index=False
        )
        
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
                                file_path_base=f"./backend/datasets/external/eurostat_data_gdp_since_2010",
                                dataset_format=datasets_format)
        
        return df