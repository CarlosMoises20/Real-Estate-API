

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
    "Price": "Price_Euros",
    "LivingArea": "LivingArea_m2",
    "TotalArea": "TotalArea_m2",
    "BuiltArea": "BuiltArea_m2"
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
    "3003101": "Calheta (Madeira)"
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


# Parishes (City, Town) of the listings whose names cannot be matched automatically with CAOP
# (see map_listings_to_dicofre in utils.py); the value is the parish code (DICOFRE) in CAOP
PARISH_DICOFRE_OVERRIDES = {
    ("Arganil", "Vila Cova de Alva e Anceriz"): "060122",               # CAOP: "Vila Cova de Alva e Anseriz"
    ("Sobral de Monte Agraço", "São Quintino"): "111201",               # CAOP: "Santo Quintino"
    ("Arruda dos Vinhos", "Santiago dos Velhos"): "110204",             # CAOP: "S. Tiago dos Velhos"
    ("Braga", "São Victor"): "030351",                                  # CAOP: "Braga (São Vítor)"
    ("Macedo de Cavaleiros", "Grijó de Vale Benfeito"): "040515",       # CAOP: "Grijó"
    ("Macedo de Cavaleiros", "Sesulfe"): "040528",                      # CAOP: "Sezulfe"
    ("Fafe", "Passos"): "030719",                                       # CAOP: "Paços"
    ("Santarém", "Santarém (Marvila), Santa Iria da Ribeira de Santarém, Santarém (São Salvador) e Santarém (São Nicolau)"): "141633",   # CAOP: "União de freguesias da cidade de Santarém"
    ("Amarante", "Real, Ataíde e Oliveira"): "130147",                  # CAOP: "Vila Meã"
    ("Marco de Canaveses", "Penhalonga e Paços de Gaiolo"): "130738",   # CAOP: "Penha Longa e Paços de Gaiolo"
    ("Ribeira Grande", "Calheta"): "420501",                            # CAOP: "Calhetas"
    ("Campo Maior", "São João Batista"): "120403",                      # CAOP: "São João Baptista"
    ("Castelo de Vide", "São João Batista"): "120504"                   # CAOP: "São João Baptista"
}


# Groups of FSQ OS Places categories used as features; a place belongs to a group
# if any of its category labels starts with one of the group's prefixes
FSQ_CATEGORY_GROUPS = {
    "Supermarkets": ["Retail > Food and Beverage Retail > Supermarket",
                     "Retail > Food and Beverage Retail > Grocery Store"],
    "Restaurants": ["Dining and Drinking > Restaurant"],
    "Pharmacies": ["Retail > Pharmacy"],
    "HealthCenters": ["Health and Medicine > Hospital", "Health and Medicine > Medical Center"],
    "Schools": ["Community and Government > Education > Primary and Secondary School"],
    "Parks": ["Landmarks and Outdoors > Park"],
    "Beaches": ["Landmarks and Outdoors > Beach"],
    "Banks": ["Business and Professional Services > Financial Service > Banking and Finance > Bank"]
}



