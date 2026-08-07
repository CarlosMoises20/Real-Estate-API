import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split


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

    # this dictionary to map the columns names to the final ones, to remove redundancy of attributes after concatenation
    # the property is the old name of the attribute and the value is the new name of the attribute
    # this step is done because there are different datasets with attributes that represent the same thing but with different names
    # for example, some datasets have "price" and others "price_int", and in both cases, this represents the Price. The idea is that in both datasets,
    # these attributes will be renamed to an equal name (in this case "Price") so that when concatenating the datasets, there will be no redundancy of attributes.
    COLUMN_MAPPING = {
        
        # Location
        "location": "Location",
        "Localization": "Location",
        
        # Price
        "price": "Price (€)",
        "price_int": "Price (€)",
        "Price": "Price (€)",
        
        # Gross Area
        "gross_area": "GrossArea",
        "area.gross": "GrossArea",
        
        # Terrain Area
        "area.land": "Terrain Area (m2)",
        
        # Area
        "Area": "Area (m2)",
        
        # Elevator
        "Elevador": "Elevator",
        
        # Useful Area
        "useful_area": "Useful Area (m2)",
        "Useful Area": "Useful Area (m2)",
        "area.net": "Useful Area (m2)",
        
        # Living Area
        "LivingArea": "Living Area (m2)",
        
        # Built Area
        "BuiltArea": "Raw Construction Area (m2)",
        
        # Number of Bedrooms
        "rooms": "NumberOfBedrooms",
        "Bedrooms": "NumberOfBedrooms",
        
        # Number of WC
        "WC's": "NumberOfWC"
    }

    # Read CSV files as a Pandas dataframe each
    df_list = [pd.read_csv(file).rename(columns=COLUMN_MAPPING) for file in csv_files]

    # Concatenate the dataframes 
    df_final = pd.concat(df_list, ignore_index=True)

    # Remove duplicates and irrelevant attributes
    df_final = df_final.drop_duplicates() \
                       .drop(columns=["Index", "Unnamed: 0", "id", "advertiser", "views", "clicks", "Sealed"])
                   
    # Create a new column "Id" with unique values starting from 1             
    df_final.insert(0, "Id", range(1, len(df_final) + 1))
    
    # TODO: Remove irrelevant or redundant attributes (columns) from the dataframe (Feature Selection)
    
    # TODO: Convert categorical attributes to numerical values
        # Feature Engineering: The "title" attribute is a categorical attribute so it will
        # be split into multiple numerical attributes, one for each unique value of the "title" attribute.
    
    # TODO: Remove outliers
    
    # TODO: Normalize the data (Min-Max Scaling or Standardization)
    
    # TODO: Handle missing values (Imputation or Removal)
    
    # TODO: Feature Reduction (PCA, LDA, etc.)
    
    # TODO: Bias mitigation (if necessary)
    
    # Save the final dataframe as a CSV file
    df_final.to_csv(f"backend/datasets/{final_filename}", index=False)
    
    # Split the data into training and testing sets (Train-Test Split)
    return train_test_split(df_final, test_size=0.2, random_state=42)


if __name__ == "__main__":
    df_train, df_test = prepare_data()