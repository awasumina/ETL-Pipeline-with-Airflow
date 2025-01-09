from airflow import DAG
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import task
from airflow.utils.dates import days_ago
import json
import requests

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
with DAG(dag_id='weather_etl_pipeline',
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
    def load_weather_data(transformed_data):
        """Load transformed weather data into a Postgres database"""
        pg_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
        conn = pg_hook.get_conn()
        cursor = conn.cursor()

        # Create table if it doesn't exist
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS weather_data (
                latitude FLOAT,
                longitude FLOAT,
                windspeed FLOAT,
                winddirection FLOAT,
                temperature FLOAT,
                weathercode INT
            );
            """
        )

        # Insert data into the table
        cursor.execute(
            """
            INSERT INTO weather_data VALUES (%s, %s, %s, %s, %s, %s);
            """,
            (
                transformed_data['latitude'],
                transformed_data['longitude'],
                transformed_data['windspeed'],
                transformed_data['winddirection'],
                transformed_data['temperature'],
                transformed_data['weathercode'],
            ),
        )
        conn.commit()
        cursor.close()

    # Set task dependencies (ensure these are within the DAG context)
    weather_data = extract_weather_data()  # This will return a JSON object
    transformed_data = transform_weather_data(weather_data)  # Pass the data as an argument, not the task itself
    load_weather_data(transformed_data)
    
