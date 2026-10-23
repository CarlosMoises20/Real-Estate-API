
import re, calendar, os, pycountry, unicodedata
import pandas as pd
import numpy as np
from pathlib import Path
from babel import Locale
from backend.common.constants import LOCATION_MAPPING, CITY_GEOCOD_NAMES, CITY_TO_COUNTRY_CODE, PROPERTY_RESIDENTIAL_TYPES, CITY_REGION_OVERRIDES, PARISH_DICOFRE_OVERRIDES


"""
Generic methods to convert columns from a Pandas dataframe, to datetime format

    df - a Pandas dataframe
    cols - a list of strings representing column names of the 'df' dataframe
    format - similar to the 'format' parameter of the 'to_datetime' method from Pandas

"""
def convert_pd_df_columns_to_datetime(df, cols, format=None):
    for col in cols:
        if col not in df.columns:
            raise KeyError(
                f"Column '{col}' does not exist in the dataframe. "
                f"Columns list: {df.columns.tolist()}"
            )
            
        df[col] = pd.to_datetime(df[col], format=format)
        
 
"""
Auxiliary method to translate names of cities and countries

    original_language: the language in which the city / country is in; must be specified in the country-code 2-letter format in lowercase (for example, "pt" for portuguese and "en" for english)
    
    target_language: the language in which the city / country will be translated to; must be specified in the country-code 2-letter format in lowercase (for example, "pt" for portuguese and "en" for english); by default, it's english ("en")
    
""" 
def build_translate_names(original_language, target_language="en"): 

    original = Locale.parse(original_language).territories
    translated = Locale.parse(target_language).territories

    translate_names = {
        name.title(): translated[code]
        for code, name in original.items()
        if code in translated and pycountry.countries.get(alpha_2=code)
    }
    
    translate_names.update({
        city.title(): translated[code]
        for city, code in CITY_TO_COUNTRY_CODE.items()
        if code in translated and pycountry.countries.get(alpha_2=code)
    })
    
    return translate_names



"""
Normalize a parish (freguesia) name to match listings with CAOP
(removes the "União das freguesias de" prefix, accents and case)

"""
def normalize_parish_name(name):
    name = re.sub(r"^Uni[ãa]o d[ae]s? freguesias d[eao]s? ", "", str(name), flags=re.IGNORECASE)
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    name = re.sub(r"\s+", " ", name).strip().lower()

    # Expand the abbreviation "S." (e.g. "Calheta de S. Jorge" -> "calheta de sao jorge")
    return re.sub(r"\bs\.\s*", "sao ", name)


"""
Split a normalized place name into a set of words, ignoring punctuation and connectors ("e", "de", "do", ...),
so that names written differently match (e.g. "Costa de Caparica" and "Costa da Caparica",
"Santiago (Sesimbra)" and "Sesimbra (Santiago)")

"""
def get_name_tokens(name):
    return set(re.sub(r"[^a-z0-9]+", " ", normalize_parish_name(name)).split()) - {"e", "de", "da", "do", "das", "dos", "d"}


