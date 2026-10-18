

# backend/common/dataset_names.py
def get_eurostat_dataset_name(dataset_code, country_code, time_period):
    return f"eurostat_{dataset_code}_{country_code.lower()}_{time_period.replace(':', '_')}"

def get_fsq_places_dataset_name(country_code):
    return f"fsq_{country_code.lower()}_places"

def get_ine_dataset_name(value_attr_name):
    return f"ine_{value_attr_name}"

def get_ecb_dataset_name(value_attr_name):
    return f"ecb_{value_attr_name}"

# TODO review this after implementing Idealista API
def get_idealista_dataset_name(country_code):
    return f"idealista_{country_code.lower()}_properties"

def get_geoapify_dataset_name(country_code):
    return f"geoapify_{country_code.lower()}_places"

def get_final_dataset_name(country_code):
    return f"real_estate_{country_code.lower()}_data"