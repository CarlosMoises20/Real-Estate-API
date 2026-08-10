import pandas as pd
import re
from pathlib import Path
from sklearn.model_selection import train_test_split
from app.constants import ATTR_MAPPING, COLUMN_ORDER


"""
Prepare the data by reading CSV files, renaming columns, concatenating dataframes, and removing duplicates.

Args:
    datasets_path (str): Path to the folder containing the CSV files.
    final_filename (str): Name of the final CSV file to be generated.

Returns:
    df_final (pd.DataFrame): The final prepared dataframe.
    
"""
def prepare_data(datasets_path="backend/datasets", final_filename="real_estate_data_final_v1.csv", 
                 old_filenames=["real_estate_data_final.csv"]):
    
    # Define the folder containing the CSV files
    folder = Path(datasets_path)

    # Include all CSV files in the folder except the final file to be generated
    csv_files = [file for file in folder.glob("*.csv") if file.name not in old_filenames]

    # Read CSV files as a Pandas dataframe each
    df_list = [pd.read_csv(file).rename(columns=ATTR_MAPPING) for file in csv_files]

    # Concatenate the dataframes 
    df_final = pd.concat(df_list, ignore_index=True)

    # Remove duplicates and irrelevant attributes
    df_final = df_final.drop_duplicates() \
                       .drop(columns=["Index", "Unnamed: 0", "id", "advertiser", 
                                      "views", "clicks", "Sealed", "category"])
                   
    # Create a new column "Id" with unique values starting from 1             
    df_final.insert(0, "Id", range(1, len(df_final) + 1))
    
    # TODO: Finish to convert categorical attributes to numerical values
        # Feature Engineering: The "title" attribute is a categorical attribute so it should
        # be split into multiple numerical attributes, one for each unique value of the "title" attribute.
    
        # TODO: "title" follows this pattern: "<property_type> T<number_of_rooms> em <location>", so we can extract these substrings 
        # and associate to the existing attributes:
            # Type: the substring before "T"
            # NumberOfBedrooms: the substring between "T" and "em"
            # Region, Location: the substring after "em"
      
    # Extract numeric values from attributes with values on string format but that should be numeric      
    for attr_name in ["GrossArea (m2)", "Terrain Area (m2)", "Useful Area (m2)", 
                      "Living Area (m2)", "Raw Construction Area (m2)",
                      "Area (m2)", "Total Area (m2)"]:
        
        # Extract the integer from the string
        df_final[attr_name] = df_final[attr_name].astype(str)
        df_final[attr_name] = df_final[attr_name].str.extract(r'(\d+(?:\.\d+)?)')
        df_final[attr_name] = pd.to_numeric(df_final[attr_name], errors='coerce')
        
        
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