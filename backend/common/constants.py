

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
                       "EnergyCertificate", "ConservationStatus", "Floor"]


# List of coordinates for Portugal Continent, Azores, and Madeira to retrieve geospatial data
PORTUGAL_COORDINATES_LIST = [
    {
        "portugal_continent": {
            "min_lon": -9.6,
            "min_lat": 36.9,
            "max_lon": -6.1,
            "max_lat": 42.2
        }
    },
    {
        "portugal_azores": {
            "min_lon": -31.4,
            "min_lat": 36.8,
            "max_lon": -24.9,
            "max_lat": 39.8
        }
    },
    {
        "portugal_madeira": {
            "min_lon": -17.4,
            "min_lat": 30.0,
            "max_lon": -15.8,
            "max_lat": 33.2
        }
    }
]