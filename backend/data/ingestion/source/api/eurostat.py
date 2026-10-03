
from backend.data.ingestion.source.api.base_api_data_source import BaseAPIDataSource
import pandas as pd
from io import StringIO
from backend.common.utils import generate_dataset_from_df, transform_data_to_range


"""This class is used to retrieve relevant data from the API of Eurostat"""
class Eurostat(BaseAPIDataSource):
    
    """Retrieve JSON data from the API of INE and return dataframe with relevant data"""
    def get_api_data(self):
        
        df = pd.read_csv(StringIO(super().get_source_data().text))
        
        # NOTE uncomment if you want to generate CSV with the dataframe before pre-processing
        #df.to_csv("./backend/datasets/external/eurostat_data_gdp_since_2010_v0.csv", index=False)
        
        # Remove samples where confidential status is C (confidential), N (not for publication) or P (information under non-statistical secrecy arrangements)
        # since this means that the information cannot be published in another API
        df = df[~df["CONF_STATUS"].isin(["C", "N", "P"])]
        
        # Remove empty columns
        df = df.dropna(axis=1, how="all")
        
        # Create columns "date_start" and "date_end" from column "TIME_PERIOD"
        
        df["TIME_PERIOD"] = df["TIME_PERIOD"].astype("string")      # Convert to string
        
        df[["date_start", "date_end"]] = pd.DataFrame(
            df["TIME_PERIOD"].apply(transform_data_to_range).tolist(),
            index=df.index
        )
    
        # Remove irrelevant attributes
        df = df.drop(columns=["STRUCTURE", "STRUCTURE_ID", "freq", "TIME_PERIOD", "OBS_FLAG"])
        
        # Rename relevant attributes
        df = df.rename(columns={
            "OBS_VALUE": "gdp_value",
            "geo": "country_code"
        })
        
        # Save final dataset            
        generate_dataset_from_df(df=df, 
                                file_path_base=f"{self._datasets_path}/eurostat_gdp_data_since_2010",
                                dataset_format=self._datasets_format)
        
        return df