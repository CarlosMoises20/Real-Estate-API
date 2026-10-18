
from backend.data.ingestion.source.api.base_api_data_source import BaseAPIDataSource
import pandas as pd
from io import StringIO
from backend.common.utils import generate_dataset_from_df, transform_data_to_range
from backend.common.dataset_names import get_eurostat_dataset_name


"""This class is used to retrieve relevant data from the API of Eurostat"""
class Eurostat(BaseAPIDataSource):

    """Constructor of Eurostat class, with the default parameters"""
    def __init__(self, datasets_format, datasets_path):
        
        super().__init__(
            url="https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/",
            params={
                "format": "csvdata",
                "formatVersion": "2.0",
                "compress": "false"      
            },
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            datasets_format=datasets_format, 
            datasets_path=datasets_path
        )

    
    """
    Retrieve JSON data from the API of INE and return dataframe with relevant data
    
    Parameters:
        - country_code: A country code or list of country codes for which to retrieve data 
                        (e.g., "PT,ES" for Portugal and Spain or "PT" for Portugal only)
        
        - time_period: The time period for which to retrieve data. Examples:
            "ge:2010" for data from 2010 to the current year
            "eq:2020" for data from 2020 only
            "gt:2015" for data from 2015 onwards (greater than 2015)
            "lt:2018" for data until 2018 (less than 2018)
            "ge:2010,lt:2018" for data from 2010 to 2018
            
        - dataset_code: The dataset code for the specific data to retrieve (e.g., "nama_10_gdp" for GDP data)
    
    Source: https://ec.europa.eu/eurostat/fr/web/user-guides/data-browser/api-data-access/api-getting-started/sdmx3.0
    
    """
    def __extract_data_from_dataset(self, country_code, time_period, dataset_code, unit_list, na_item_list):
        
        self._params["c[GEO]"] = country_code
        
        self._params["c[TIME_PERIOD]"] = time_period
        
        url_base = self._url
                
        self._url += f"{dataset_code}/1.0"
        
        # StringIO is a module in Python that allows you to treat strings as file-like objects
        # This allows you to read a string as a file; as a result, when the resulting dataframe
        # is saved in a new file, the data will be written to the file with the appropriate format and encoding
        df = pd.read_csv(StringIO(super().get_source_data().text))
        
        self._url = url_base
        
        # In case of multiple country codes, whose names are separated by commas, replace commas with underscores
        # since this will be used for the dataset name
        if "," in country_code:
            country_code = country_code.replace(",", "_")
        
        dataset_path = f"{self._datasets_path}/{get_eurostat_dataset_name(dataset_code, country_code, time_period)}"
        
        # NOTE uncomment if you want to generate CSV with the dataframe before pre-processing
        #df.to_csv(f"{dataset_path}_v0.csv", index=False)
        
        if "CONF_STATUS" in df.columns:
        
            # Remove samples where confidential status is C (confidential), N (not for publication) or P (information under non-statistical secrecy arrangements)
            # since this means that the information cannot be published in another API
            df = df[~df["CONF_STATUS"].isin(["C", "N", "P"])]
        
        # Keep samples with "unit" attribute with values representing relevant metrics
        if "unit" in df.columns:
        
            # CLV_PCH_PRE: Chain linked volumes, percentage change on previous period
            df = df[df["unit"].isin(unit_list)]
        
        # Keep samples with "na_item" attribute with values representing relevant metrics
        if "na_item" in df.columns:
        
            # B1GQ: Gross domestic product at market prices
            # P31_S14: Final consumption expenditure of household
            df = df[df["na_item"].isin(na_item_list)]
        
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
        # Remove "TIME_PERIOD" column after applying the data transformation and 
        # saving it in "date_start" and "date_end"
        df = df.drop(columns=["STRUCTURE", "STRUCTURE_ID", "freq", 
                              "TIME_PERIOD", "OBS_FLAG", "s_adj", "geo"])
        
        # Remove duplicated entries from the dataset
        df = df.drop_duplicates()
        
        # Save final dataset            
        generate_dataset_from_df(df=df, 
                                file_path_base=dataset_path,
                                dataset_format=self._datasets_format)
        
        return df
        
        
        
    """
    Method to retrieve data from API from a specific country (country_code) and
    a period of time (time_period)
    
    Parameters:
    - country_code: A country code or list of country codes for which to retrieve data 
                    (e.g., "PT,ES" for Portugal and Spain or "PT" for Portugal only)
    
    - time_period: The time period for which to retrieve data. Examples:
        "ge:2010" for data from 2010 to the current year
        "eq:2020" for data from 2020 only
        "gt:2015" for data from 2015 onwards (greater than 2015)
        "lt:2018" for data until 2018 (less than 2018)
        "ge:2010,lt:2018" for data from 2010 to 2018
    
    
    """ 
    def get_api_data(self, country_code, time_period):
        
        # Gross domestic product and Final consumption expenditure of household
        self.__extract_data_from_dataset(country_code=country_code, 
                                        time_period=time_period,
                                        dataset_code="namq_10_gdp",
                                        unit_list=["CLV_PCH_PRE"],
                                        na_item_list=["B1GQ", "P31_S14"])