"""
Map each listing to the code of its parish (freguesia) in the CAOP (DICOFRE), based on the names of
the district, municipality (City) and parish (Town), since the listings have no coordinates

The parish names are compared within the same district and municipality, in 3 steps:
    1. Same normalized name
    2. Same set of words, ignoring the municipality name (e.g. "São Sebastião" and "Setúbal (São Sebastião)")
    3. The words of one name are contained in the other, and only one parish of the municipality matches
       (e.g. a parish that existed before 2013, "Coruche", and its current union "Coruche, Fajarda e Erra")

Exceptions that are not solved by these steps are defined in PARISH_DICOFRE_OVERRIDES

    df: Pandas dataframe with the listings ("District", "City" and "Town" columns)
    df_parishes: Pandas dataframe with the CAOP parishes ("dicofre", "parish", "municipality", "district_island")
    returns: a Pandas series with the DICOFRE code of each listing (NaN when there is no match)

"""
def map_listings_to_dicofre(df, df_parishes):

    # Remove the suffixes used to disambiguate municipality names (e.g. "Lagoa (Algarve)" -> "Lagoa")
    strip_suffix = lambda city: re.sub(r"\s*\(.*\)$", "", str(city))

    municipality_key = lambda district, city: normalize_parish_name(district) + "|" + normalize_parish_name(strip_suffix(city))

    # Parishes of each municipality: (dicofre, normalized name, words, words without the municipality name)
    parishes_by_municipality = {}

    for row in df_parishes.itertuples():
        municipality_tokens = get_name_tokens(row.municipality)
        tokens = get_name_tokens(row.parish)
        parishes_by_municipality.setdefault(municipality_key(row.district_island, row.municipality), []).append(
            (row.dicofre, normalize_parish_name(row.parish), tokens, (tokens - municipality_tokens) or tokens)
        )


    """Find the DICOFRE code of a single (district, city, town) combination"""
    def match_parish(district, city, town):

        if (city, town) in PARISH_DICOFRE_OVERRIDES:
            return PARISH_DICOFRE_OVERRIDES[(city, town)]

        candidates = parishes_by_municipality.get(municipality_key(district, city), [])

        name = normalize_parish_name(town)
        tokens = get_name_tokens(town)
        tokens_no_municipality = (tokens - get_name_tokens(strip_suffix(city))) or tokens

        # 1. Same normalized name
        for dicofre, parish_name, _, _ in candidates:
            if parish_name == name:
                return dicofre

        # 2. Same set of words, ignoring the municipality name
        matches = [dicofre for dicofre, _, _, parish_tokens in candidates if parish_tokens == tokens_no_municipality]

        if len(matches) == 1:
            return matches[0]

        # 3. The words of one name are contained in the other (only accepted if there is a single match)
        matches = [dicofre for dicofre, _, parish_tokens, _ in candidates
                   if tokens and (tokens <= parish_tokens or parish_tokens <= tokens)]

        return matches[0] if len(matches) == 1 else np.nan


    # Match each distinct combination only once, since there are many listings per parish
    combinations = df[["District", "City", "Town"]].drop_duplicates().dropna()

    combinations["dicofre"] = [match_parish(*row) for row in combinations.itertuples(index=False)]

    unmatched = combinations[combinations["dicofre"].isna()]

    if len(unmatched) > 0:
        print(f"Parishes without a match in CAOP ({len(unmatched)}); add them to PARISH_DICOFRE_OVERRIDES if needed:")
        print(unmatched[["District", "City", "Town"]].to_string(index=False))

    return df.merge(combinations, on=["District", "City", "Town"], how="left")["dicofre"].set_axis(df.index)


"""
Assign each place to the category groups defined in 'category_groups' (e.g. FSQ_CATEGORY_GROUPS)
A place belongs to a group if any of its category labels starts with one of the group's prefixes;
a place can belong to several groups, so the returned dataframe has one row per (place, group)

    df: Pandas dataframe with the places
    label_col: name of the column with the category labels, separated by 'separator'
    category_groups: dictionary {group name: list of category label prefixes}

"""
def assign_category_groups(df, label_col, category_groups, separator="|"):

    df_labels = df.assign(_label=df[label_col].str.split(separator)).explode("_label")
    df_labels["_label"] = df_labels["_label"].str.strip()

    df_groups = []

    for group, prefixes in category_groups.items():
        mask = df_labels["_label"].str.startswith(tuple(prefixes), na=False)
        df_groups.append(df_labels[mask].assign(category_group=group))

    df_groups = pd.concat(df_groups, ignore_index=True).drop(columns=["_label"])

    # A place with several labels of the same group counts only once in that group
    return df_groups.drop_duplicates(subset=[c for c in df.columns if c != label_col] + ["category_group"])



