import tweepy
import pickle
from keys import *

def get_user_tweets(user_id, consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    tweets = api.user_timeline(screen_name=user_id, count=200, include_rts=True, tweet_mode='extended')

    return tweets

