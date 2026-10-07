
import pandas as pd
from backend.common.utils import generate_df_from_dataset
import os, kagglehub
from dotenv import load_dotenv
from backend.data.ingestion.source.duckdb.fsq_os_places import FSQOSPlaces
from backend.data.ingestion.source.api.eurostat import Eurostat
from backend.data.ingestion.source.api.ine import INE
from backend.data.ingestion.processing.base_country_data_processor import BaseCountryDataProcessor
from backend.data.ingestion.source.duckdb.fsq_os_places import FSQOSPlaces



class PortugalDataProcessor(BaseCountryDataProcessor):
    
    def __init__(self, datasets_format="parquet"):
        
        super().__init__(datasets_format=datasets_format)
        
        self.__country_code = "PT"
        


    def _get_country_code(self):
        return self.__country_code



    def _aggregate_external_data(self):
        
        ### Eurostat GDP dataset (with data related to GDP per capita in Portugal from 2010 to current year)
        df_eurostat_pt = generate_df_from_dataset(
            file_path_base=f"{self._get_external_datasets_path()}/eurostat_gdp_pt_data_ge_2010", 
            dataset_format=self._datasets_format
        )
        
        ### RASI dataset (with data related to criminal records from 2024 and 2025)
        df_rasi = generate_df_from_dataset(
            file_path_base=f"{self._get_external_datasets_path()}/rasi_data_2024_2025", 
            dataset_format=self._datasets_format
        )
        
        ### FSQ Places
        fsq_os_places = FSQOSPlaces(
            datasets_format=self._datasets_format,
            access_token=os.getenv("FSQ_OS_PLACES_ACCESS_TOKEN"),
            db_file_path="./backend/data/duckdb_source/fsq/fsq_os_places.db",
            datasets_path=self._get_external_datasets_path()
        )
        
        df_fsq_os_places = fsq_os_places.get_source_data(country_code=self._get_country_code())
        
        ### INE data related to average salary in Portugal
        df_ine_avg_salary = generate_df_from_dataset(
            file_path_base=f"{self._get_external_datasets_path()}/ine_data_avg_salary_euros",
            dataset_format=self._datasets_format
        )
        
        ### INE data related to inflation (homologous variation) in Portugal
        df_ine_inflation_homologous_variable = generate_df_from_dataset(
            file_path_base=f"{self._get_external_datasets_path()}/ine_data_inflation_homologous_variable",
            dataset_format=self._datasets_format
        )
        
        ### INE data related to housing credit rate in Portugal
        df_ine_housing_credit_rate = generate_df_from_dataset(
            file_path_base=f"{self._get_external_datasets_path()}/ine_data_housing_credit_rate",
            dataset_format=self._datasets_format
        )
        
        ### INE data related to unemployment rate in Portugal   
        df_ine_unemployment_rate = generate_df_from_dataset(
            file_path_base=f"{self._get_external_datasets_path()}/ine_data_unemployment_rate",
            dataset_format=self._datasets_format
        )
        
        ### INE data related to housing price per square meter (euros) in Portugal
        df_ine_housing_price_per_m2_euros = generate_df_from_dataset(
            file_path_base=f"{self._get_external_datasets_path()}/ine_data_housing_price_per_m2_euros",
            dataset_format=self._datasets_format
        )
        
        return {
            "INE (Average salary)": df_ine_avg_salary,
            "INE (Inflation - Homologous variation)": df_ine_inflation_homologous_variable,
            "INE (Housing credit rate)": df_ine_housing_credit_rate,
            "INE (Unemployment rate (%))": df_ine_unemployment_rate,
            "INE (Housing price per square meter, euros)": df_ine_housing_price_per_m2_euros,
            "Eurostat GDP": df_eurostat_pt,
            "FSQ Places": df_fsq_os_places,
            "RASI Criminal Record": df_rasi
        }
        

        
    def _aggregate_internal_data(self):
        
        # Read CSV Kaggle dataset from the local datasets
        df_kaggle = pd.read_csv(f"{self._get_internal_datasets_path()}/portugal_listinigs.csv", sep=",", encoding="utf-8")
        
        # TODO aggregate data from Idealista

        return {
                "Kaggle": df_kaggle
            }
        
        
        
    def update_datasets(self):

        # Download CSV Kaggle dataset from the link
        # https://www.kaggle.com/datasets/luvathoms/portugal-real-estate-2024
        kagglehub.dataset_download(handle="luvathoms/portugal-real-estate-2024", 
                                    path="portugal_listinigs.csv",
                                    force_download=True, 
                                    output_dir=self._get_internal_datasets_path())

        ine = INE(
            url="https://www.ine.pt/ine/json_indicador/pindica.jsp", 
            headers={
                    "User-Agent": "Mozilla/5.0",
                    "Content-Type": "application/json"
                },
            datasets_format=self._datasets_format,
            datasets_path=self._get_external_datasets_path()
        )
        
        
        ine.get_api_data()
        
        
        # API Reference: https://ec.europa.eu/eurostat/web/user-guides/data-browser/api-data-access/api-detailed-guidelines/api-statistics
        # SMDX-2.0 CSV
        eurostat = Eurostat(
            url="https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/",
            params={
                "format": "csvdata",
                "formatVersion": "2.0",
                "compress": "false"      
            },
            headers={
                    "User-Agent": "Mozilla/5.0",
                    "Content-Type": "application/json"
                },
            datasets_format=self._datasets_format,
            datasets_path=self._get_external_datasets_path()    
        )
        
        # Portugal data
        # From 2010 to current year
        eurostat.get_api_data(country_code_list=self._get_country_code(), 
                              time_period="ge:2010", 
                              dataset_code="nama_10_gdp")
        
        
        # NOTE you need to create a .env file in the compose folder with the variable GEOAPIFY_API_KEY={your_api_key_here}
        load_dotenv(dotenv_path="./compose/.env")

        
        # Foursquare OS Places API Reference: https://docs.foursquare.com/data-products/docs/fsq-places-open-source
        fsq_os_places = FSQOSPlaces(
            datasets_format=self._datasets_format,
            access_token=os.getenv("FSQ_OS_PLACES_ACCESS_TOKEN"),
            db_file_path="./backend/data/duckdb_source/fsq/fsq_os_places.db",
            datasets_path=self._get_external_datasets_path()
        )
        
        fsq_os_places.update_data(country_code=self._get_country_code())
        
        
        
        
    def join_and_save_data(self):
        # Aggregate external data
        external_data = self._aggregate_external_data()
        
        # Aggregate internal data
        internal_data = self._aggregate_internal_data()
        
        # TODO join the datasets and save them to a final dataset to be consumed by the API
        
        
        
        
# This script is executed once per day 
# to update the data (including local datasets) to be consumed by the API
if __name__ == "__main__":
    
    pt = PortugalDataProcessor()
    
    # PARQUET format is more efficient for large datasets, 
    # but CSV format is more compatible with other tools and easier to read and edit manually
    
    # CSV format
    pt.update_datasets()
    
    pt.__setattr__("_datasets_format", "csv")
    
    # PARQUET format
    pt.update_datasets() 
    
    """scheduler = BackgroundScheduler()

    scheduler.add_job(
        update_datasets,
        CronTrigger(
            hour=3,
            minute=0,
            timezone="Europe/Lisbon",
        ),
        id="daily_dataset_update",
    )

    scheduler.start()

    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()"""