"""
Metadata of every data source used by the project (single source of truth for attribution)
This is exposed by the API (/api/v1/sources) and must be shown to the users of the API and web app,
since most licenses require the attribution to reach the end users, not only the code

    name: name of the source, as it must be cited
    attribution: text that must be shown wherever data from this source is displayed
    license: license or reuse conditions of the source
    license_url: link to the license or reuse conditions
    url: link to the source
    redistribution_allowed: whether the data can be exposed to third parties (API and web app);
                            False means the data can only be used internally (e.g. ML training)
    notes: additional obligations or pending verifications

"""
DATA_SOURCES = {
    "ine": {
        "name": "Statistics Portugal (INE)",
        "attribution": "Source: Statistics Portugal (INE)",
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "url": "https://www.ine.pt",
        "redistribution_allowed": True,
        "notes": "Values transformed by this project must be identified as derived"
    },
    "dgpj": {
        "name": "Directorate-General for Justice Policy (DGPJ)",
        "attribution": "Source: INE / Directorate-General for Justice Policy (DGPJ)",
        "license": "CC BY 4.0 (disseminated by INE)",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "url": "https://estatisticas.justica.gov.pt",
        "redistribution_allowed": True,
        "notes": "Original producer of the crime statistics disseminated by INE"
    },
    "eurostat": {
        "name": "Eurostat",
        "attribution": "Source: Eurostat",
        "license": "Eurostat reuse policy (commercial and non-commercial reuse with source acknowledgement)",
        "license_url": "https://ec.europa.eu/eurostat/help/copyright-notice",
        "url": "https://ec.europa.eu/eurostat",
        "redistribution_allowed": True,
        "notes": "Changes to the data must be stated; Eurostat is not responsible for derived values; logos are excluded"
    },
    "ecb": {
        "name": "European Central Bank (ECB)",
        "attribution": "Source: European Central Bank (ECB)",
        "license": "ECB reuse conditions (free use, reproduced accurately, with source acknowledgement)",
        "license_url": "https://www.ecb.europa.eu/services/disclaimer/html/index.en.html",
        "url": "https://data.ecb.europa.eu",
        "redistribution_allowed": True,
        "notes": "Transformations (e.g. growth rates, seasonal adjustment) must be stated explicitly"
    },
    "fsq_os_places": {
        "name": "Foursquare Open Source Places",
        "attribution": "Contains data from Foursquare Open Source Places",
        "license": "Apache-2.0",
        "license_url": "https://www.apache.org/licenses/LICENSE-2.0",
        "url": "https://docs.foursquare.com/data-products/docs/fsq-places-open-source",
        "redistribution_allowed": True,
        "notes": "A copy of the license and the Foursquare copyright notice must be included (see NOTICE)"
    },
    "openstreetmap": {
        "name": "OpenStreetMap",
        "attribution": "© OpenStreetMap contributors",
        "license": "ODbL 1.0",
        "license_url": "https://www.openstreetmap.org/copyright",
        "url": "https://www.openstreetmap.org",
        "redistribution_allowed": True,
        "notes": "Publicly shared databases derived from OSM (e.g. POI counts per area) must be released under ODbL"
    },
    "geoapify": {
        "name": "Geoapify",
        "attribution": "Powered by Geoapify | © OpenStreetMap contributors",
        "license": "Geoapify Terms and Conditions (data from OpenStreetMap, ODbL 1.0)",
        "license_url": "https://www.geoapify.com/terms-and-conditions/",
        "url": "https://www.geoapify.com",
        "redistribution_allowed": False,
        "notes": "Storage and redistribution of API results not confirmed in the terms; Geoapify attribution is mandatory on the free plan"
    },
    "kaggle_pt_listings": {
        "name": "Portugal Real Estate dataset (luvathoms, Kaggle)",
        "attribution": "Source: Portugal Real Estate dataset (luvathoms, Kaggle)",
        "license": "MIT (as declared by the uploader; origin of the listings unverified)",
        "license_url": "https://www.kaggle.com/datasets/luvathoms/portugal-real-estate-2024",
        "url": "https://www.kaggle.com/datasets/luvathoms/portugal-real-estate-2024",
        "redistribution_allowed": False,                # TODO verify terms
        "notes": "Use only for development and ML training until the origin of the listings and the authorization of the source platforms are confirmed"
    },
    "dgt_caop": {
        "name": "Carta Administrativa Oficial de Portugal (CAOP), Direção-Geral do Território (DGT)",
        "attribution": "Source: CAOP 2024, Direção-Geral do Território (DGT)",
        "license": "Free download from DGT (license to confirm)",
        "license_url": "https://www.dgterritorio.gov.pt/cartografia/cartografia-tematica/caop",
        "url": "https://www.dgterritorio.gov.pt",
        "redistribution_allowed": True,
        "notes": "Parish boundaries and areas, used to assign places and listings to parishes; the license is not stated in the CAOP 2024 metadata"
    },
    "idealista": {
        "name": "idealista",
        "attribution": "Source: idealista",
        "license": "Pending (idealista API access request)",
        "license_url": "https://developers.idealista.com",
        "url": "https://www.idealista.pt",  
        "redistribution_allowed": False,                # TODO verify terms
        "notes": "Storage, display and redistribution require idealista's express written authorization"
    }
}


