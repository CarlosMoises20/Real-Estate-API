

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

# Residential Properties
PROPERTY_RESIDENTIAL_TYPES = [
    "Apartment", "House", "Duplex", "Studio",
    "Mansion", "Manor", "Other - Residential",
    "Investment"
]

# Oath base of every datasets of the project
DATASETS_PATH_BASE = "./backend/datasets"

# Dictionary to map cities to its corresponding countries. This
# dictionary can be updated as necessary
CITY_TO_COUNTRY_CODE = {
    "Dubai": "AE"
}

CITY_REGION_OVERRIDES = {
    **dict.fromkeys(["Arouca", "Castelo de Paiva", "Espinho", "Oliveira de Azeméis", "Santa Maria da Feira",
                     "São João da Madeira", "Vale de Cambra",      # Aveiro district
                     "Vila Nova de Foz Côa",                       # Guarda
                     "Cinfães", "Penedono"], "Norte"),             # Viseu
    **dict.fromkeys(["Alcobaça", "Bombarral", "Caldas da Rainha", "Nazaré", "Peniche", "Óbidos",   # Leiria
                     "Alenquer", "Arruda dos Vinhos", "Azambuja", "Cadaval", "Lourinhã",
                     "Sobral de Monte Agraço", "Torres Vedras"], "Oeste e Vale do Tejo"),          # Lisboa
    **dict.fromkeys(["Alcácer do Sal", "Grândola", "Santiago do Cacém", "Sines"], "Alentejo"),    # Setúbal
}

# Mapping Portuguese districts (values) to their parent regions (keys)
LOCATION_MAPPING = {
    # North of Portugal
    "Norte": [
        "Viana do Castelo",
        "Braga",
        "Porto",
        "Vila Real",
        "Bragança"
    ],

    # Center of Portugal
    "Centro": [
        "Aveiro",
        "Coimbra",
        "Leiria",
        "Viseu",
        "Guarda",
        "Castelo Branco"
    ],

    # Lisbon Regions
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

    # Autonomous regions (not mainland districts)
    "Região Autónoma dos Açores": [
        "Ilha Terceira",
        "Ilha de São Miguel",
        "Ilha de Santa Maria",
        "Ilha do Faial",
        "Ilha das Flores",
        "Ilha do Pico",
        "Ilha Graciosa",
        "Ilha de São Jorge",
        "Ilha do Corvo"
    ],

    "Região Autónoma da Madeira": [
        "Ilha da Madeira",
        "Ilha de Porto Santo",
        "Ilhas Desertas",
        "Ilhas Selvagens"
    ]
}