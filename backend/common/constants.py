

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


PROPERTY_RESIDENTIAL_TYPES = [
    "Apartment",
    "House",
    "Duplex",
    "Other - Residential",
    "Studio",
    "Farm",
    "Mansion",
    "Manor",
]

PROPERTY_STANDARD_HOUSING_TYPES = [
    "Apartment",
    "House",
    "Duplex",
    "Studio",
    "Other - Residential",
]

PROPERTY_SPECIAL_RESIDENTIAL_TYPES = [
    "Farm",
    "Mansion",
    "Manor",
]

# Mapping Portuguese subregions to their parent regions on the dataset
LOCATION_MAPPING = {
    # North of Portugal
    "Norte": [
        "Vila Real",
        "Porto",
        "Braga",
        "Bragança",
        "Viana do Castelo"
    ],

    # Center of Portugal
    "Centro": [
        "Leiria",
        "Guarda",
        "Coimbra",
        "Viseu",
        "Castelo Branco",
        "Aveiro"
    ],

    # Lisbom Regions
    "Grande Lisboa": [
        "Lisboa"
    ],
    
    "Península de Setúbal": [
        "Setúbal"
    ],

    # Oeste e Vale do Tejo
    "Oeste e Vale do Tejo": [
        "Santarém"
    ],

    # Alentejo
    "Alentejo": [
        "Beja",
        "Évora",
        "Portalegre"
    ],

    # Algarve
    "Algarve": [
        "Faro"
    ],

    # Automonous regions
    "Região Autónoma dos Açores": [
        "Ilha Terceira",
        "Ilha de São Miguel",
        "Ilha de Santa Maria",
        "Ilha de São Jorge",
        "Ilha do Faial",
        "Ilha das Flores",
        "Ilha do Pico"
    ],

    "Região Autónoma da Madeira": [
        "Ilha da Madeira",
        "Ilha de Porto Santo"
    ]
}