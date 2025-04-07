import pandas as pd
from datetime import datetime

def adjust_future_dates(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%d/%m/%y")
    except ValueError:
        return None

    if date_obj > datetime.now():
        new_year = date_obj.year - 100
        date_obj = date_obj.replace(year=new_year)
    
    return date_obj.strftime("%Y-%m-%d")


def adjust_csv_dates(input_csv, output_csv):
    df = pd.read_csv(input_csv)

    for column in df.columns:
        if 'date' in column.lower():
            df[column] = df[column].apply(adjust_future_dates)

    df.to_csv(output_csv, index=False)
    print(f"Adjusted CSV saved as {output_csv}")


adjust_csv_dates("races.csv", "new_races.csv")

