import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.decomposition import PCA
from backend.app.constants import COLUMN_RENAME_MAP, CATEGORICAL_COLUMNS
from sklearn.preprocessing import StandardScaler


"""
Prepare the internal data by reading CSV files, renaming columns, concatenating dataframes, and removing duplicates.

Args:
    datasets_path (str): Path to the folder containing the CSV files.

Returns:
    df_internal (pd.DataFrame): The final prepared dataframe.
    
"""
def prepare_internal_data(internal_datasets_path="backend/datasets/internal"):
    
    # Define the folder containing the CSV files
    folder = Path(internal_datasets_path)

    # Include all CSV files in the specified folder, except for the final output file.
    # This approach has the advantage of supporting multiple datasets being stored in "datasets_path",
    # which will be useful in the future if more datasets are added to the folder to train / test the models
    csv_files = [file for file in folder.glob("*.csv")]

    # Read CSV files as a Pandas dataframe each
    df_list = [pd.read_csv(file).rename(columns=COLUMN_RENAME_MAP) for file in csv_files]

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
def prepare_external_data(external_datasets_path="backend/datasets/external"):
    pass


# Join internal and external datasets, using the appropriate keys in the join method
def join_internal_and_external_data(df_internal, df_external):
    pass


def prepare_final_data(df_final, final_filename="real_estate_internal_data_final.csv", save_new_dataset_as_csv_file=True):
    
    # Split data into train and test dataset
    X = df_final.drop("Price (euros)", axis=1)
    y = df_final["Price (euros)"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=True)
    
    print("Number of training samples before removing 'outliers':", X_train.shape[0])
    
    # Remove price outliers using only training data; TODO analyze how this affects the model's results
    mean_price = y_train.mean()
    std_price = y_train.std()

    lower_bound = mean_price - 3 * std_price
    upper_bound = mean_price + 3 * std_price

    outlier_mask = ((y_train < lower_bound) | (y_train > upper_bound))

    X_train = X_train.loc[~outlier_mask]
    y_train = y_train.loc[~outlier_mask]
    
    print("Number of training samples after removing 'outliers':", X_train.shape[0])
    
    # Handle missing values (Imputation or Removal)
    imputer = SimpleImputer(strategy="median")
    
    X_train = pd.DataFrame(data=imputer.fit_transform(X_train), columns=X.columns, index=X_train.index)
    
    X_test = pd.DataFrame(data=imputer.transform(X_test), columns=X.columns, index=X_test.index)

    # Normalize the data; TODO analyze later how this affects the model efficacy)
    scaler = StandardScaler()
    
    X_train = pd.DataFrame(scaler.fit_transform(X_train), columns=X.columns, index=X_train.index)
    
    X_test = pd.DataFrame(scaler.transform(X_test), columns=X.columns, index=X_test.index)
    
    # Feature Reduction (PCA); TODO analyze later how this affects the model efficacy
    pca = PCA()
    
    X_train = pd.DataFrame(data=pca.fit_transform(X_train), columns=X.columns, index=X_train.index)
    
    X_test = pd.DataFrame(data=pca.transform(X_test), columns=X.columns, index=X_test.index)
    
    # TODO: Bias mitigation (if necessary, check this after seeing the first results of the models in test)
        
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
    
    # Save the final dataframe as a CSV file if the flag is True
    if save_new_dataset_as_csv_file:
        df_final.to_csv(f"backend/datasets/{final_filename}", index=False)
        
    # NOTE: uncomment this to print some examples of the training and testing datasets
    """print(pd.DataFrame(X_train).head(20))
    print(pd.DataFrame(X_test).head(20))
    print(pd.DataFrame(y_train).head(20))
    print(pd.DataFrame(y_test).head(20))"""
    
    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    
    df_internal = prepare_internal_data()
    
    # TODO create external dataset; prepare_external_data
    
    # TODO concatenate external dataset with internal dataset through join; join_internal_and_external_data
    df_final = df_internal
    
    X_train, X_test, y_train, y_test = prepare_final_data(df_final, save_new_dataset_as_csv_file=True)
    
    