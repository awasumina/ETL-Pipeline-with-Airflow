# Twitter ETL with Airflow

This project demonstrates an ETL (Extract, Transform, Load) pipeline that fetches tweets using the Twitter API, processes them, and saves the refined data into a CSV file. The pipeline is orchestrated using Apache Airflow.

## Overview

The ETL pipeline consists of the following steps:

1. **Extract**: Retrieve tweets from a specified Twitter user using the Twitter API v2.
2. **Transform**: Process the tweet data to extract relevant fields such as creation date, text, retweet count, and like count.
3. **Load**: Save the processed data into a CSV file for further analysis.

The entire process is automated with Apache Airflow, running daily as a scheduled task (DAG).

## Project Structure

- **`twitter_etl.py`**: Contains the Python script for the ETL process.
- **Airflow DAG (`twitter_dag`)**: Defines the schedule and execution of the ETL pipeline.
- **`refined_tweets_v2.csv`**: Output file containing the processed tweet data.


## Output
The processed tweet data will be saved in a CSV file named `refined_tweets_v2.csv` in the current working directory. This file includes the following fields:

- **`created_at`**: Timestamp of the tweet.
- **`text`**: Content of the tweet.
- **`retweet_count`**: Number of retweets.
- **`like_count`**: Number of likes.

## Notes
- This example fetches up to 100 recent tweets from the specified user (`justinbieber`). You can adjust the `max_results` parameter as needed.
- Ensure the Airflow environment's Python interpreter has access to the required libraries.
- Handle API rate limits appropriately for larger-scale data extraction.
