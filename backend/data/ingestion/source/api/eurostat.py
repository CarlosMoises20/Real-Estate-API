
from backend.data.ingestion.source.api.base_api_data_source import BaseAPIDataSource
import pandas as pd
from io import StringIO
from backend.common.utils import generate_dataset_from_df, transform_data_to_range


"""This class is used to retrieve relevant data from the API of Eurostat"""
class Eurostat(BaseAPIDataSource):
    
    """
    Retrieve JSON data from the API of INE and return dataframe with relevant data
    
    Parameters:
        - country_code: The country code for which to retrieve data (e.g., "PT" for Portugal)
        - time_period: The time period for which to retrieve data. Examples:
            "ge:2010" for data from 2010 to the current year
            "eq:2020" for data from 2020 only
            "gt:2015" for data from 2015 onwards (greater than 2015)
            "lt:2018" for data until 2018 (less than 2018)
            "ge:2010,lt:2018" for data from 2010 to 2018
            
        - dataset_code: The dataset code for the specific data to retrieve (e.g., "nama_10_gdp" for GDP data)
    
    Source: https://ec.europa.eu/eurostat/fr/web/user-guides/data-browser/api-data-access/api-getting-started/sdmx3.0
    
    """
    def get_api_data(self, country_code, time_period, dataset_code):
        
        self._url += f"{dataset_code}/1.0"
        
        self._params["c[GEO]"] = country_code
        
        self._params["c[TIME_PERIOD]"] = time_period
        
        df = pd.read_csv(StringIO(super().get_source_data().text))
        
        # NOTE uncomment if you want to generate CSV with the dataframe before pre-processing
        #df.to_csv("./backend/datasets/external/eurostat_gdp_data_since_2010_v0.csv", index=False)
        
        # Remove samples where confidential status is C (confidential), N (not for publication) or P (information under non-statistical secrecy arrangements)
        # since this means that the information cannot be published in another API
        df = df[~df["CONF_STATUS"].isin(["C", "N", "P"])]
        
        # Keep samples with "unit" attribute with values representing relevant metrics
        # CLV_PCH_PRE: Chain linked volumes, percentage change on previous period
        # NOTE include the metric below when starting to expand to another countries
        #   CP_MPPS_EU27_2020: Current prices, million purchasing power standard (EU27_2020)
        df = df[df["unit"] == "CLV_PCH_PRE"]
        
        # Keep samples with "na_item" attribute with values representing relevant metrics
        # B1GQ: Gross domestic product at market prices
        # P31_S14: Final consumption expenditure of household
        df = df[df["na_item"].isin(["B1GQ", "P31_S14"])]
        
        # Remove empty columns
        df = df.dropna(axis=1, how="all")
        
        # Convert "TIME_PERIOD" column to string type to avoid issues when applying the function "transform_data_to_range"
        df["TIME_PERIOD"] = df["TIME_PERIOD"].astype("string")      

        # Create "date_start" and "date_end" columns from column "TIME_PERIOD"
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