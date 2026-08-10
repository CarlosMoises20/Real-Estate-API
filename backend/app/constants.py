
# database credentials
DB_USERNAME = "postgres"
DB_PASSWORD = "postgres"

# database access
DB_HOST = "localhost"
DB_PORT = 5432

# this dictionary to map the columns names to the final ones, to remove redundancy of attributes after concatenation
# the property is the old name of the attribute and the value is the new name of the attribute
# this step is done because there are different datasets with attributes that represent the same thing but with different names
# for example, some datasets have "price" and others "price_int", and in both cases, this represents the Price. The idea is that in both datasets,
# these attributes will be renamed to an equal name (in this case "Price") so that when concatenating the datasets, there will be no redundancy of attributes.
ATTR_MAPPING = {
    
    # Location
    "location": "Location",
    "Localization": "Location",
    
    # Latitude and longitude
    "latitude": "Latitude",
    "longitude": "Longitude",
    
    # Price
    "price": "Price (euros)",
    "price_int": "Price (euros)",
    "Price": "Price (euros)",
    
    # Gross Area
    "gross_area": "GrossArea (m2)",
    "area.gross": "GrossArea (m2)",
    "Gross Area": "GrossArea (m2)",
    
    # Terrain Area
    "area.land": "Terrain Area (m2)",
    
    # Area
    "Area": "Area (m2)",
    
    # Elevator
    "Elevador": "Elevator",
    
    # Energy Certificate
    "EnergyCertificate": "Energy Certificate",
    
    # Useful Area
    "useful_area": "Useful Area (m2)",
    "Useful Area": "Useful Area (m2)",
    "area.net": "Useful Area (m2)",
    
    # Living Area
    "LivingArea": "Living Area (m2)",
    
    # Total Area
    "TotalArea": "Total Area (m2)",
    
    # Built Area
    "BuiltArea": "Raw Construction Area (m2)",
    
    # Number of Bedrooms
    "rooms": "NumberOfBedrooms",
    "Bedrooms": "NumberOfBedrooms",
    
    # Number of WC
    "WC's": "NumberOfWC"
}



COLUMN_ORDER = ["Id", "title", "Type", 
                
                "region", "Location", "District", "City", "Town",
                
                "NumberOfBedrooms", "NumberOfBathrooms", "NumberOfWC", "TotalRooms",
                
                "GrossArea (m2)", "Terrain Area (m2)", "Useful Area (m2)", "Living Area (m2)", "Raw Construction Area (m2)",
                "Area (m2)", "Total Area (m2)",
                
                "Longitude", "Latitude",
                
                "Floors", "Floor", "Elevator", "Garage",
                
                "ConstructionYear", "Construction Viability",
                
                "Parking", "Fractions",
                
                "Energy Certificate", "EnergyEfficiencyLevel",
                
                "started_at", "PublishDate",
                
                "ElectricCarsCharging", "ConservationStatus", "LotSize",
                
                "Price (euros)"]