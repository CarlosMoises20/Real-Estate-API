
import duckdb
from backend.data.ingestion.source.base_data_source import BaseDataSource
from abc import abstractmethod

class BaseDuckDBDataSource(BaseDataSource):
    
    """Constructor for the BaseDuckDBDataSource class, which initializes the DuckDB
    connection and the datasets format"""
    def __init__(self, datasets_format=None, connection=None):
        super().__init__(datasets_format=datasets_format)
        self._connection = duckdb.connect() if not connection else connection
    
    
    """Abstract method used by subclasses to setup the environment before fetching data from the source, using the DuckDB connection"""
    @abstractmethod
    def _initial_setup(self):
        """..."""