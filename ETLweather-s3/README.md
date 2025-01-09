# Weather ETL Pipeline with Airflow

This project sets up an ETL pipeline using Apache Airflow to extract weather data from the Open Meteo API, transform it into a suitable format, and load it into an S3 bucket. The pipeline runs daily to fetch real-time weather information based on the latitude and longitude of Kathmandu, Nepal (27.7172° N, 85.3240° E).
    
## Prerequisites

- **Astro CLI**: To manage the project locally using Docker
- **Docker**: To run the services locally in a containerized environment
- **Amazon S3**: For storing the transformed weather data
- **Airflow**: To manage and schedule the ETL tasks

### Airflow DAG Overview

The Airflow DAG defined in `etlweather.py` performs the following steps:

1. **Extract**:
   - Fetches weather data from Open Meteo API using the HTTP hook.

2. **Transform**:
   - Extracts necessary fields (latitude, longitude, windspeed, temperature, etc.) and prepares them for storage in S3.

3. **Load**:
   - Loads the transformed data into an S3 bucket (`etlweather`) as a JSON file.

### S3 Bucket Overview

The transformed weather data is stored in an S3 bucket with the following characteristics:
- **Bucket Name**: `etlweather`
- **File Name**: The file is dynamically generated based on the current date (e.g., `weather_data_2025-01-09.json`).

### Example Transformation Output (JSON)

The transformed data is stored in the following JSON format:

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

Each day, the pipeline will generate a new JSON file with the latest weather data. The pipeline runs daily and overwrites the file in the S3 bucket if a file with the same name exists.