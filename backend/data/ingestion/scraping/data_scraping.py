
import pandas as pd
from backend.common.utils import generate_df_from_dataset

def aggregate_external_data(datasets_format="parquet", 
                            external_datasets_path="./backend/datasets/external"):
    
    # Eurostat GDP dataset (with data related to GDP per capita in Portugal from 2010 to current year)
    df_eurostat = generate_df_from_dataset(
        file_path_base=f"{external_datasets_path}/eurostat_gdp_data_since_2010", 
        dataset_format=datasets_format
    )
    
    # RASI dataset (with data related to criminal records from 2024 and 2025)
    df_rasi = generate_df_from_dataset(
        file_path_base=f"{external_datasets_path}/rasi_data_2024_2025", 
        dataset_format=datasets_format
    )
    
    # FSQ Places
    df_fsq = generate_df_from_dataset(
        file_path_base=f"{external_datasets_path}/fsq_os_places",
        dataset_format=datasets_format
    )
    
    # Geoapify dataset (with data related to facilities in Portugal)
    df_geoapify = generate_df_from_dataset(
        file_path_base=f"{external_datasets_path}/geoapify_data_facilities",
        dataset_format=datasets_format
    )
    
    # INE data related to average salary in Portugal
    df_ine_avg_salary = generate_df_from_dataset(
        file_path_base=f"{external_datasets_path}/ine_data_avg_salary_euros",
        dataset_format=datasets_format
    )
    
    # INE data related to inflation (homologous variation) in Portugal
    df_ine_inflation_homologous_variable = generate_df_from_dataset(
        file_path_base=f"{external_datasets_path}/ine_data_inflation_homologous_variable",
        dataset_format=datasets_format
    )
    
    # INE data related to housing credit rate in Portugal
    df_ine_housing_credit_rate = generate_df_from_dataset(
        file_path_base=f"{external_datasets_path}/ine_data_housing_credit_rate",
        dataset_format=datasets_format
    )
    
    # INE data related to unemployment rate in Portugal   
    df_ine_unemployment_rate = generate_df_from_dataset(
        file_path_base=f"{external_datasets_path}/ine_data_unemployment_rate",
        dataset_format=datasets_format
    )
    
    # INE data related to housing price per square meter (euros) in Portugal
    df_ine_housing_price_per_m2_euros = generate_df_from_dataset(
        file_path_base=f"{external_datasets_path}/ine_data_housing_price_per_m2_euros",
        dataset_format=datasets_format
    )
    
    return {
        "INE (Average salary)": df_ine_avg_salary,
        "INE (Inflation - Homologous variation)": df_ine_inflation_homologous_variable,
        "INE (Housing credit rate)": df_ine_housing_credit_rate,
        "INE (Unemployment rate (%))": df_ine_unemployment_rate,
        "INE (Housing price per square meter, euros)": df_ine_housing_price_per_m2_euros,
        "GDP": df_eurostat,
        "Geoapify Places": df_geoapify,
        "FSQ Places": df_fsq,
        "RASI Criminal Record": df_rasi
    }
    

    
    
    
    
def aggregate_internal_data(datasets_format="parquet", 
                            internal_datasets_path="./backend/datasets/internal/"):
    
    # Read CSV Kaggle dataset from the local datasets
    df_kaggle = pd.read_csv(f"{internal_datasets_path}/portugal_listinigs.csv", sep=",", encoding="utf-8")
    
    # TODO aggregate data from Idealista

    return {
            "Kaggle": df_kaggle
        }
    
    
# TODO remove this when no longer needed    
if __name__ == "__main__":
    
    df_internal_list = aggregate_internal_data()
    
    df_external_list = aggregate_external_data()