"""
Helper for price per square meter and crime dataframes

"""
def keep_city_level(df_external):
    df_external = df_external[df_external["geocod"].astype(str).str.len() == 7].copy()
    df_external["geodsg"] = df_external["geocod"].astype(str).map(CITY_GEOCOD_NAMES).fillna(df_external["geodsg"])
    return df_external.drop_duplicates(["geodsg", "date_end"], keep="last") 


"""
Generic method to join internal data (df) with external data (df_external) by date range (by default,
"date_end" column, based on the rule "right_end_date_col < PublishDate", to use the latest available metric
that was published in the moment that the property was published; for example, a property from 2026 is associated
to the inflation of 2025, because at the moment that property was published, the inflation of 2026 was not yet known)

    df: a Pandas dataframe with data representing internal factors (number of rooms, number of WC, price, etc.)
    df_external: a Pandas dataframe (or a list of Pandas dataframes) with data representing external factors (inflation, average salary, etc.)
    old_col_name: a string representing the old name of the column representing the value of the parameter to be joined
    new_col_name: a string representing the name of the column to be created, representing the value of the parameter to be joined

    left_date_col: a string representing the name of the left date column in the 'df' dataframe
    right_end_date_col: a string representing the name of the end date column in the 'df_external' dataframe
    
    left_region_col: a string representing the name of the left region column in the 'df' dataframe
    right_region_col: a string representing the name of the right region column in the 'df_external' dataframe; 
                    this parameter is optional but it must be specified if you want to join data based on region, where
                        left_region_col = right_region_col
                        
    property_specific: a boolean flag that indicates whether if the JOIN is only applied to houses (True), or to all types of property (False)
    
    location_mapping: a boolean flag that indicates whether it's necessary to map the location names to match the original ones (True) or not (False)
                        This mapping will consider that the values of df_external[right_region_col] are keys of LOCATION_MAPPING ("Norte", "Centro", "Grande Lisboa", etc) 
                        and the values of df[left_region_col] are values of LOCATION_MAPPING ("Vila Real", "Porto", etc)
                        
    publication_lag_days: an optional integer which indicates how many days it takes for the metric to be published after "right_end_date_col"
                        For example, if 'date_end' is '2025-12-31' and the data is only published at '2026-01-15', the publication_lag_days must be set as 15; 
                        if it's published at '2026-02-28', publication_lag_days is 59 (31 + 28 = 59)
    
"""
def join_df_with_external_data(df, df_external, old_col_name, new_col_name, 
                                left_date_col="PublishDate", 
                                right_end_date_col="date_end",
                                left_region_col="City",
                                right_region_col=None,
                                property_specific=False,
                                location_mapping=False,
                                publication_lag_days=None):
    
    # If location_mapping is set to True and right_region_col is not specified, raise an exception
    if location_mapping and not right_region_col:
        raise ValueError("When 'location_mapping' is True, 'right_region_col' must be specified")
    
    if publication_lag_days and publication_lag_days < 0:
        raise ValueError("'publication_lag_days' must be >= 0")
    
    left_region_col = "District" if location_mapping else left_region_col

    # dt.normalize() -> Sets the time to midnight (00:00:00), preserving the timezone,
    # so that the comparison considers only the calendar date, not the time.
    # For example, if dt is 2025-12-31 00:00:00 and PublishDate is 2025-12-31 15:30:00,
    # normalizing PublishDate gives 2025-12-31 00:00:00, so both dates are equal
    left = pd.DataFrame({
        "_pos": np.arange(len(df)),
        "_date": df[left_date_col].dt.normalize().to_numpy(dtype="datetime64[ns]")   
    })
    
    lag = np.timedelta64(int(publication_lag_days or 0), "D")

    right = pd.DataFrame({
        "_end": df_external[right_end_date_col].dt.normalize().to_numpy(dtype="datetime64[ns]") + lag,
        "_value": df_external[old_col_name].to_numpy()
    })

    by = None
    
    # JOIN based on region if right_region_col is specified
    if right_region_col:
        
        # Location Mapping is only applied if location_mapping is set to True and right_region_col is specified
        # because if there is no region-based JOIN, there is no location-based JOIN and location mapping, since
        # location mapping is a part of the region-based JOIN 
        if location_mapping:
            
            # Dictionary that maps each district to its corresponding region
            # For example, Porto -> Norte; Lisboa -> Grande Lisboa; Braga -> Norte; Leiria -> Centro
            district_to_region = {
                district: region
                for region, districts in LOCATION_MAPPING.items()
                for district in districts
            }
            
            region = df["City"].map(CITY_REGION_OVERRIDES).fillna(df[left_region_col].map(district_to_region))
            
            unmapped = df.loc[region.isna() & df["District"].notna(), "District"].unique()
            
            if len(unmapped) > 0:
                print(f"Unmapped districts in LOCATION_MAPPING: {list(unmapped)}")

            left["_region"] = region.to_numpy()
            
        else:
            left["_region"] = df[left_region_col].to_numpy()
        
        right["_region"] = df_external[right_region_col].to_numpy()
        
        by = "_region"
        
    # Condition related to JOIN which only includes properties corresponding to some types
    # If the condition is true, properties such as stores, warehouses and offices might be excluded from the JOIN
    if property_specific:
        
        has_dwelling = df["NumberOfBedrooms"].gt(0) | df["NumberOfBathrooms"].gt(0)
        
        # Include only residential properties and farms/estates that have a dwelling (at least 1 bedroom or 1 bathroom)
        housing_mask = (
            df["Type"].isin(PROPERTY_RESIDENTIAL_TYPES)
            | (df["Type"].isin(["Farm", "Estate"]) & has_dwelling)
        )
        
        left = left[housing_mask.to_numpy()]

    left = left.dropna(subset=["_date"])
    right = right.dropna(subset=["_end", "_value"])

    if by:
        left = left.dropna(subset=["_region"])
        right = right.dropna(subset=["_region"])

    merged = pd.merge_asof(
        left.sort_values("_date"),
        right.sort_values("_end"),
        left_on="_date",
        right_on="_end",
        by=by,
        allow_exact_matches=False,
    )

    df[new_col_name] = (
        merged.set_index("_pos")["_value"]
        .reindex(np.arange(len(df)))
        .to_numpy()
    )

    return df


