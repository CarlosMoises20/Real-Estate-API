import pandas as pd
from pathlib import Path


"""
Prepare the data by reading CSV files, renaming columns, concatenating dataframes, and removing duplicates.

Args:
    datasets_path (str): Path to the folder containing the CSV files.
    final_filename (str): Name of the final CSV file to be generated.

Returns:
    df_final (pd.DataFrame): The final prepared dataframe.
    
"""
def prepare_data(datasets_path="backend/datasets", final_filename="pt_real_estate_data_final.csv"):
    
    # Define the folder containing the CSV files
    folder = Path(datasets_path)

    # Include all CSV files in the folder except the final file to be generated
    csv_files = [file for file in folder.glob("*.csv") if file.name != final_filename]

    # TODO: finish to review this dictionary to map the columns names to the final ones, to remove redundancy of attributes after concatenation
    COLUMN_MAPPING = {
        "Location": ["location", "localization"],
        "Price": ["price", "price_int"],
        "GrossArea": ["gross_area", "area.gross", "area.land"],
        "Useful Area (m2)": ["Useful Area", "area.net", "useful_area"],
        "Latitude": ["latitude"],
        "Longitude": ["longitude"],
        "Living Area (m2)": ["LivingArea"],
        "NumberOfBedrooms": ["rooms"],
        "NumberOfWC": ["WC's"]
    }

    for file in csv_files:
        print(file.name)

    # Read CSV files as a Pandas dataframe each
    df_list = [pd.read_csv(file) for file in csv_files]

    # rename columns to remove attributes redundancy
    for df in df_list:
        for new_column_name, old_column_names in COLUMN_MAPPING.items():
            if new_column_name not in df.columns:
                for old_column_name in old_column_names:
                    if old_column_name in df.columns:
                        df.rename(columns={old_column_name: new_column_name}, inplace=True)
                        break

    # Concatenate the dataframes 
    df_final = pd.concat(df_list, ignore_index=True)

    print("Number of rows before removing duplicates:", len(df_final))
    print(df_final.columns.tolist())

    print("Number of duplicates to be removed:", df_final.duplicated().sum())

    duplicates = df_final.duplicated()

    # Print the number of duplicates found
    print(len(df_final.index[duplicates].tolist()))

    print("Number of rows before removing duplicates:", len(df_final))

    df_final = df_final.drop_duplicates() \
                        .drop(columns=["Index", "Unnamed: 0", "id"]) \
                                
    df_final.insert(0, "Id", range(1, len(df_final) + 1))

    df_final.to_csv(f"backend/datasets/real_dataset_files/{final_filename}", index=False)

    print("Final number of rows:", len(df_final))
    
    return df_final