
import json
import pandas as pd
from io import StringIO
from backend.data.ingestion.source.api.base_api_data_source import BaseAPIDataSource
from backend.common.utils import generate_dataset_from_df, transform_data_to_range
from backend.common.dataset_names import get_ecb_dataset_name

"""
This class is used to retrieve relevant data from the API of European Central Bank (BCE)

"""
class EuropeanCentralBank(BaseAPIDataSource):
    
    """Constructor of ECB class, with the default parameters"""
    def __init__(self, datasets_format, datasets_path):
        
        super().__init__(
            url="https://data-api.ecb.europa.eu/service/data",
            params={
                "format": "csvdata",
            },
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            datasets_format=datasets_format, 
            datasets_path=datasets_path
        )
    
    
    """
    Retrieve CSV data from a specific dataset of the API of ECB
    
        cols: 
            List of columns to extract from the data (array of strings, each string is a column name)
        
        value_attr_old_name:
            Name of the column that contains the value of the data
        
        value_attr_name: 
            Name of the column that will be used to store the data
        
        flow_ref:
            Identifier of the ECB dataflow (dataset) containing the requested
            data. It determines the dataset from which the series is retrieved.
            It forms the first path segment after "/service/data/" in the URL.
            Examples: "MIR" (MFI interest rates), "QSA" (quarterly sector
            accounts).
        
        series_key:
            Dot-separated sequence of dimension codes that uniquely identifies
            a specific time series within the selected dataflow. The codes must
            follow the dimension order defined by that dataflow.
            It forms the path segment immediately after flow_ref in the URL.
            Examples:
                "M.PT.B.A2C.A.R.A.2250.EUR.N" for a Portuguese housing
                credit interest rate series in MIR.
                "A.N.PT.W0.S1M.S1._Z.B.B6G._Z._Z._Z.XDC._T.S.V.GY._T"
                for a Portuguese gross disposable income growth series in QSA.
                
                
    API URL structure:
        {base_url}/{flow_ref}/{series_key}?format=csvdata
    
    """
    def __extract_data_from_dataset(self, cols, value_attr_old_name, value_attr_name, flow_ref, series_key):
        
        base_url = self._url
        
        self._url = f"{self._url}/{flow_ref}/{series_key}"
        
        # StringIO is a module in Python that allows you to treat strings as file-like objects
        # This allows you to read a string as a file; as a result, when the resulting dataframe
        # is saved in a new file, the data will be written to the file with the appropriate format and encoding
        df = pd.read_csv(StringIO(super().get_source_data().text))
        
        self._url = base_url
        
        dataset_name = get_ecb_dataset_name(value_attr_name)
        
        dataset_path = f"{self._datasets_path}/{dataset_name}"
        
        # NOTE uncomment this if you want to save the data in raw format
        df.to_csv(f"{dataset_path}_v0.csv", index=False)
        
        # Remove irrelevant attributes from the dataset
        df = df[cols]
        
        df = df.rename(columns={value_attr_old_name: value_attr_name})
        
        # Convert "TIME_PERIOD" column to string type to avoid issues when applying the function 
        # "transform_data_to_range"
        df["TIME_PERIOD"] = df["TIME_PERIOD"].astype("string")      

        # Create "date_start" and "date_end" columns from column "TIME_PERIOD"
        df[["date_start", "date_end"]] = pd.DataFrame(
            df["TIME_PERIOD"].apply(transform_data_to_range).tolist(),
            index=df.index
        )
        
        # Remove "TIME_PERIOD" column after applying the data transformation and 
        # saving it in "date_start" and "date_end"
        df = df.drop(columns=["TIME_PERIOD"])
        
        # Remove duplicated entries from the dataset
        df = df.drop_duplicates()
        
        # Save final dataset
        generate_dataset_from_df(df=df, 
                                 file_path_base=dataset_path, 
                                 dataset_format=self._datasets_format)
        
        
    """Retrieve CSV data from the API of ECB and return dataframe with relevant data"""
    def get_api_data(self):
        
        # Gross disposable income (Growth Rate)
        # Annual, Portugal, gross disposable income (B6G), growth rate over one year (GY).
        self.__extract_data_from_dataset(cols=["TIME_PERIOD", "OBS_VALUE", "OBS_STATUS"],
                                         value_attr_old_name="OBS_VALUE",
                                         value_attr_name="gross_disposable_income_growth_rate",
                                         flow_ref="MIR",
                                         series_key="M.PT.B.A2C.A.R.A.2250.EUR.N")
        
        # Housing credit rate
        # Monthly, Portugal, loans to households for house purchase, new business.
        self.__extract_data_from_dataset(cols=["TIME_PERIOD", "OBS_VALUE"],
                                        value_attr_old_name="OBS_VALUE",
                                        value_attr_name="housing_credit_rate",
                                        flow_ref="QSA",
                                        series_key="A.N.PT.W0.S1M.S1._Z.B.B6G._Z._Z._Z.XDC._T.S.V.GY._T")
        