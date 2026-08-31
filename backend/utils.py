
import re, calendar


"""
This function generates a dataset from a dataframe and
saves it to a file in the specified format and in a path defined by 'file_path_base'

"""
def generate_dataset_from_df(df, file_path_base, dataset_format):
    
    if dataset_format:
        
        file_path = f"{file_path_base}.{dataset_format}"
        
        if dataset_format == "csv":
            df.to_csv(file_path, index=False)
        
        elif dataset_format == "parquet":
            df.to_parquet(file_path, index=False)
        



# dt_string = "Janeiro de 2022" (example)
# returns two dates: the first day of the month and the last day of the month
# for example; '2022-01-01' and '2022-01-31'
def transform_data_to_range(dt_string):
    
    # Pattern ('Month' de 'Year'); example: "Janeiro de 2022"
    match_month_year = re.fullmatch(
        r"(Janeiro|Fevereiro|Março|Abril|Maio|Junho|Julho|Agosto|"
        r"Setembro|Outubro|Novembro|Dezembro) de (\d{4})",
        dt_string
    )
    
    # Pattern 'YYYY-MM'
    match_yyyy_mm = re.fullmatch(r"(\d{4})-(\d{2})", dt_string)
    
    if match_month_year or match_yyyy_mm:
        
        if match_month_year:
            pass
        
            month_name, year = match_month_year.groups()
        
            month_number = {
                "Janeiro": 1,
                "Fevereiro": 2,
                "Março": 3,
                "Abril": 4,
                "Maio": 5,
                "Junho": 6,
                "Julho": 7,
                "Agosto": 8,
                "Setembro": 9,
                "Outubro": 10,
                "Novembro": 11,
                "Dezembro": 12
            }
            
            month = month_number[month_name]
            
        elif match_yyyy_mm:
            year, month = match_yyyy_mm.groups()
            month = int(month)
            
        year = int(year)
        
        last_day = calendar.monthrange(year, month)[1]
        
        return f"{year}-{month:02d}-01", f"{year}-{month:02d}-{last_day}"
    
    
    # Pattern 'Year'; example: "2023"
    match = re.fullmatch(r"(\d{4})", dt_string)
    
    if match:
        year = int(match.group())
        
        return f"{year}-01-01", f"{year}-12-31"
    
    
    # For trimester formats
    
    # "1.\u00ba Trimestre de 2026"
    match_extended_trimester = re.fullmatch(
        r"(1.\u00ba Trimestre|2.\u00ba Trimestre|3.\u00ba Trimestre|4.\u00ba Trimestre) de (\d{4})",
        dt_string
    )
    
    # Format 'YYYY-QQ'
    match_yyyy_qq = re.fullmatch(r"(\d{4})-Q(\d{1})", dt_string)
    
    if match_extended_trimester or match_yyyy_qq:
        
        if match_extended_trimester:
        
            trimester, year = match_extended_trimester.groups()
        
            trimester_number = {
                "1.\u00ba Trimestre": 1,
                "2.\u00ba Trimestre": 4,
                "3.\u00ba Trimestre": 7,
                "4.\u00ba Trimestre": 10
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
    
    
    # For format "1.\u00ba Semestre de 2026"
    match = re.fullmatch(
        r"(1.\u00ba Semestre|2.\u00ba Semestre) de (\d{4})",
        dt_string
    )
    
    if match:
        semester, year = match.groups()
        
        year = int(year)
        
        semester_number = {
            "1.\u00ba Semestre": 1,
            "2.\u00ba Semestre": 7
        }
        
        semester_number = semester_number[semester]
        
        last_day = calendar.monthrange(year, semester_number + 5)[1]
        
        return f"{year}-{semester_number:02d}-01", f"{year}-{semester_number + 5:02d}-{last_day}"
    
    