""" TODO add geospatial data when these enter the JOIN

Metadata of each external column of the final dataset, used to attach the source to every value exposed by the API

    source: key of DATA_SOURCES
    series: code of the series in the source
    derived: whether the value was transformed by this project (True) or is the official published value (False)
    transformation: description of the transformation, when derived is True

"""
SERIES_SOURCES = {
    "GDP_QoQ": {
        "source": "eurostat",
        "series": "namq_10_gdp (B1GQ, CLV_PCH_PRE, SCA)",
        "derived": False,
        "transformation": None
    },
    "GDP_YoY": {
        "source": "eurostat",
        "series": "namq_10_gdp (B1GQ, CLV_PCH_SM, SCA)",
        "derived": False,
        "transformation": None
    },
    "HouseholdConsumption_QoQ": {
        "source": "eurostat",
        "series": "namq_10_gdp (P31_S14, CLV_PCH_PRE, SCA)",
        "derived": False,
        "transformation": None
    },
    "HouseholdConsumption_YoY": {
        "source": "eurostat",
        "series": "namq_10_gdp (P31_S14, CLV_PCH_SM, SCA)",
        "derived": False,
        "transformation": None
    },
    "InflationGrowthRate": {
        "source": "ine",
        "series": "0014647",
        "derived": False,
        "transformation": None
    },
    "AvgSalary_Euros": {
        "source": "ine",
        "series": "0011132",
        "derived": False,
        "transformation": None
    },
    "AvgSalary_12m_avg_Euros": {
        "source": "ine",
        "series": "0011132",
        "derived": True,
        "transformation": "12-month average: mean of the official 3-month values ending in months t, t-3, t-6 and t-9"
    },
    "HousingCreditRate": {
        "source": "ecb",
        "series": "MIR.M.PT.B.A2C.A.R.A.2250.EUR.N",
        "derived": False,
        "transformation": None
    },
    "UnemploymentRate": {
        "source": "ine",
        "series": "0012136",
        "derived": False,
        "transformation": None
    },
    "HousingNumTransactions": {
        "source": "ine",
        "series": "0012785",
        "derived": False,
        "transformation": None
    },
    "HousingNumTransactions_4Q_YoY": {
        "source": "ine",
        "series": "0012785",
        "derived": True,
        "transformation": "Year-on-year growth rate (%) of the sum of the last 4 quarters, per region"
    },
    "HousingPricePerM2_Euros": {
        "source": "ine",
        "series": "0012255",
        "derived": False,
        "transformation": None
    },
    "CrimeRate": {
        "source": "dgpj",
        "series": "0000849 (2009-2010), 0008074 (2011-2020), 0012260 (2021 onwards)",
        "derived": False,
        "transformation": None
    },

    # Density of places per group of FSQ_CATEGORY_GROUPS (e.g. "POI_Supermarkets_per_km2")
    **{
        f"POI_{group}_per_km2": {
            "source": "fsq_os_places",
            "series": f"FSQ OS Places ({', '.join(prefixes)}); parish areas from CAOP 2024 (DGT)",
            "derived": True,
            "transformation": "Number of places open at the listing's publish date in the listing's parish, divided by the parish area (km2)"
        }
        for group, prefixes in FSQ_CATEGORY_GROUPS.items()
    }
}


# Disclaimers that must be shown to the users of the API and web app (and included in the terms of use)
DATA_DISCLAIMERS = [
    "Official statistics are revised by their producers over time; values reflect the date they were retrieved.",
    "Values marked as derived were calculated by this project and are not official statistics.",
    "INE, DGPJ, Eurostat and the ECB are not responsible for derived values or for the use made of the data.",
    "Property price estimates are produced by statistical models and are not official property valuations."
]