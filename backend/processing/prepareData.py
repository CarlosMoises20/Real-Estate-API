import pandas as pd
from backend.common.constants import COLUMN_RENAME_MAP, CATEGORICAL_COLUMNS
from backend.data.ingestion.scraping.data_scraping import aggregate_external_data, aggregate_internal_data


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
def join_internal_and_external_data(df_internal, df_external):
    
    # TODO join each attribute from external datasets with 'df_internal'
    
        # TODO inflation (INE)
        
        # TODO unemployment rate (INE)
        
        # TODO housing sold (INE)
        
        # TODO housing price per m2
        
        # TODO housing credit rate
        
        # TODO gross disposable income
        
        # TODO average salary
        
        # TODO GDP (Eurostat)
        
        # TODO FSQ (geospatial data)
        
        # TODO Geoapify (geospatial data)
        
        # TODO RASI (criminal data)
    
    
    pass
    


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
    
    # Save the final dataframe if the flag 'datasets_format' is provided
    # If the flag is None, no dataset will be generated
    if datasets_format:
        
        file_path = f"backend/datasets/{final_filename}.{datasets_format}"
        
        if datasets_format == "csv":
            df_final.to_csv(file_path, index=False)
        
        elif datasets_format == "parquet":
            df_final.to_parquet(file_path, index=False)
    
    return df_final



def prepare_data(datasets_format="parquet"):
    
    df_internal = prepare_internal_data(datasets_format=datasets_format)
    
    df_external = prepare_external_data(datasets_format=datasets_format)
    
    # TODO concatenate internal dataset with external dataset through join; join_internal_and_external_data
    df_final = join_internal_and_external_data(df_internal, df_external)
    
    return prepare_final_data(df_final, datasets_format=datasets_format)


if __name__ == "__main__":
    
    df_final = prepare_data()