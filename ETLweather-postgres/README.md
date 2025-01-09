# Weather ETL Pipeline with Airflow

This project sets up an ETL pipeline using Apache Airflow to extract weather data from the Open Meteo API, transform it into a suitable format, and load it into a PostgreSQL database. The pipeline runs daily to fetch real-time weather information based on the latitude and longitude of Kathmandu, Nepal (27.7172° N, 85.3240° E).

## Prerequisites

- **Astro CLI**: To manage the project locally using Docker
- **Docker**: To run the services locally in a containerized environment
- **PostgreSQL**: For storing the transformed weather data
- **Airflow**: To manage and schedule the ETL tasks


###  Airflow DAG Overview

The Airflow DAG defined in `etlweather.py` performs the following steps:

1. **Extract**: 
   - Fetches weather data from Open Meteo API using the HTTP hook.

2. **Transform**:
   - Extracts necessary fields (latitude, longitude, windspeed, temperature, etc.) and prepares them for insertion into PostgreSQL.

3. **Load**:
   - Loads the transformed data into a PostgreSQL table (`weather_data`) using the Postgres hook.
   
The table schema is defined as follows:

```sql
CREATE TABLE IF NOT EXISTS weather_data (
    latitude FLOAT,
    longitude FLOAT,
    windspeed FLOAT,
    winddirection FLOAT,
    temperature FLOAT,
    weathercode INT
);
```
