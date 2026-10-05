
from abc import ABC, abstractmethod


"""
This is the abstract class used to retrieve relevant data from a specific API

This includes the url, parameters and headers
It also includes the method get_source_data, which will be used by all the subclasses representing 
each one a different API, to get the data from the API through the indicated URL, and using the optionally
indicated parameters and headers

"""
class BaseDataSource(ABC):
    
    """Base constructor for the BaseDataSource class, which initializes the datasets format ("csv" or "parquet")"""
    def __init__(self, datasets_format, datasets_path):
        self._datasets_format = datasets_format
        self._datasets_path = datasets_path
    
    """Retrieve data from an indicated source, depending on the source type"""
    @abstractmethod
    def get_source_data(self):
        """..."""
    
    