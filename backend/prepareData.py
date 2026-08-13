import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.decomposition import PCA
from app.constants import COLUMN_RENAME_MAP, CATEGORICAL_COLUMNS
from sklearn.preprocessing import StandardScaler


"""
Prepare the data by reading CSV files, renaming columns, concatenating dataframes, and removing duplicates.

Args:
    datasets_path (str): Path to the folder containing the CSV files.
    final_filename (str): Name of the final CSV file to be generated.

Returns:
    df_final (pd.DataFrame): The final prepared dataframe.
    
"""
def prepare_data(datasets_path="backend/datasets", final_filename="real_estate_internal_data_final.csv", 
                 old_filenames=["real_estate_internal_data_final.csv", 
                                "real_estate_internal_data_final_v0.csv"]):
    
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
    
    # Convert all boolean attributes to integer
    df_final = df_final.map(lambda x: int(x) if isinstance(x, bool) else x)
    
    # Dummy Coding
    df_final = pd.get_dummies(data=df_final, columns=CATEGORICAL_COLUMNS, dtype=int)
    
    # Convert "PublishDate" column to datetime and extract year, month and day to have only numeric attributes
    df_final["PublishDate"] = pd.to_datetime(
        df_final["PublishDate"],
        errors="coerce"
    )
    
    df_final["PublishYear"] = df_final["PublishDate"].dt.year
    df_final["PublishMonth"] = df_final["PublishDate"].dt.month
    df_final["PublishDay"] = df_final["PublishDate"].dt.day
    
    df_final = df_final.drop(columns=["PublishDate", "EnergyEfficiencyLevel"])
    
    """# TODO fix this issue with negative values
    for attr_name in ["Living Area (m2)", "Total Area (m2)", "Built Area (m2)",
                      "NumberOfBathrooms", "NumberOfWC"]:
        
        df_final[attr_name] = pd.to_numeric(df_final[attr_name], errors="coerce").abs()
    
    # Split data into train and test dataset
    X = df_final.drop("Price (euros)", axis=1)
    y = df_final["Price (euros)"]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, shuffle=True
    )
    
    # Handle missing values (Imputation or Removal); TODO: review this
    imputer = SimpleImputer(strategy="median")
    
    X_train = imputer.fit_transform(X_train)
    X_test = imputer.transform(X_test)

    # Normalize the data
    scaler = StandardScaler()
    
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    # Feature Reduction (PCA, LDA, etc.); verify if it's necessary
    pca = PCA()
    
    X_train = pca.fit_transform(X_train)
    X_test = pca.transform(X_test)
    
    # TODO: Bias mitigation (if necessary, check this after seeing the first results of the models in test)
    
    pd.DataFrame(X_train).head(10)
    pd.DataFrame(X_test).head(10)"""
        
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
    
    # Save the final dataframe as a CSV file
    df_final.to_csv(f"backend/datasets/{final_filename}", index=False)
    
    # Split the data into training and testing sets (Train-Test Split)
    #return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    #X_train, X_test, y_train, y_test = prepare_data()
    prepare_data()