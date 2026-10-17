
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from backend.data.ingestion.source.api.eurostat import Eurostat
from backend.data.ingestion.source.duckdb.fsq_os_places import FSQOSPlaces
from backend.data.ingestion.source.api.idealista import Idealista
import kagglehub, pycountry
from backend.common.utils import generate_df_from_dataset
from backend.common.constants import DATASETS_PATH_BASE


"""
This is the abstract class used to aggregate relevant data from
a specific country, including data from external sources and internal sources

"""
class BaseCountryDataProcessor(ABC):
    
    """
    Base constructor for the BaseCountryDataProcessor class, 
    which initializes the datasets format ("csv" or "parquet")
    
    """
    def __init__(self, datasets_format, country_code=None):
        
        self._datasets_format = datasets_format
        self._country_code = country_code
        
        # NOTE you need to create a .env file in the compose folder with the variables indicated in the README file
        # TODO try to find a better place to put this code line
        load_dotenv(dotenv_path="./compose/.env")
        
        
    """
    Get the path to the internal datasets for the specific country
        data_type: must be "internal", "external" or "final"
        returns: the path to the internal datasets
        
    """
    def _get_datasets_path(self, data_type):
        
        if data_type not in ["internal", "external", "final"]:
            raise ValueError("data_type must be 'internal', 'external' or 'final'")
        
        return f"{DATASETS_PATH_BASE}/{self._get_country_name().lower().replace(' ', '_')}/{data_type}" 
    
    """
    Generic method to update data from the Eurostat API
    
    """
    def _update_eurostat(self, time_period):
        Eurostat(
            datasets_format=self._datasets_format,
            datasets_path=self._get_datasets_path(data_type="external")
        ).get_api_data(country_code=self._get_country_code(), 
                       time_period=time_period)
        
    
    """
    Generic method to update data from Idealista
    
        TODO review this after implementing Idealista API
        
    """
    """def _update_idealista(self, ...):
        Idealista(
            datasets_format=self._datasets_format,
            datasets_path=self._get_datasets_path(data_type="external")
        ).get_api_data(...)"""
        
    
    """Generic method to update data from the FSQ OS Places API"""
    def _update_fsq_places(self):
        FSQOSPlaces(
            datasets_format=self._datasets_format,
            datasets_path=self._get_datasets_path(data_type="external")
        ).get_source_data(country_code=self._get_country_code())


    """Generic method to update data from Kaggle"""
    def _download_kaggle(self, handle, filename, data_type):
        kagglehub.dataset_download(
            handle=handle, 
            path=filename, 
            force_download=True,
            output_dir=self._get_datasets_path(data_type)
        )


    """Generic method to generate a pandas dataframe from a dataset"""
    def _read_dataset(self, name, data_type):
        return generate_df_from_dataset(
            file_path_base=f"{self._get_datasets_path(data_type)}/{name}",
            dataset_format=self._datasets_format
        )
    
                  
    """
    Generic method to get the country code corresponding 
    to the subclass of BaseCountryDataProcessor
    
    """    
    def _get_country_code(self):
        return self._country_code
    
    
    """Generic method to get the country name based on the country code (2-letter format always)"""
    def _get_country_name(self):
        return pycountry.countries.get(alpha_2=self._get_country_code()).name
    
    
    """
    Abstract method to update the datasets for the specific country, 
    by aggregating data from external and internal sources
    
    """
    @abstractmethod
    def update_datasets(self):
        """..."""
    
    
    """
    Abstract method to aggregate data from APIs with external data (such as inflation,
    average salary, unemployment rate, etc.)
    
    """
    @abstractmethod
    def _aggregate_external_data(self):
        """..."""
    
    
    """
    Abstract method to aggregate data from APIs with internal data (such as number of 
    bedrooms, bathrooms, gross area, type of property, etc.)
    
    """
    @abstractmethod
    def _aggregate_internal_data(self):
        """..."""
    
    
    """
    Abstract method to join and save data in a final dataset representing the specific country's 
    real estate market data
    
    """
    @abstractmethod
    def join_and_save_data(self):
        """..."""