

import time

import duckdb
from backend.data.ingestion.source.base_data_source import BaseDataSource
from abc import abstractmethod

class BaseDuckDBDataSource(BaseDataSource):
    
    # TODO complete this class
    
    """Constructor for the BaseDuckDBDataSource class, which initializes the DuckDB
    connection and the datasets format"""
    def __init__(self, datasets_format=None, connection=None):
        super().__init__(datasets_format=datasets_format)
        self._connection = duckdb.connect() if not connection else connection
    
    
    """Abstract method used by subclasses to setup the environment before fetching data from the source, using the DuckDB connection"""
    @abstractmethod
    def _initial_setup(self):
        """..."""
    
    
    """Abstract method used by subclasses to build the query to retrieve relevant data from the source"""
    @abstractmethod
    def _build_fetch_query(self, **kwargs):
        """..."""        
    
    """
    Method to retrieve data from an indicated source, using the DuckDB
    connection and the query built in the _setup_and_build_query method
    It includes retried
    """
    def _execute_query_with_retries(self, query, retries=3):
        for attempt in range(retries):
            try:
                return self._connection.execute(query)
            except duckdb.HTTPException:
                if attempt == retries - 1:
                    raise
                wait = 2 ** attempt
                print(f"HTTP request failed. Attempt in {wait}s...")
                time.sleep(wait)

    """Run a query with indicated parameters and return the result"""            
    def _fetch(self, **kwargs):
        return self._execute_query_with_retries(self._build_fetch_query(**kwargs))