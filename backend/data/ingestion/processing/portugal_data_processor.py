
import pandas as pd
from backend.data.ingestion.source.api.ine import INE
from backend.data.ingestion.processing.base_country_data_processor import BaseCountryDataProcessor
from backend.common.constants import COLUMN_RENAME_MAP, DATASETS_PATH_BASE
from backend.common.utils import generate_dataset_from_df, join_df_with_external_data, convert_pd_df_columns_to_datetime, build_translate_names, keep_city_level
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
        
        # Drop redundant attribute: EnergyEfficiencyLevel
        df_internal = df_internal.drop(columns=["EnergyEfficiencyLevel"])
        
        # for some negative values, transform those into positive values by applying the absolute value
        for attr_name in ["Living Area (m2)", "Total Area (m2)", 
                            "Built Area (m2)", "NumberOfBathrooms", "NumberOfWC"]:
            
            df_internal[attr_name] = df_internal[attr_name].abs()
            
        convert_pd_df_columns_to_datetime(df=df_internal, cols=["PublishDate"], format="mixed")
        
        # Split the data into training and testing sets (Train-Test Split)
        return df_internal
        

    """Method used to aggregate data with external factors, from several data sources"""
    def _aggregate_external_data(self):
        
        ### Eurostat GDP dataset with data related to GDP per capita in Portugal since 2009
        ### because the oldest property in the Kaggle dataset with Portugal data is from 2010
        df_gdp = super()._read_dataset(
            name=get_eurostat_dataset_name(
                dataset_code="namq_10_gdp", 
                country_code=self._get_country_code(), 
                time_period="ge:2009"
            ), 
            data_type="external"
        )
        
        ### FSQ Places        
        df_fsq_places = super()._read_dataset(
            name=get_fsq_places_dataset_name(country_code=self._get_country_code()), 
            data_type="external"
        )
        
        ### ECB data related to housing credit rate in Portugal
        df_housing_credit_rate = super()._read_dataset(
            name=get_ecb_dataset_name(value_attr_name="housing_credit_rate"), 
            data_type="external"
        )
        
        ### INE data related to inflation (homologous variation) in Portugal
        df_inflation = super()._read_dataset(
            name=get_ine_dataset_name(value_attr_name="inflation_growth_rate"), 
            data_type="external"
        )
        
        ### INE data related to average salary in Portugal
        df_avg_salary = super()._read_dataset(
            name=get_ine_dataset_name(value_attr_name="avg_salary_euros"), 
            data_type="external"
        )
        
        ### INE data related to unemployment rate in Portugal   
        df_unemployment_rate = super()._read_dataset(
            name=get_ine_dataset_name("unemployment_rate"), 
            data_type="external"
        )
        
        ### INE data related to number of housing transactions in Portugal
        df_housing_transactions = super()._read_dataset(
            name=get_ine_dataset_name("housing_num_transactions"), 
            data_type="external"
        )
        
        ### INE data related to housing price per square meter (euros) in Portugal
        df_housing_price_per_m2 = super()._read_dataset(
            name=get_ine_dataset_name("housing_price_per_m2_euros"), 
            data_type="external"
        )
        
        ### INE data related to crime rate in Portugal
        
        ## Retrieve data from 1998 to 2013
        df_crime_rate_1998_2013 = super()._read_dataset(
            name=get_ine_dataset_name("crime_rate_from_1998_to_2013"), 
            data_type="external"
        )
        
        # Filter that data to keep only the data from 2009 to 2010
        df_crime_rate_2009_2010 = df_crime_rate_1998_2013[
            (pd.to_datetime(df_crime_rate_1998_2013["date_start"]) >= "2009-01-01") &
            (pd.to_datetime(df_crime_rate_1998_2013["date_end"]) <= "2010-12-31")
        ]
        
        ## Retrieve data from 2011 to 2022
        df_crime_rate_2011_2022 = super()._read_dataset(
            name=get_ine_dataset_name("crime_rate_from_2011_to_2022"), 
            data_type="external"
        )
        
        # Filter that data to keep only the data from 2011 to 2020
        df_crime_rate_2011_2020 = df_crime_rate_2011_2022[
            pd.to_datetime(df_crime_rate_2011_2022["date_end"]) <= "2020-12-31"
        ]
        
        ## Retrieve data from 2021 to 2025
        df_crime_rate_2021_2025 = super()._read_dataset(
            name=get_ine_dataset_name("crime_rate_from_2021_to_2025"), 
            data_type="external"
        )
        
        # Join crime data in a single dataset (from 2009 to 2025)
        df_crime_rate = pd.concat([
            df_crime_rate_2009_2010, 
            df_crime_rate_2011_2020, 
            df_crime_rate_2021_2025
        ], ignore_index=True)
        
        ### Generate final crime dataset
        generate_dataset_from_df(df=df_crime_rate, 
                                 file_path_base=f"{self._get_datasets_path(data_type='external')}/{get_ine_dataset_name('crime_rate')}", 
                                 dataset_format=self._datasets_format)
        
        # TODO observe the final dataset before applying these changes
        """g = df_ine_crime_rate["geocod"].astype(str)
        df_ine_crime_rate.loc[g.str.startswith("200") & df_ine_crime_rate.geodsg.isin(["Calheta", "Lagoa"]), "geodsg"] += ' (R.A.A.)'
        df_ine_crime_rate.loc[g.str.startswith("300") & (df_ine_crime_rate.geodsg == "Calheta"), "geodsg"] = 'Calheta (R.A.M.)'
        df_ine_crime_rate.loc[g.str.startswith("150") & (df_ine_crime_rate.geodsg == "Lagoa"), "geodsg"] = 'Lagoa (Algarve)'"""
            
        result = {
            "Inflation": df_inflation,
            "Average Salary (€)": df_avg_salary,
            "Unemployment Rate": df_unemployment_rate,
            "Number of Housing Transactions": df_housing_transactions,
            "Housing Price per m2 (€)": df_housing_price_per_m2,
            "Crime rate": df_crime_rate,
            "Housing credit rate": df_housing_credit_rate,
            "GDP": df_gdp,
            "FSQ Places": df_fsq_places
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
        
        # Europan Central Bank (ECB)
        super()._update_ecb()
        
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
        
        df_gdp = df_external_list_dict["GDP"]
        
        
        # GDP (Quarterly Variation)
        
        df_gdp_qoq = df_gdp[(df_gdp["na_item"] == "B1GQ") & (df_gdp["unit"] == "CLV_PCH_PRE")]      
        
        df_gdp_qoq_col = "GDP_QoQ"
        
        df_final = join_df_with_external_data(df=df_final, 
                                            df_external=df_gdp_qoq, 
                                            old_col_name="OBS_VALUE", 
                                            new_col_name=df_gdp_qoq_col,
                                            publication_lag_days=45)
        
        
        # GDP (Homologous Variation)
        # NOTE: Homologous variation is important to capture sazonal changes without the noise 
        # of the quarterly variation; This metric is more stable and it's the way how the main numbers are published
        
        df_gdp_yoy = df_gdp[(df_gdp["na_item"] == "B1GQ") & (df_gdp["unit"] == "CLV_PCH_SM")]
        
        df_gdp_yoy_col = "GDP_yoy"
        
        df_final = join_df_with_external_data(df=df_final, 
                                         df_external=df_gdp_yoy, 
                                         old_col_name="OBS_VALUE", 
                                         new_col_name=df_gdp_yoy_col,
                                         publication_lag_days=45)
        
        
        # Final consumption expenditure of household (Quarterly Variation)
                
        df_hh_cons_qoq = df_gdp[(df_gdp["na_item"] == "P31_S14") & (df_gdp["unit"] == "CLV_PCH_PRE")]
                
        df_hh_cons_qoq_col = "HouseholdConsumption_QoQ"
        
        df_final = join_df_with_external_data(df=df_final, 
                                            df_external=df_hh_cons_qoq, 
                                            old_col_name="OBS_VALUE", 
                                            new_col_name=df_hh_cons_qoq_col,
                                            publication_lag_days=65)
        
        
        # Final consumption expenditure of household (Homologous Variation)
        
        df_hh_cons_yoy = df_gdp[(df_gdp["na_item"] == "P31_S14") & (df_gdp["unit"] == "CLV_PCH_SM")]
        
        df_hh_cons_yoy_col = "HouseholdConsumption_YoY"
        
        df_final = join_df_with_external_data(df=df_final, 
                                         df_external=df_hh_cons_yoy, 
                                         old_col_name="OBS_VALUE", 
                                         new_col_name=df_hh_cons_yoy_col,
                                         publication_lag_days=65)
        
        
        ### INFLATION GROWTH RATE (Homologous variation)
        
        df_inflation = df_external_list_dict["Inflation"]
        
        # Filter by geodsg=Portugal (contains results from Portugal instead of being specific
        # to the continent; the difference is almost irrelevant) and dim_3_t=Total, since
        # it aggregates the inflation results from every category
        df_inflation = df_inflation[df_inflation["geodsg"] == "Portugal"]
        
        inflation_col = "InflationGrowthRate"
        
        df_final = join_df_with_external_data(df=df_final,
                                         df_external=df_inflation, 
                                         old_col_name=inflation_col, 
                                         new_col_name=inflation_col,
                                         publication_lag_days=15)
        
        
        ### HOUSING CREDIT RATE
        
        df_housing_credit_rate = df_external_list_dict["Housing credit rate"]
        
        housing_credit_rate_col = "HousingCreditRate"
        
        df_final = join_df_with_external_data(df=df_final,
                                         df_external=df_housing_credit_rate, 
                                         old_col_name=housing_credit_rate_col, 
                                         new_col_name=housing_credit_rate_col,
                                         property_specific=True,
                                         publication_lag_days=35)
        
        
        ### AVERAGE SALARY (€)
        
        df_avg_salary = df_external_list_dict["Average Salary (€)"]
        
        # We will keep this only for the API
        avg_salary_col = "AvgSalary_Euros"
        
        df_final = join_df_with_external_data(df=df_final,
                                         df_external=df_avg_salary, 
                                         old_col_name=avg_salary_col, 
                                         new_col_name=avg_salary_col,
                                         publication_lag_days=45)
        
        s = df_avg_salary["AvgSalary_Euros"]
        
        # Calculates the variation of the average salary, ignoring the sazonal variations
        df_avg_salary["AvgSalary_12m_avg_Euros"] = (s + s.shift(3) + s.shift(6) + s.shift(9)) / 4
        
        df_avg_salary = df_avg_salary.drop(columns=["avg_salary_euros"]) \
                                     .dropna(subset=["AvgSalary_12m_avg_Euros"])
        
        # NOTE only for testing
        df_avg_salary.to_csv(f"{self._get_datasets_path(data_type='external')}/{get_ine_dataset_name('avg_salary_euros_12_month_average')}.csv",
                                            index=False)
        
        # We will keep this only for the Machine Learning models, not the API
        avg_salary_hom_var_col = "AvgSalary_12m_avg_Euros"
        
        df_final = join_df_with_external_data(df=df_final,
                                                df_external=df_avg_salary, 
                                                old_col_name=avg_salary_hom_var_col, 
                                                new_col_name=avg_salary_hom_var_col,
                                                publication_lag_days=45)
        
        
        
        ### NUMBER OF HOUSING TRANSACTIONS
        
        df_housing_transactions = df_external_list_dict["Number of Housing Transactions"]
        
        housing_num_trans_col = "HousingNumTransactions"
        
        df_final = join_df_with_external_data(df=df_final,
                                         df_external=df_housing_transactions, 
                                         old_col_name=housing_num_trans_col, 
                                         new_col_name=housing_num_trans_col,
                                         right_region_col="geodsg",
                                         property_specific=True,
                                         location_mapping=True,
                                         publication_lag_days=85)
        
        
        
        # HOUSING TRANSACTIONS (Homologous Variation of the last 4 quarters)

        housing_num_trans_yoy_col = "HousingNumTransactions_4Q_YoY"

        # Remove duplicated regions (e.g. Açores appears with geocod 2 and 20 with the same values)
        df_housing_transactions = df_housing_transactions.drop_duplicates(["geodsg", "date_end"]) \
                                                        .sort_values(["geodsg", "date_end"])

        # Number of transactions in the last 4 quarters (last 12 months), per region, removing seasonality
        trans_4q_sum = df_housing_transactions.groupby("geodsg")[housing_num_trans_col] \
                                            .transform(lambda s: s.rolling(4).sum())

        # Year-on-year growth rate (%) of the last 4 quarters compared with the 4 quarters before
        trans_4q_sum_prev_year = trans_4q_sum.groupby(df_housing_transactions["geodsg"]).shift(4)

        df_housing_transactions[housing_num_trans_yoy_col] = (trans_4q_sum / trans_4q_sum_prev_year - 1) * 100

        df_housing_transactions = df_housing_transactions.dropna(subset=[housing_num_trans_yoy_col])

        df_final = join_df_with_external_data(df=df_final,
                                        df_external=df_housing_transactions, 
                                        old_col_name=housing_num_trans_yoy_col, 
                                        new_col_name=housing_num_trans_yoy_col,
                                        right_region_col="geodsg",
                                        property_specific=True,
                                        location_mapping=True,
                                        publication_lag_days=85)

        
        
        ### UNEMPLOYMENT RATE (%)
        
        df_unemployment_rate = df_external_list_dict["Unemployment Rate"]
        
        unemp_rate_col = "UnemploymentRate"
        
        df_final = join_df_with_external_data(df=df_final,
                                         df_external=df_unemployment_rate, 
                                         old_col_name=unemp_rate_col, 
                                         new_col_name=unemp_rate_col,
                                         right_region_col="geodsg",
                                         location_mapping=True,
                                         publication_lag_days=40)
        
        
        ### PRICE PER SQUARE METER (€)
        
        df_price_per_m2 = df_external_list_dict["Housing Price per m2 (€)"]
        
        price_per_m2_col = "HousingPricePerM2_Euros"

        df_price_per_m2 = keep_city_level(df_price_per_m2)
        
        df_final = join_df_with_external_data(df=df_final,
                                            df_external=df_price_per_m2, 
                                            old_col_name=price_per_m2_col, 
                                            new_col_name=price_per_m2_col,
                                            right_region_col="geodsg",
                                            property_specific=True,
                                            publication_lag_days=115)
        
        
        ### CRIME RATE
        
        df_crime_rate = df_external_list_dict["Crime rate"]
        
        crime_rate_col = "CrimeRate"

        df_crime_rate = keep_city_level(df_crime_rate)
        
        df_final = join_df_with_external_data(df=df_final,
                                            df_external=df_crime_rate, 
                                            old_col_name=crime_rate_col, 
                                            new_col_name=crime_rate_col,
                                            right_region_col="geodsg",
                                            publication_lag_days=185)
        
        
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
            
            # GDP (quarterly variation)
            df_gdp_qoq_col,
            
            # GDP (homologous variation)
            df_gdp_yoy_col,
            
            # Final consumption expenditure of household (quarterly variation)
            df_hh_cons_qoq_col,
            
            # Final consumption expenditure of household (homologous variation)
            df_hh_cons_yoy_col,
            
            # Inflation (homologous variable)
            inflation_col,
            
            # Average salary (euros)
            avg_salary_col,
            
            # Average salary 12-month average (euros)
            avg_salary_hom_var_col,
            
            # Housing credit rate
            housing_credit_rate_col,
            
            # Unemployment Rate (%)
            unemp_rate_col,
            
            # Number of housing transactions
            housing_num_trans_col,
            
            # Number of housing transactions (homologous variation)
            housing_num_trans_yoy_col,
            
            # Price per square meter (euros)
            price_per_m2_col,
            
            # Crime rate
            crime_rate_col,
            
            # TODO FSQ OS Places (Facilities)
    
            # Target (price)
            "Price_Euros"
        ]
            
        df_final = df_final[COLUMN_ORDER]
        
        # Save the final dataframe in the format indicated by 'datasets_format' (CSV or Parquet)
        generate_dataset_from_df(df=df_final, 
                                file_path_base=f"{self._get_datasets_path(data_type='final')}/{get_final_dataset_name(self._get_country_code())}",
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