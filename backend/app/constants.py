
# database credentials
DB_USERNAME = "postgres"
DB_PASSWORD = "postgres"

# database access
DB_HOST = "localhost"
DB_PORT = 5432

"""
Mapping of dataset-specific column names to standardized column names.
Currently, this is mainly used to make attribute names and units explicit
and consistent. It also provides a standardized schema for combining
multiple datasets in the future.
The dictionary key represents the original column name, while the value
represents the standardized column name used in the final dataset.
This prevents redundancy when different datasets use different names for
equivalent attributes. For example, "price" and "price_int" may both
represent the property's price and should therefore be mapped to the same
standardized column name.

"""
COLUMN_RENAME_MAP = {
    "Price": "Price (euros)",
    "LivingArea": "Living Area (m2)",
    "TotalArea": "Total Area (m2)",
    "BuiltArea": "Built Area (m2)"
}

# Columns that represent categorical attributes
CATEGORICAL_COLUMNS = ["Type", "District", "City", "Town", 
                       "EnergyCertificate", "ConservationStatus", "Floor",
                       "EnergyEfficiencyLevel"]