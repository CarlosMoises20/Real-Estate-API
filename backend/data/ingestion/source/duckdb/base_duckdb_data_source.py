
import duckdb, os
from pathlib import Path
from backend.data.ingestion.source.base_data_source import BaseDataSource
from abc import abstractmethod

"""
This is the abstract class used to retrieve relevant data from a specific DuckDB data source

"""
class BaseDuckDBDataSource(BaseDataSource):
    
    """
    Constructor for the BaseDuckDBDataSource class, which initializes the DuckDB
    connection and the datasets format
    
    """
    def __init__(self, datasets_format=None, datasets_path=None, connection=None):
        super().__init__(datasets_format=datasets_format,
                         datasets_path=datasets_path)
        self._connection = duckdb.connect() if not connection else connection
        
    
    """
    Method used to create the DuckDB connection through a database file
    whose path is specified in "db_file_path"
    If file does not exist, it will be created
    If directory does not exist, it will be created before the file being created inside ir
    
    """    
    def _create_connection_from_db_file(self, db_file_path):
        
        # Raise an exception if the database file path is not specified
        if not db_file_path:
            raise ValueError("Database file path must be specified")
        
        # Get parent directory
        parent_dir = Path(db_file_path).parent
        
        # Create the directory where the database file will be created if it does not exist
        if not os.path.exists(parent_dir):
            
            # Create parent directory if it does not exist
            parent_dir.mkdir(parents=True, exist_ok=True)
        
        # Create the DuckDB connection; this will create the database file if it does not exist, or open it if it already exists    
        return duckdb.connect(db_file_path)
            
    
    
    """Abstract method used by subclasses to setup the environment before fetching data from the source, using the DuckDB connection"""
    @abstractmethod
    def _initial_setup(self):
        """..."""
        
        
    """Abstract method used by subclasses to update data from the source, using the DuckDB connection"""
    @abstractmethod
    def update_data(self):
        """..."""