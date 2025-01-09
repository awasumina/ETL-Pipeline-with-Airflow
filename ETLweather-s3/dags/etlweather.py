from airflow import DAG
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.decorators import task
from airflow.utils.dates import days_ago
import json
from datetime import datetime

# Define dynamic file name based on the current date
FILE_NAME = f"weather_data_{datetime.now().strftime('%Y-%m-%d')}.json"

# Latitude and longitude for desired location
LATITUDE = '27.7172'
LONGITUDE = '85.3240'
POSTGRES_CONN_ID = 'postgres_default'
API_CONN_ID = 'open_meteo_api'  # Connection name

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1)
}

# Create a DAG
with DAG(dag_id='weather_etl_pipeline_s3',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:

    @task()
    def extract_weather_data():
        """Extract weather data from Open Meteo API using Airflow connection"""
        
        # Use HTTP hook to get connection details from airflow
        http_hook = HttpHook(http_conn_id=API_CONN_ID, method='GET')

        # Build API endpoint -- url--> https://api.open-meteo.com/v1/forecast?latitude=27.7172&longitude=85.3240&current_weather=true
        endpoint = f'/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current_weather=true'

        # Make request via HTTP hook
        response = http_hook.run(endpoint)

        if response.status_code == 200:
            return response.json()  
        else:
            raise ValueError(f'API returned status code {response.status_code}, failed to fetch data')

    @task()
    def transform_weather_data(weather_data):
        """Transform weather data into a format that can be loaded into a database"""
        transformed_data = {
            'latitude': weather_data['latitude'],
            'longitude': weather_data['longitude'],
            'windspeed': weather_data['current_weather']['windspeed'],  # Nested field
            'winddirection': weather_data['current_weather']['winddirection'],  # Nested field
            'temperature': weather_data['current_weather']['temperature'],  # Nested field
            'weathercode': weather_data['current_weather']['weathercode'],  # Nested field
        }
        return transformed_data

    @task()
    def load_weather_data_to_s3(transformed_data):
         """Load transformed weather data into an S3 bucket"""
         s3_hook = S3Hook(aws_conn_id='aws_default')  # Use the Airflow connection to AWS
         # Define the S3 bucket and key (filename) for storing the data
         BUCKET_NAME = 'etlweather'
         FILE_NAME = 'weather_data.json'

         # Convert transformed data to JSON format
         json_data = json.dumps(transformed_data, indent=4)

         # Upload the JSON data to S3
         s3_hook.load_string(
             string_data=json_data,
             key=FILE_NAME,
             bucket_name=BUCKET_NAME,
             replace=True  # Set to True to overwrite the file if it exists
         )
         
    # Task definitions
    weather_data = extract_weather_data()
    transformed_data = transform_weather_data(weather_data)
    load_weather_data_to_s3(transformed_data)

 