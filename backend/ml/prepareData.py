import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.decomposition import PCA
from backend.app.constants import COLUMN_RENAME_MAP, CATEGORICAL_COLUMNS
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
                                "real_estate_internal_data_final_v0.csv"],
                 save_new_dataset_as_csv_file=True):
    
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
    
    # Dummy Coding to encode categorical attributes
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
    
    # for some negative values, transform those into positive values by applying the absolute value
    for attr_name in ["Living Area (m2)", "Total Area (m2)", "Built Area (m2)",
                      "NumberOfBathrooms", "NumberOfWC"]:
        
        df_final[attr_name] = df_final[attr_name].abs()
    
    # Split data into train and test dataset
    X = df_final.drop("Price (euros)", axis=1)
    y = df_final["Price (euros)"]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, shuffle=True
    )
    
    print("Number of training samples before removing 'outliers':", X_train.shape[0])
    
    # Remove price outliers using only training data; TODO analyze how this affects the model's results
    mean_price = y_train.mean()
    std_price = y_train.std()

    lower_bound = mean_price - 3 * std_price
    upper_bound = mean_price + 3 * std_price

    outlier_mask = (
        (y_train < lower_bound) |
        (y_train > upper_bound)
    )

    X_train = X_train.loc[~outlier_mask]
    y_train = y_train.loc[~outlier_mask]
    
    print("Number of training samples after removing 'outliers':", X_train.shape[0])
    
    # Handle missing values (Imputation or Removal)
    imputer = SimpleImputer(strategy="median")
    
    X_train = pd.DataFrame(
        imputer.fit_transform(X_train),
        columns=X.columns,
        index=X_train.index
    )
    X_test = pd.DataFrame(
        imputer.transform(X_test),
        columns=X.columns,
        index=X_test.index
    )

    # Normalize the data; TODO analyze later how this affects the model efficacy)
    scaler = StandardScaler()
    
    X_train = pd.DataFrame(
        scaler.fit_transform(X_train),
        columns=X.columns,
        index=X_train.index
    )
    X_test = pd.DataFrame(
        scaler.transform(X_test),
        columns=X.columns,
        index=X_test.index
    )
    
    # Feature Reduction (PCA); TODO analyze later how this affects the model efficacy
    pca = PCA()
    
    X_train = pd.DataFrame(
        pca.fit_transform(X_train),
        columns=X.columns,
        index=X_train.index
    )
    X_test = pd.DataFrame(
        pca.transform(X_test),
        columns=X.columns,
        index=X_test.index
    )
    
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
    
    # Split the data into training and testing sets (Train-Test Split)
    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    X_train, X_test, y_train, y_test = prepare_data(save_new_dataset_as_csv_file=False)