import tweepy
import pandas as pd 
import json
from datetime import datetime
import s3fs 


access_secret = "fvlmyion6H5ZNxILGH9x9WOrYgTK0I9Oow4nmIO5O0rugLvTzB" 
access_key = "LrWSqrZdD1ilgpuYTJeunxL0d" 
consumer_key = "1580150115528245249-CNQOZRwV5jLtM5Mh9RtXVAqrXC08Fa"
consumer_secret = "P9voF2kPE1DSoHGSiYfZa8mYKKjBX8zYcWLn5kMRArAlt"

def run_twitter_etl():
    # Twitter API keys
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAEJwxwEAAAAArqQOdlyRTQp7%2FGHA7D6eE9OqnIc%3DH76Ytj1m670f4V9wWNg2uJSMu8CrvQlk2TwH9vOb6gQM43WgdU"

    # Initialize the client
    client = tweepy.Client(bearer_token=bearer_token)

    # Fetch tweets using the v2 API
    user_id = client.get_user(username='justinbieber').data.id
    tweets = client.get_users_tweets(user_id, max_results=100, tweet_fields=["created_at", "public_metrics", "text"])

    # Extract relevant data
    tweets_data = []
    for tweet in tweets.data:
        tweets_data.append({
            "created_at": tweet.created_at,
            "text": tweet.text,
            "retweet_count": tweet.public_metrics["retweet_count"],
            "like_count": tweet.public_metrics["like_count"],
        })

    # Save to CSV
    df = pd.DataFrame(tweets_data)
    df.to_csv("refined_tweets_v2.csv", index=False)
    print("Tweets saved successfully!")
run_twitter_etl()


