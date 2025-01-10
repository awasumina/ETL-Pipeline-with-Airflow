# ETL Pipelines with Airflow

This project demonstrates ETL (Extract, Transform, Load) pipelines orchestrated using Apache Airflow. Each pipeline automates the extraction of data from external APIs, transforms it into a structured format, and loads it into a suitable destination for analysis.

## Pipelines Overview

### 1. Weather ETL Pipeline
This pipeline extracts weather data from the Open Meteo API, transforms it, and loads it into either an S3 bucket or a PostgreSQL database.

### 2. Twitter ETL Pipeline
This pipeline fetches tweets using the Twitter API, processes them, and saves the refined data into a CSV file.

---

## Prerequisites

- **Apache Airflow**: To manage and schedule the ETL tasks.
- **Docker**: For containerized execution of Airflow services.
- **Astro CLI**: (Optional) To manage the Airflow project locally.
- **Amazon S3**: (Optional) For storing weather data.
- **PostgreSQL**: (Optional) For storing weather data.
- **Twitter API**: Access credentials to fetch tweets.

---

## Weather ETL Pipeline

### Pipeline Steps
1. **Extract**:
   - Fetches real-time weather data for Kathmandu, Nepal (27.7172° N, 85.3240° E) using the Open Meteo API.

2. **Transform**:
   - Prepares data fields like latitude, longitude, windspeed, temperature, etc., for storage.

3. **Load**:
   - **Option 1: S3**: Saves data as a JSON file in the `etlweather` S3 bucket.
   - **Option 2: PostgreSQL**: Inserts data into a `weather_data` table.

### Example Output
- **JSON Format (S3)**:
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
- **PostgreSQL Table Schema**:
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
The pipeline runs daily, overwriting the JSON file in S3 or inserting new rows into PostgreSQL.

---

## Twitter ETL Pipeline

### Pipeline Steps
1. **Extract**:
   - Fetches up to 100 recent tweets from a specified user (e.g., `justinbieber`) using the Twitter API v2.

2. **Transform**:
   - Extracts fields such as creation date, tweet text, retweet count, and like count.

3. **Load**:
   - Saves the processed data into a CSV file (`refined_tweets_v2.csv`) for further analysis.

### Example Output
The CSV file contains:
- `created_at`: Timestamp of the tweet.
- `text`: Content of the tweet.
- `retweet_count`: Number of retweets.
- `like_count`: Number of likes.


---

- **Outputs**:
  - Weather data in JSON (S3) or PostgreSQL.
  - Processed tweet data in `refined_tweets_v2.csv`.

---

## Conclusion

These pipelines illustrate the flexibility of Airflow in managing diverse ETL workflows. The Weather ETL pipeline provides insights into real-time weather data, while the Twitter ETL pipeline enables the analysis of social media trends. Both pipelines can be customized and scaled based on specific use cases.