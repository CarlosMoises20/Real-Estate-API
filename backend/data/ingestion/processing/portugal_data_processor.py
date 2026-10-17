
import pandas as pd
from backend.data.ingestion.source.api.ine import INE
from backend.data.ingestion.processing.base_country_data_processor import BaseCountryDataProcessor
from backend.common.constants import COLUMN_RENAME_MAP, DATASETS_PATH_BASE
from backend.common.utils import generate_dataset_from_df, join_df_with_external_data, convert_pd_df_columns_to_datetime, build_translate_names
from backend.common.dataset_names import *


"""This class is used to process data related to Portugal"""
class PortugalDataProcessor(BaseCountryDataProcessor):
    
    """Constructor for the PortugalDataProcessor class"""
    def __init__(self, datasets_format="parquet"):
        super().__init__(datasets_format=datasets_format)
        self._country_code = "PT"
  

    """Method used to aggregate data with internal factors, from several data sources"""
    def _aggregate_internal_data(self):
        
        # Read CSV Kaggle dataset from the local datasets
        df_kaggle = pd.read_csv(
            filepath_or_buffer=f"{self._get_datasets_path(data_type='internal')}/portugal_listinigs.csv", 
            sep=",", 
            encoding="utf-8"
        )
        
        df_kaggle = df_kaggle.drop_duplicates()
        
        # Remove properties outside of Portugal
        outside_pt_mask = df_kaggle["District"] == "Z - Fora de Portugal"
        
        df_internal = df_kaggle[~outside_pt_mask]
        
        # NOTE if, in the future, this logic is implemented in another place on the project, create a generic function for this and then here we call that function
        # Move properties outside of Portugal to separate datasets representing their corresponding country
        # (specified on the attributes "District" and "Town")
        df_outside_pt = df_kaggle[outside_pt_mask]
        
        translate_names = build_translate_names(original_language="pt")
        
        for district_col_value, df_prop_outside_pt in df_outside_pt.groupby("City"):
            
            country_name = translate_names.get(district_col_value, None)

            if country_name is None:
                print(f"Unknown country or district: {district_col_value}")
                continue
            
            country_name = country_name.lower().replace(" ", "_")

            generate_dataset_from_df(df=df_prop_outside_pt,
                                     file_path_base=f"{DATASETS_PATH_BASE}/{country_name}/internal/other_properties",
                                     dataset_format=self._datasets_format)
        
        
        # TODO gather data from Idealista
        df_idealista = pd.DataFrame()
        
        df_returned_list = [df_internal, df_idealista]
        
        df_list = [df.rename(columns=COLUMN_RENAME_MAP) for df in df_returned_list]
        
        # Concatenate the dataframes 
        df_internal = pd.concat(df_list, ignore_index=True)
    
        # Remove duplicated entries and irrelevant attributes
        df_internal = df_internal.drop_duplicates()
        
        # Convert all boolean attributes to integer
        df_internal = df_internal.map(lambda x: int(x) if isinstance(x, bool) else x)
        
        # Drop redundant attribute: EnergyEfficiencyLevel
        df_internal = df_internal.drop(columns=["EnergyEfficiencyLevel"])
        
        # for some negative values, transform those into positive values by applying the absolute value
        for attr_name in ["Living Area (m2)", "Total Area (m2)", "Built Area (m2)",
                            "NumberOfBathrooms", "NumberOfWC"]:
            
            df_internal[attr_name] = df_internal[attr_name].abs()
            
        convert_pd_df_columns_to_datetime(df=df_internal, cols=["PublishDate"], format="mixed")
        
        # Split the data into training and testing sets (Train-Test Split)
        return df_internal
        

    """Method used to aggregate data with external factors, from several data sources"""
    def _aggregate_external_data(self):
        
        ### Eurostat GDP dataset with data related to GDP per capita in Portugal since 2010
        ### because the oldest property in the Kaggle dataset with Portugal data is from 2010
        df_eurostat = super()._read_dataset(
            name=get_eurostat_dataset_name(
                dataset_code="namq_10_gdp", 
                country_code=self._get_country_code(), 
                time_period="ge:2009"
            ), 
            data_type="external"
        )
        
        ### FSQ Places        
        df_fsq_os_places = super()._read_dataset(
            name=get_fsq_places_dataset_name(country_code=self._get_country_code()), 
            data_type="external"
        )
        
        ### INE data related to inflation (homologous variation) in Portugal
        df_ine_inflation_growth_rate = super()._read_dataset(
            name=get_ine_dataset_name(value_attr_name="inflation_growth_rate"), 
            data_type="external"
        )
        
        ### INE data related to housing credit rate in Portugal
        df_ine_housing_credit_rate = super()._read_dataset(
            name=get_ine_dataset_name(value_attr_name="housing_credit_rate"), 
            data_type="external"
        )
        
        ### INE data related to average salary in Portugal
        df_ine_avg_salary = super()._read_dataset(
            name=get_ine_dataset_name(value_attr_name="avg_salary_euros"), 
            data_type="external"
        )
        
        ### INE gross disposable income (€)
        df_ine_gross_disposable_income = super()._read_dataset(
            name=get_ine_dataset_name(value_attr_name="gross_disposable_income_euros"), 
            data_type="external"
        )
        
        ### INE data related to unemployment rate in Portugal   
        df_ine_unemployment_rate = super()._read_dataset(
            name=get_ine_dataset_name("unemployment_rate"), 
            data_type="external"
        )
        
        ### INE data related to number of housing transactions in Portugal
        df_ine_housing_sold_num_transactions = super()._read_dataset(
            name=get_ine_dataset_name("housing_sold_num_transactions"), 
            data_type="external"
        )
        
        ### INE data related to housing price per square meter (euros) in Portugal
        df_ine_housing_price_per_m2_euros = super()._read_dataset(
            name=get_ine_dataset_name("housing_price_per_m2_euros"), 
            data_type="external"
        )
        
        ### INE data related to crime rate in Portugal
        df_ine_crime_rate = super()._read_dataset(
            name=get_ine_dataset_name("crime_rate"), 
            data_type="external"
        )
            
        result = {
            "INE (Inflation - Homologous variation)": df_ine_inflation_growth_rate,
            "INE (Housing credit rate)": df_ine_housing_credit_rate,
            "INE (Average salary)": df_ine_avg_salary,
            "INE (Gross Disposable Income - Euros)": df_ine_gross_disposable_income,
            "INE (Unemployment rate (%))": df_ine_unemployment_rate,
            "INE (Housing sold, number of transactions)": df_ine_housing_sold_num_transactions,
            "INE (Housing price per square meter - Euros)": df_ine_housing_price_per_m2_euros,
            "INE (Crime rate)": df_ine_crime_rate,
            "Eurostat GDP": df_eurostat,
            "FSQ Places": df_fsq_os_places
        }
        
        # convert date_start and date_end to datetime format before the JOIN
        for name, df_ext in result.items():
            
            if name == "FSQ Places":
                continue
            
            convert_pd_df_columns_to_datetime(df=df_ext, cols=["date_start", "date_end"])
        
        return result
      

    """Method used to update datasets by fetching data from different sources, including APIs and Kaggle datasets"""
    def update_datasets(self):

        # Download CSV Kaggle dataset from the link
        # https://www.kaggle.com/datasets/luvathoms/portugal-real-estate-2024
        # This dataset contains real estate data properties (internal factors) from Portugal        
        super()._download_kaggle(
            handle="luvathoms/portugal-real-estate-2024", 
            filename="portugal_listinigs.csv",
            data_type="internal"
        )

        # Instituto Nacional de Estatística (INE)
        ine = INE(
            datasets_format=self._datasets_format,
            datasets_path=self._get_datasets_path(data_type="external")
        )
        
        ine.get_api_data()
        
        # TODO Banco de Portugal
        
        # API Reference: https://ec.europa.eu/eurostat/web/user-guides/data-browser/api-data-access/api-detailed-guidelines/api-statistics
        # SMDX-2.0 CSV
        super()._update_eurostat(time_period="ge:2009")
        

        # Foursquare OS Places API Reference: https://docs.foursquare.com/data-products/docs/fsq-places-open-source
        super()._update_fsq_places()
        
        
        # update API with final dataset
        self.join_and_save_data()
        
    
    """Method to join the datasets and save them to a final dataset to be directly consumed by the API"""     
    def join_and_save_data(self):
        
        # Aggregate external data
        df_external_list_dict = self._aggregate_external_data()
        
        # Final dataset starts with data from internal factors
        df_final = self._aggregate_internal_data()
        
        
        ### Join GDP data from Eurostat with final dataset
        
        df_gdp = df_external_list_dict["Eurostat GDP"]
        
        df_gdp_market_prices = df_gdp[df_gdp["na_item"] == "B1GQ"]
        
        df_gdp_market_growth_output_col = "gdp_growth_rate"
        
        df_final = join_df_with_external_data(df=df_final, 
                                         df_external=df_gdp_market_prices, 
                                         old_col_name="OBS_VALUE", 
                                         new_col_name=df_gdp_market_growth_output_col)
        
        df_gdp_final_consumption = df_gdp[df_gdp["na_item"] == "P31_S14"]
        
        df_gdp_final_cons_output_col = "household_consumption_growth_rate"
        
        df_final = join_df_with_external_data(df=df_final, 
                                         df_external=df_gdp_final_consumption, 
                                         old_col_name="OBS_VALUE", 
                                         new_col_name=df_gdp_final_cons_output_col)
        
        
        ### INFLATION GROWTH RATE (Homologous variation)
        
        df_inflation = df_external_list_dict["INE (Inflation - Homologous variation)"]
        
        # Filter by geodsg=Portugal (contains results from Portugal instead of being specific
        # to the continent; the difference is almost irrelevant) and dim_3_t=Total, since
        # it aggregates the inflation results from every category
        df_inflation = df_inflation[df_inflation["geodsg"] == "Portugal"]
        
        inflation_col = "inflation_growth_rate"
        
        df_final = join_df_with_external_data(df=df_final,
                                         df_external=df_inflation, 
                                         old_col_name="inflation_growth_rate", 
                                         new_col_name=inflation_col)
        
        
        ### HOUSING CREDIT RATE
        
        df_ine_housing_credit_rate = df_external_list_dict["INE (Housing credit rate)"]
        
        housing_credit_rate_col_name = "housing_credit_rate"
        
        df_final = join_df_with_external_data(df=df_final,
                                         df_external=df_ine_housing_credit_rate, 
                                         old_col_name=housing_credit_rate_col_name, 
                                         new_col_name=housing_credit_rate_col_name,
                                         right_region_col="geodsg",
                                         property_specific=True)
        
        
        ### AVERAGE SALARY (€)
        
        df_ine_avg_salary = df_external_list_dict["INE (Average salary)"]
        
        avg_salary_col_name = "avg_salary_euros"
        
        df_final = join_df_with_external_data(df=df_final,
                                         df_external=df_ine_avg_salary, 
                                         old_col_name=avg_salary_col_name, 
                                         new_col_name=avg_salary_col_name)
        
        
        ### GROSS DISPOSABLE INCOME (€)
                
        df_gross_disposable_income = df_external_list_dict["INE (Gross Disposable Income - Euros)"]
        
        gross_disposable_income_col_name = "gross_disposable_income_euros"
        
        df_final = join_df_with_external_data(df=df_final,
                                            df_external=df_gross_disposable_income, 
                                            old_col_name=gross_disposable_income_col_name, 
                                            new_col_name=gross_disposable_income_col_name,
                                            right_region_col="geodsg",
                                            location_mapping=True)
        
        
        ### UNEMPLOYMENT RATE (%) 
        
        df_ine_unemployment_rate = df_external_list_dict["INE (Unemployment rate (%))"]
        
        unemp_rate_col_name = "unemployment_rate"
        
        df_final = join_df_with_external_data(df=df_final,
                                         df_external=df_ine_unemployment_rate, 
                                         old_col_name=unemp_rate_col_name, 
                                         new_col_name=unemp_rate_col_name,
                                         right_region_col="geodsg",
                                         location_mapping=True)
        
        
        ### HOUSING SOLD (NUMBER OF TRANSACTIONS)
        
        df_ine_housing_sold_num_transactions = df_external_list_dict["INE (Housing sold, number of transactions)"]
        
        housing_sold_transactions_col_name = "housing_sold_num_transactions"
        
        df_final = join_df_with_external_data(df=df_final,
                                         df_external=df_ine_housing_sold_num_transactions, 
                                         old_col_name=housing_sold_transactions_col_name, 
                                         new_col_name=housing_sold_transactions_col_name,
                                         right_region_col="geodsg",
                                         property_specific=True,
                                         location_mapping=True)
        
        ### PRICE PER SQUARE METER (€) # TODO review mapping
        
        df_ine_price_per_square_meter = df_external_list_dict["INE (Housing price per square meter - Euros)"]
        
        price_per_square_meter_col_name = "housing_price_per_m2_euros"
        
        df_final = join_df_with_external_data(df=df_final,
                                         df_external=df_ine_price_per_square_meter, 
                                         old_col_name=price_per_square_meter_col_name, 
                                         new_col_name=price_per_square_meter_col_name,
                                         #left_region_col="Town",       # TODO review, some values are in Town, others in City
                                         right_region_col="geodsg",
                                         property_specific=True)
        
        
        ### CRIME RATE
        
        df_ine_crime_rate = df_external_list_dict["INE (Crime rate)"]
        
        crime_rate_col_name = "crime_rate"
        
        df_final = join_df_with_external_data(df=df_final,
                                                 df_external=df_ine_crime_rate, 
                                                 old_col_name=crime_rate_col_name, 
                                                 new_col_name=crime_rate_col_name,
                                                 #left_region_col="Town",       # TODO review, some values are in Town, others in City
                                                 right_region_col="geodsg",
                                                 property_specific=True)
        
        ### TODO FSQ OS PLACES (FACILITIES)
        
        df_fsq_places = df_external_list_dict["FSQ Places"]
    


        
        # Reorder the columns in the desired order for the final dataframe 
        # Standard column order for the final dataset.
        # Keeping a fixed order makes the resulting dataset easier to inspect,
        # process, and use consistently throughout the machine learning pipeline.
        COLUMN_ORDER = [
            # Property type
            "Type",
    
            # Location
            "District", "City", "Town",
    
            # Property characteristics
            "NumberOfBedrooms", "NumberOfBathrooms", "NumberOfWC", "TotalRooms",
    
            # Areas
            "Built Area (m2)", "Living Area (m2)", "Total Area (m2)", "LotSize",
    
            # Building characteristics
            "Floor", "Elevator", "Garage", "ConstructionYear", "Parking",
    
            # Energy
            "EnergyCertificate", "ElectricCarsCharging",
    
            # Conservation
            "ConservationStatus",
    
            # Publish date
            "PublishDate",
            
            # GDP growth rate
            df_gdp_market_growth_output_col,
            
            # Final consumption expenditure of household
            df_gdp_final_cons_output_col,
            
            # Inflation (homologous variable)
            inflation_col,
            
            # Average salary (euros)
            avg_salary_col_name,
            
            # Housing credit rate
            housing_credit_rate_col_name,
            
            # Gross disposable income (euros)
            gross_disposable_income_col_name,
            
            # Unemployment rate (%)
            unemp_rate_col_name,
            
            # Housing sold (number of transactions)
            housing_sold_transactions_col_name,
            
            # Price per square meter (euros)
            price_per_square_meter_col_name,
            
            # Crime rate
            crime_rate_col_name,
            
            # TODO FSQ OS Places (Facilities)
    
            # Target (price)
            "Price (euros)"
        ]
        
        dropped = [c for c in df_final.columns if c not in COLUMN_ORDER]
        
        if dropped:
            print(f"Colunas descartadas pelo COLUMN_ORDER: {dropped}")
            
        df_final = df_final[COLUMN_ORDER]
        
        # Save the final dataframe in the format indicated by 'datasets_format' (CSV or Parquet)         
        # TODO check "v1" in the end to remove, this is only for testing and to not remove the original one   
        generate_dataset_from_df(df=df_final, 
                                file_path_base=f"{self._get_datasets_path(data_type='final')}/{get_final_dataset_name(self._get_country_code())}_v1",
                                dataset_format=self._datasets_format)
        
        return df_final
        
        
# This script is executed once per day 
# to update the data (including local datasets) to be consumed by the API
if __name__ == "__main__":
    
    pt = PortugalDataProcessor(datasets_format="parquet")
    
    # PARQUET format is more efficient for large datasets, 
    # but CSV format is more compatible with other tools and easier to read and edit manually
    
    # PARQUET format
    #pt.update_datasets()
    
    #pt.join_and_save_data()
    
    pt.__setattr__("_datasets_format", "csv")
    
    # CSV format
    pt.update_datasets() 
    
    #pt.join_and_save_data()
    
    """scheduler = BackgroundScheduler()

    scheduler.add_job(
        update_datasets,
        CronTrigger(
            hour=3,
            minute=0,
            timezone="Europe/Lisbon",
        ),
        id="daily_dataset_update",
    )

    scheduler.start()

    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()"""