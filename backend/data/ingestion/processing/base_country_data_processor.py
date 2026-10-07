
from abc import ABC, abstractmethod

"""
This is the abstract class used to aggregate relevant data from
a specific country, including data from external sources and internal sources

"""
class BaseCountryDataProcessor(ABC):
    
    """Base constructor for the BaseCountryDataProcessor class, which initializes the datasets format ("csv" or "parquet")"""
    def __init__(self, datasets_format):
        self._datasets_format = datasets_format
        
        
    """Get the path to the internal datasets for the specific country"""
    def _get_internal_datasets_path(self):
        return f"./backend/datasets/{self._get_country_code()}/internal" 
    
    
    """Get the path to the external datasets for the specific country"""
    def _get_external_datasets_path(self):
            return f"./backend/datasets/{self._get_country_code()}/external" 
    
    
    """Update the datasets for the specific country, by aggregating data from external and internal sources"""
    def update_datasets(self):
        """..."""
    
    """Aggregate data from external sources"""
    @abstractmethod
    def _aggregate_external_data(self):
        """..."""
    
    
    """Aggregate data from internal sources"""
    @abstractmethod
    def _aggregate_internal_data(self):
        """..."""
    
        
    @abstractmethod
    def _get_country_code(self):
        """..."""
    
        
    @abstractmethod
    def join_and_save_data(self):
        """..."""