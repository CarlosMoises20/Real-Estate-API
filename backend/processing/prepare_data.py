
import pandas as pd
from backend.common.constants import COLUMN_RENAME_MAP, CATEGORICAL_COLUMNS
from backend.data.ingestion.aggregation.data_aggregation import aggregate_external_data, aggregate_internal_data
from backend.common.utils import generate_dataset_from_df


"""
Prepare the internal data by reading CSV files, renaming columns, concatenating dataframes, and removing duplicates.

Args:
    datasets_path (str): Path to the folder containing the CSV files.

Returns:
    df_internal (pd.DataFrame): The final prepared dataframe.
    
"""
def prepare_internal_data(datasets_format):
    
    # TODO finish this
    
    df_returned_list = aggregate_internal_data(datasets_format=datasets_format, 
                                               internal_datasets_path="backend/datasets/internal")
    
    df_list = [df.rename(columns=COLUMN_RENAME_MAP) for df in df_returned_list]

    # Concatenate the dataframes 
    df_internal = pd.concat(df_list, ignore_index=True)

    # Remove duplicated entries and irrelevant attributes
    df_internal = df_internal.drop_duplicates()
    
    # Convert all boolean attributes to integer
    df_internal = df_internal.map(lambda x: int(x) if isinstance(x, bool) else x)
    
    # Dummy Coding to encode categorical attributes
    df_internal = pd.get_dummies(data=df_internal, columns=CATEGORICAL_COLUMNS, dtype=int)
    
    # Convert "PublishDate" column to datetime and extract year, month and day to have only numeric attributes
    df_internal["PublishDate"] = pd.to_datetime(
        df_internal["PublishDate"],
        errors="coerce"
    )
    
    df_internal["PublishYear"] = df_internal["PublishDate"].dt.year
    df_internal["PublishMonth"] = df_internal["PublishDate"].dt.month
    df_internal["PublishDay"] = df_internal["PublishDate"].dt.day
    
    df_internal = df_internal.drop(columns=["PublishDate", "EnergyEfficiencyLevel"])
    
    # for some negative values, transform those into positive values by applying the absolute value
    for attr_name in ["Living Area (m2)", "Total Area (m2)", "Built Area (m2)",
                      "NumberOfBathrooms", "NumberOfWC"]:
        
        df_internal[attr_name] = df_internal[attr_name].abs()
    
    # Split the data into training and testing sets (Train-Test Split)
    return df_internal


"""
Prepare the external data by reading CSV files, renaming columns, concatenating dataframes, and removing duplicates.

Args:
    datasets_path (str): Path to the folder containing the CSV files.

Returns:
    df_external (pd.DataFrame): The final prepared dataframe.
    
"""
def prepare_external_data(datasets_format):
    
    df_dict = aggregate_external_data(datasets_format=datasets_format)
    
    for df_name, df in df_dict.items():
        
        df_dict[df_name] = df.drop_duplicates()
    
    return df_dict


# Join internal and external datasets, using the appropriate keys in the join method
def join_internal_and_external_data(df_internal, df_external_list_dict):
    
    df_final = df_internal
    
    ##### TODO join each attribute from external datasets with 'df_internal', using temporal features (date_start, date_end, country_code, etc)
    
    ## TODO GDP (Eurostat)
    
    df_gdp = df_external_list_dict["Eurostat GDP"]
    
    df_gdp_market_prices = df_gdp[df_gdp["na_item"] == "B1GQ"]
    
    df_gdp_final_consumption = df_gdp[df_gdp["na_item"] == "P31_S14"]
    
    # Join the GDP data with the internal dataset using the "date_start" and "date_end" columns
    # TODO review this and fix if necessary; the join should be done using the "date_start" and "date_end" columns, but the internal dataset may not have these columns, so we need to ensure that the join is done correctly
    df_final = pd.merge(df_final, df_gdp_market_prices, on=["date_start", "date_end"])  
    df_final = pd.merge(df_final, df_gdp_final_consumption, on=["date_start", "date_end"])
    
    
    # TODO unemployment rate (INE)
    
    df_unemployment = df_external_list_dict["INE (Unemployment rate (%))"]
    
    # TODO housing sold (INE); join using "date_start" and "date_end"
    
    df_housing_sold = df_external_list_dict["INE (Housing sold)"]
    
    # TODO housing price per m2
    
    # TODO inflation (INE)
    
    df_inflation = df_external_list_dict["INE (Inflation - Monthly variation)"]
    
    
    # TODO unemployment rate (INE)
    
    df_unemployment = df_external_list_dict["INE (Unemployment rate (%))"]
    
    # TODO housing sold (INE); join using "date_start" and "date_end"
    
    df_housing_sold = df_external_list_dict["INE (Housing sold)"]
    
    # TODO housing price per m2
    
    df_housing_price = df_external_list_dict["INE (Housing price per square meter, euros)"]
    
    # TODO population
    
    df_population = df_external_list_dict["INE (Population)"]
    
    # TODO INE (housing credit rate)
    
    # TODO INE (gross disposable income)
    
    # TODO INE (average salary)
    
    
    
    # TODO FSQ (geospatial data)
    
    # TODO Geoapify (geospatial data)
    
    # TODO RASI (criminal data)
    
    
    return df_final


def prepare_final_data(df_final, datasets_format, final_filename="real_estate_internal_data_final"):
        
    # Reorder the columns in the desired order for the final dataframe 
    # Standard column order for the final dataset.
    # Keeping a fixed order makes the resulting dataset easier to inspect,
    # process, and use consistently throughout the machine learning pipeline.
    COLUMN_ORDER = [
        # Property type
        *sorted(col for col in df_final.columns if col.startswith("Type_")),

        # Location
        *sorted(col for col in df_final.columns if col.startswith("District_")),
        *sorted(col for col in df_final.columns if col.startswith("City_")),
        *sorted(col for col in df_final.columns if col.startswith("Town_")),

        # Property characteristics
        "NumberOfBedrooms", "NumberOfBathrooms", "NumberOfWC", "TotalRooms",

        # Areas
        "Built Area (m2)", "Living Area (m2)", "Total Area (m2)", "LotSize",

        # Building characteristics
        *sorted(col for col in df_final.columns if col.startswith("Floor_")),
        "Elevator", "Garage", "ConstructionYear", "Parking",

        # Energy
        *sorted(col for col in df_final.columns if col.startswith("EnergyCertificate_")),
        "ElectricCarsCharging",

        # Conservation
        *sorted(col for col in df_final.columns if col.startswith("ConservationStatus_")),

        # Publication date
        "PublishYear", "PublishMonth", "PublishDay",

        # Target
        "Price (euros)"
    ]
    
    df_final = df_final[COLUMN_ORDER]
    
    # Save the final dataframe in the format indicated by 'datasets_format' (CSV or Parquet)            
    generate_dataset_from_df(df=df_final, 
                             file_path_base=f"backend/datasets/{final_filename}",
                             dataset_format=datasets_format)
    
    return df_final



def prepare_data(datasets_format="parquet"):
    
    df_internal = prepare_internal_data(datasets_format=datasets_format)
    
    df_external_list_dict = prepare_external_data(datasets_format=datasets_format)
    
    # TODO concatenate internal dataset with external dataset through join; join_internal_and_external_data
    df_final = join_internal_and_external_data(df_internal, df_external_list_dict)
    
    return prepare_final_data(df_final, datasets_format=datasets_format)


if __name__ == "__main__":
    
    df_final = prepare_data()