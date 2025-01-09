# Weather ETL Pipeline with Airflow

This project sets up an ETL pipeline using Apache Airflow to extract weather data from the Open Meteo API, transform it into a suitable format, and load it either into an S3 bucket or a PostgreSQL database. The pipeline runs daily to fetch real-time weather information based on the latitude and longitude of Kathmandu, Nepal (27.7172° N, 85.3240° E).

## Prerequisites

- **Astro CLI**: To manage the project locally using Docker
- **Docker**: To run the services locally in a containerized environment
- **Amazon S3**: For storing the transformed weather data (optional setup)
- **PostgreSQL**: For storing the transformed weather data (optional setup)
- **Airflow**: To manage and schedule the ETL tasks

## Airflow DAG Overview

The Airflow DAG defined in `etlweather.py` performs the following steps:

1. **Extract**: 
   - Fetches weather data from Open Meteo API using the HTTP hook.

2. **Transform**: 
   - Extracts necessary fields (latitude, longitude, windspeed, temperature, etc.) and prepares them for storage.

3. **Load**:
   - **Option 1: S3**: Loads the transformed data into an S3 bucket (`etlweather`) as a JSON file.
   - **Option 2: PostgreSQL**: Loads the transformed data into a PostgreSQL table (`weather_data`) using the Postgres hook.

### S3 Bucket Overview (Optional)

If you're storing the data in S3, the transformed weather data will be stored with the following characteristics:
- **Bucket Name**: `etlweather`
- **File Name**: The file is dynamically generated based on the current date (e.g., `weather_data_2025-01-09.json`).

### Example Transformation Output (JSON)

The transformed data is stored in the following JSON format when using S3:

```json
{
    "latitude": 27.7172,
    "longitude": 85.3240,
    "windspeed": 3.5,
    "winddirection": 180,
    "temperature": 22.1,
    "weathercode": 3
}
```

### PostgreSQL Table Overview (Optional)

If you're loading the data into PostgreSQL, the data will be inserted into the `weather_data` table. The table schema is defined as:

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

### Execution Schedule

The pipeline runs daily, fetching the latest weather data and either:
- Overwriting the JSON file in the S3 bucket if a file with the same name exists, or
- Inserting new rows into the PostgreSQL `weather_data` table.

## Conclusion

This ETL pipeline automates the process of extracting weather data from the Open Meteo API, transforming it into a structured format, and loading it into either an S3 bucket or a PostgreSQL database for further analysis or use.