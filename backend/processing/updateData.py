

import os, kagglehub
from dotenv import load_dotenv
from backend.data.ingestion.source.duckdb.fsq_os_places import FSQOSPlaces
from backend.data.ingestion.source.api.eurostat import Eurostat
from backend.data.ingestion.source.api.ine import INE
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


def update_datasets(datasets_format="parquet", 
                    external_datasets_path="./backend/datasets/external/", 
                    internal_datasets_path="./backend/datasets/internal/"):

    # Download CSV Kaggle dataset from the link
    # https://www.kaggle.com/datasets/luvathoms/portugal-real-estate-2024
    kagglehub.dataset_download(handle="luvathoms/portugal-real-estate-2024", 
                                path="portugal_listinigs.csv",
                                force_download=True, 
                                output_dir=internal_datasets_path)

    ine = INE(
        url="https://www.ine.pt/ine/json_indicador/pindica.jsp", 
        headers={
                "User-Agent": "Mozilla/5.0",
                "Content-Type": "application/json"
            },
        datasets_format=datasets_format,
        datasets_path=external_datasets_path
    )
    
    
    ine.get_api_data()
    
    
    # API Reference: https://ec.europa.eu/eurostat/web/user-guides/data-browser/api-data-access/api-detailed-guidelines/api-statistics
    # SMDX-2.0 CSV
    # get GDP per capita data from Eurostat API (from 2010 to current year)
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
        datasets_format=datasets_format,
        datasets_path=external_datasets_path    
    )
    
    # Portugal data
    # From 2010 to current year
    eurostat.get_api_data(country_code="PT", 
                          time_period="ge:2010",
                          dataset_code="nama_10_gdp")
    
    
    # NOTE you need to create a .env file in the compose folder with the variable GEOAPIFY_API_KEY={your_api_key_here}
    load_dotenv(dotenv_path="./compose/.env")

    
    # Foursquare OS Places API Reference: https://docs.foursquare.com/data-products/docs/fsq-places-open-source
    fsq_os_places = FSQOSPlaces(
        datasets_format=datasets_format,
        access_token=os.getenv("FSQ_OS_PLACES_ACCESS_TOKEN"),
        db_file_path="./backend/data/duckdb_source/fsq/fsq_os_places.db",
        datasets_path=external_datasets_path
    )
    
    fsq_os_places.update_data(country_code="PT")
    
    
    
# This script is executed once per day 
# to update the data (including local datasets) to be consumed by the API
if __name__ == "__main__":
    
    # PARQUET format is more efficient for large datasets, 
    # but CSV format is more compatible with other tools and easier to read and edit manually
    
    # CSV format
    update_datasets(datasets_format="csv")
    
    # PARQUET format
    update_datasets() 
    
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