"""
This function generates a dataset from a Pandas dataframe (df) and
saves it to a file in the specified format and in a path defined by 'file_path_base'
It saves in 'CSV' or 'parquet' formats, depending on the 'dataset_format' parameter

"""
def generate_dataset_from_df(df, file_path_base, dataset_format):
    
    if not dataset_format or dataset_format not in ["csv", "parquet"]:
        raise ValueError("The 'dataset_format' parameter must be provided and cannot be None.")
    
    file_path = f"{file_path_base}.{dataset_format}"
    
    os.makedirs(Path(file_path).parent, exist_ok=True)
    
    if dataset_format == "csv":
        df.to_csv(file_path, index=False)
    
    elif dataset_format == "parquet":
        df.to_parquet(file_path, index=False)


"""
This function returns a Pandas dataframe from the local dataset specified by 'file_path_base' and in the 
format specified by 'dataset_format'

"""
def generate_df_from_dataset(file_path_base, dataset_format):
    
    if not dataset_format:
        raise ValueError("The 'dataset_format' parameter must be provided and cannot be None.")
        
    file_path = f"{file_path_base}.{dataset_format}"
    
    if dataset_format == "csv":
        return pd.read_csv(file_path)
    
    elif dataset_format == "parquet":
        return pd.read_parquet(file_path)


