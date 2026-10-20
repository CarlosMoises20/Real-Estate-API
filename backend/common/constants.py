

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

# NOTE this is for pre-processing before creating ML models
CATEGORICAL_COL_MAPPING = {

    # Give each floor a numeric number 
    "Floor": {
        "Basement Level": -1,
        "Basement": -1,
        "Ground Level": 0,
        "1st Floor": 1,
        "2nd Floor": 2,
        "3rd Floor": 3,
        "4th Floor": 4,
        "5th Floor": 5,
        "6th Floor": 6,
        "7th Floor": 7,
        "8th Floor": 8,
        "9th Floor": 9,
        "10th Floor": 10,
        "Above 10th Floor": 11
    },
    
    # TODO for "FloorType", review the best approach before implementing ML models;
    # For 'Duplex', 'Top Floor', 'Triplex', 'Attic', 'Mezzanine', 'Service Floor'
    
    # Greater numeric values represent better energy efficiency
    "EnergyCertificate": {
        "A+": 8,
        "A": 7,
        "B": 6,
        "B-": 5,
        "C": 4,
        "D": 3,
        "E": 2,
        "F": 1,
        "G": 0
    },
    
    # Greater values indicate better conservation status
    "ConservationStatus": {
        "Needs renovation": 0,
        "Reasonable": 1,
        "Good condition": 2,
        "Like new": 3,
        "New": 4
    }

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

CITY_GEOCOD_NAMES = {
    "1500806": "Lagoa (Algarve)",
    "2004201": "Lagoa (São Miguel)",
    "2004302": "Praia da Vitória",        # INE: "Vila da Praia da Vitória"
    "2004501": "Calheta de S. Jorge",     # INE: "Calheta (R.A.A.)" / "Calheta"
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