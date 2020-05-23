import pandas as pd
import tweepy
import os
import sys
import jsonpickle
# run the script on terminal with 'nohup python data_retriever.py &', the & will leave the program running on background 
# the number of the process will be returned (save it for later)
# to finish the process, run 'kill -9 (insert here the number of the process)'
client_key = '19mR3oZBtNdMycE2dXaWnCln4'
client_secret = 'p5iYOiau1Y02ciP8GMYS2iktp7IWJFF0R00PywM85ABU2cd7e2'

access_token = '1245132190746324996-pybplw0mTwXm8FrUUv37oYEdRDmlAR'
access_token_secret = 'oNumM1Si2eVUZhKGfhaSxMrmcKto6t2ND2RwprXvu7cBu'

path = os.path.dirname(os.path.abspath(__file__))
print(path)

auth = tweepy.AppAuthHandler(client_key, client_secret)
api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)
searchQuery = 'futebol OR flamengo OR cruzeiro OR ciência or cloroquina'
lang = 'pt'
maxTweets = 10000000 # Some arbitrary large number
tweetsPerQry = 100  # this is the max the API permits
fName = path + '/tweets.txt' # We'll store the tweets in a text file.
# If results from a specific ID onwards are reqd, set since_id to that ID.
# else default to no lower limit, go as far back as API allows
sinceId = None

# If results only below a specific ID are, set max_id to that ID.
# else default to no upper limit, start from the most recent tweet matching the search query.
max_id = -1

tweetCount = 0
print("Downloading max {0} tweets".format(maxTweets))
with open(fName, 'w') as f:
    while tweetCount < maxTweets:
        try:
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry, tweet_mode = 'extended', lang = lang)
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry, tweet_mode = 'extended', lang = lang,
                                            since_id=sinceId)
            else:
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry, tweet_mode = 'extended', lang = lang,
                                            max_id=str(max_id - 1))
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry, tweet_mode = 'extended', lang = lang,
                                            max_id=str(max_id - 1),
                                            since_id=sinceId)
            if not new_tweets:
                print("No more tweets found")
                break
            for tweet in new_tweets:
                f.write(jsonpickle.encode(tweet._json, unpicklable=False) +
                        '\n')
            tweetCount += len(new_tweets)
            print("Downloaded {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            break

print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))