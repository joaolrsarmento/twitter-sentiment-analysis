import pandas as pd
import tweepy
import os
import schedule
import time

# run the script on terminal with 'nohup python data_retriver.py &', the & will leave the program running on background 
# the number of the process will be returned (save it for later)
# to finish the process, run 'kill -9 (insert here the number of the process)'

def get_message(tweet):
    """
    Robustly get a message on a tweet.
    Even if not extended mode or is a retweet (always truncated).
    """
    try:
        return tweet.full_text
    except AttributeError:
        return tweet.text

def get_tweets(cursor, limit):
    results = []
    i = 0
    for tweet in cursor.items():
        if (i == limit):
            break
        parsed_tweet = {
            "id": tweet.id,
            "screen_name": tweet.author.screen_name,
            "message": get_message(tweet),
        }
        i = i + 1
        results.append(parsed_tweet)
    return results


client_key = '19mR3oZBtNdMycE2dXaWnCln4'
client_secret = 'p5iYOiau1Y02ciP8GMYS2iktp7IWJFF0R00PywM85ABU2cd7e2'

access_token = '1245132190746324996-pybplw0mTwXm8FrUUv37oYEdRDmlAR'
access_token_secret = 'oNumM1Si2eVUZhKGfhaSxMrmcKto6t2ND2RwprXvu7cBu'


def job():

    path = os.path.dirname(os.path.abspath(__file__))
    path = path + '/data.csv'

    auth = tweepy.OAuthHandler(client_key, client_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    query = 'governo OR bolsonaro OR política OR presidente OR COVID OR Corona OR Vírus'
    lang = 'pt'

    actual_data = pd.read_csv((path), index_col = 'Unnamed: 0')
    last_data_id = actual_data['id'].iloc[len(actual_data['id']) - 1]
    cursor = tweepy.Cursor(
        api.search,
        q=query,
        result_type = 'recent',
        tweet_mode="extended",
        lang=lang,
        since_id = last_data_id
    )

    remaining_tweets = api.rate_limit_status()['resources']['search']['/search/tweets']['remaining']

    tweet_list = get_tweets(cursor, remaining_tweets)
    df = pd.DataFrame(data = tweet_list)
    df = pd.concat([actual_data, df], sort = False, ignore_index = True)
    df.to_csv(path)

    print(len(df['id']))

schedule.every(15).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

