import pandas as pd
import requests
from datetime import datetime
from pandas import json_normalize
import s3fs

def run_rapid_football_etl():
    url = 'https://api-football-v1.p.rapidapi.com/v3/fixtures'
    querystring = {"league": "1", "season": "2010"}
    headers = {
        "X-RapidAPI-Key": "your_api_key",
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    # Extract data and normalize the response
    response = requests.get(url, headers=headers, params=querystring)
    fixtures = response.json()["response"]

    df = pd.json_normalize(fixtures)

    # Function to transform column names
    def rename_columns(df):
        renamed_columns = []
        for column in df.columns:
            renamed_columns.append(column.replace('.', '_'))
        return renamed_columns
    
    df.columns = rename_columns(df)
    df_sorted = df.sort_values(by='fixture_date')

    # Store output in csv format in a S3 bucket
    df_sorted.to_csv("s3://pablomtb-burner-20240513-airflow/results/rapid_football_results_2010.csv")