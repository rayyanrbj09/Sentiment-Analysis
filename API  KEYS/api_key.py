import os
import time
import tweepy
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# CREDENTIALS
BEARER_TOKEN = os.getenv('BEARER_TOKEN')

# Initialize Tweepy Client (Only Bearer Token Required)
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Querying depending on the topic
query = '#TrendingTopic lang:en -is:retweet'

def fetch_tweets(query, max_tweets=100):
    all_tweets = []
    next_token = None

    while len(all_tweets) < max_tweets:
        try:
            response = client.search_recent_tweets(
                query=query, 
                tweet_fields=['created_at', 'text'], 
                max_results=min(50, max_tweets - len(all_tweets)),  # Ensuring we don't exceed limit
                next_token=next_token
            )

            if response and response.data:
                all_tweets.extend(response.data)
                next_token = response.meta.get("next_token")
                if not next_token:
                    break  # No more tweets available
            else:
                break  # No tweets found

        except tweepy.RateLimitError as e:
            print("Rate limit exceeded. Waiting before retrying...")
            time.sleep(60)  # Waiting before retry
        except tweepy.TweepyException as e:
            print(f"Error: {e}")
            break  # Stop fetching in case of API error

    return all_tweets

# Fetch tweets
tweets = fetch_tweets(query, max_tweets=100)

# Processing tweet data
if not tweets:
    print("Failed to fetch tweets or no tweets found!")
else:
    tweet_data = [{"created_at": tweet.created_at, "text": tweet.text} for tweet in tweets]
    df = pd.DataFrame(tweet_data)

    # Save to CSV
    df.to_csv('tweets.csv', index=False, encoding='utf-8-sig')
    print("Tweets saved to tweets.csv")
    print(df)