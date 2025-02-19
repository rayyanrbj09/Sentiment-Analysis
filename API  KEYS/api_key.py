import os 
from dotenv import load_dotenv
import tweepy
import tweepy.client
import time
import pandas as pd

load_dotenv()
# CREDENTIALS
Bearer_token =  os.getenv('BEARER_TOKEN')
headers = {"Authorization": f"Bearer {Bearer_token}"}

client =  tweepy.Client(bearer_token=Bearer_token)

#Querying depending on the topic 
query = '#TrendingTopic lang:en -is:retweet'
try:
    tweets = client.search_recent_tweets(query, tweet_fields = ['created_at', 'text'],max_results = 10)
except tweepy.TooManyRequests:
    print("Rate limit exceeded. Wait before trying")
    time.sleep(60)

tweet_data =[]

if tweets.data:
    df =  pd.DataFrame(tweet_data)
    # Saving tweets to csv file for easy processing 
    df.to_csv('tweets.csv',  index= False,  encoding= 'utf-8')
    print("Tweets saved to tweet.csv")
else:
    print('No tweets found!!')