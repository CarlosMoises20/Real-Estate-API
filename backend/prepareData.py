import pandas as pd
import re
from pathlib import Path
from sklearn.model_selection import train_test_split
from app.constants import COLUMN_RENAME_MAP, COLUMN_ORDER


"""
Prepare the data by reading CSV files, renaming columns, concatenating dataframes, and removing duplicates.

Args:
    datasets_path (str): Path to the folder containing the CSV files.
    final_filename (str): Name of the final CSV file to be generated.

Returns:
    df_final (pd.DataFrame): The final prepared dataframe.
    
"""
def prepare_data(datasets_path="backend/datasets", final_filename="real_estate_data_final.csv", 
                 old_filenames=["real_estate_data_final.csv", 
                                "real_estate_data_final_v0.csv"]):
    
    # Define the folder containing the CSV files
    folder = Path(datasets_path)

    # Include all CSV files in the specified folder, except for the final output file.
    # This approach has the advantage of supporting multiple datasets being stored in "datasets_path",
    # which will be useful in the future if more datasets are added to the folder to train / test the models
    csv_files = [file for file in folder.glob("*.csv") if file.name not in old_filenames]

    # Read CSV files as a Pandas dataframe each
    df_list = [pd.read_csv(file).rename(columns=COLUMN_RENAME_MAP) for file in csv_files]

    # Concatenate the dataframes 
    df_final = pd.concat(df_list, ignore_index=True)

    # Remove duplicated entries and irrelevant attributes
    df_final = df_final.drop_duplicates()
    
    # TODO: Finish to convert categorical attributes to numerical values (Dummy Coding?)
        
    # Convert all boolean attributes to integer
    df_final = df_final.map(lambda x: int(x) if isinstance(x, bool) else x)

    # TODO: Remove outliers (examples with abnormal price / area values)
    
    # TODO: Normalize the data (Min-Max Scaling or Standardization)
    
    # TODO: Handle missing values (Imputation or Removal)
    
    # TODO: Feature Reduction (PCA, LDA, etc.)
    
    # TODO: Bias mitigation (if necessary)
    
    # Sort the dataset attributes for better interpretability while visualizing the dataset
    df_final = df_final[COLUMN_ORDER]
    
    # Save the final dataframe as a CSV file
    df_final.to_csv(f"backend/datasets/{final_filename}", index=False)
    
    # Split the data into training and testing sets (Train-Test Split)
    return train_test_split(df_final, test_size=0.2, random_state=42)


if __name__ == "__main__":
    df_train, df_test = prepare_data()