"""
Generic method to transform data rage in a specific format and return two strings with the start date and the end date

    dt_string = "January 2022" (example)
    returns two dates: the first day of the month and the last day of the month
    for example; '2022-01-01' and '2022-01-31'
    
"""
def transform_data_to_range(dt_string):
    
    ### FOR MONTHLY FORMATS
    
    # Pattern ('Month' 'Year'); example: "January 2022"
    match_month_year = re.fullmatch(
        r"(January|February|March|April|May|June|July|August|"
        r"September|October|November|December) (\d{4})",
        dt_string
    )
    
    # Pattern 'YYYY-MM'
    match_yyyy_mm = re.fullmatch(r"(\d{4})-(\d{2})", dt_string)
    
    if match_month_year or match_yyyy_mm:
        
        if match_month_year:
        
            month_name, year = match_month_year.groups()
        
            month_number = {
                "January": 1,
                "February": 2,
                "March": 3,
                "April": 4,
                "May": 5,
                "June": 6,
                "July": 7,
                "August": 8,
                "September": 9,
                "October": 10,
                "November": 11,
                "December": 12
            }
            
            month = month_number[month_name]
            
        elif match_yyyy_mm:
            year, month = match_yyyy_mm.groups()
            month = int(month)
            
        year = int(year)
        
        last_day = calendar.monthrange(year, month)[1]
        
        return f"{year}-{month:02d}-01", f"{year}-{month:02d}-{last_day}"
    
    
    
    ### FOR YEAR FORMATS
    
    # Pattern 'Year'; example: "2023"
    match_year = re.fullmatch(r"(\d{4})", dt_string)
    
    if match_year:
        year = int(match_year.group())
        return f"{year}-01-01", f"{year}-12-31"
    
    
    
    ### FOR TRIMESTER FORMATS
    
    # "1st Quarter 2026"
    match_extended_trimester = re.fullmatch(
        r"(1st|2nd|3rd|4th) Quarter (\d{4})",
        dt_string
    )
    
    # Format 'YYYY-QQ'
    match_yyyy_qq = re.fullmatch(r"(\d{4})-Q(\d{1})", dt_string)
    
    if match_extended_trimester or match_yyyy_qq:
        
        if match_extended_trimester:
        
            trimester, year = match_extended_trimester.groups()
        
            trimester_number = {
                "1st": 1,
                "2nd": 4,
                "3rd": 7,
                "4th": 10
            }
            
        elif match_yyyy_qq:
            
            year, trimester = match_yyyy_qq.groups()
            
            trimester_number = {
                "1": 1,
                "2": 4,
                "3": 7,
                "4": 10
            }
            
        trimester_number = trimester_number[trimester]
            
        year = int(year)
        
        last_day = calendar.monthrange(year, trimester_number + 2)[1]
        
        return f"{year}-{trimester_number:02d}-01", f"{year}-{trimester_number + 2:02d}-{last_day}"
    
    
    
    ### FOR SEMESTER FORMATS
    
    # For format "1st Semester 2026"
    match_semester = re.fullmatch(
        r"(1st|2nd) Semester (\d{4})",
        dt_string
    )
    
    # For format "YYYY-S1" or "YYYY-S2"
    match_yyyy_ss = re.fullmatch(r"(\d{4})-S(\d{1})", dt_string)
    
    if match_semester or match_yyyy_ss:
        
        if match_semester:
        
            semester, year = match_semester.groups()
        
            semester_number = {
                "1st": 1,
                "2nd": 7
            }
        
        if match_yyyy_ss:
            
            year, semester = match_yyyy_ss.groups()
            
            semester_number = {
                "1": 1,
                "2": 7
            }
        
        year = int(year)
        
        semester_number = semester_number[semester]
        
        last_day = calendar.monthrange(year, semester_number + 5)[1]
        
        return f"{year}-{semester_number:02d}-01", f"{year}-{semester_number + 5:02d}-{last_day}"
    

