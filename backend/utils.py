
import re, calendar


# dt_string = "Janeiro de 2022" (example)
# returns two dates: the first day of the month and the last day of the month
# for example; '2022-01-01' and '2022-01-31'
def transform_data_to_range(dt_string):
    
    # Pattern ('Month' de 'Year'); example: "Janeiro de 2022"
    match = re.fullmatch(
        r"(Janeiro|Fevereiro|Março|Abril|Maio|Junho|Julho|Agosto|"
        r"Setembro|Outubro|Novembro|Dezembro) de (\d{4})",
        dt_string
    )
    
    if match:
        month_name, year = match.groups()
        
        year = int(year)
        
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
        
        last_day = calendar.monthrange(year, month)[1]
        
        return f"{year}-{month:02d}-01", f"{year}-{month:02d}-{last_day}"
    
    
    # Pattern 'Year'; example: "2023"
    match = re.fullmatch(r"\d{4}", dt_string)
    
    if match:
        year = int(match.group())
        
        return f"{year}-01-01", f"{year}-12-31"
    
    
    # For format "1.\u00ba Trimestre de 2026"
    match = re.fullmatch(
        r"(1.\u00ba Trimestre|2.\u00ba Trimestre|3.\u00ba Trimestre|4.\u00ba Trimestre) de (\d{4})",
        dt_string
    )
    
    if match:
        trimester, year = match.groups()
        
        year = int(year)
        
        trimester_number = {
            "1.\u00ba Trimestre": 1,
            "2.\u00ba Trimestre": 4,
            "3.\u00ba Trimestre": 7,
            "4.\u00ba Trimestre": 10
        }
        
        trimester_number = trimester_number[trimester]
        
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
    
    