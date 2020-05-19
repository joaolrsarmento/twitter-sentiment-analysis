import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob


class TwitterServer(object):
    ''' 
    Connects to twitter api. 
    '''

    def __init__(self):
        ''' 
        Class constructor or initialization method. 
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = 'bKRkBkn2see1Rf2vT4erLl6j6'
        consumer_secret = 'Xkz4shXrCWVMd4en56IJsQwvRWAcmMDJ0vyN5Q3AYMIu89oJnJ'
        access_token = '1260981479619866627-3krEP78iJo80ik7IXbhUxTLGCyMbjx'
        access_token_secret = 'HSpum4tvexp3aNNwARvwA8Bo3n6UJe0os6NvuQaBZoZ9G'

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error in auth. Try again later.")
            exit()

    def clean_tweet(self, tweet):
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+) | ([ ^ 0-9A-Za-z \t])|(\w+: \/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        ''' 
        Utility function to classify sentiment of passed tweet 
        using textblob's sentiment method 
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=10):
        ''' 
        Uses the api to get tweets through a query. This method will return count tweets.
        '''
        
        tweets = [] # Empty list to store the tweets

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q=query, count=count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(
                    tweet.text)

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))


# creating object of TwitterClient Class
api = TwitterServer()
# calling function to get tweets
tweets = api.get_tweets(query='Bolsonaro', count=10)

# picking positive tweets from tweets
ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
# percentage of positive tweets
print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
# picking negative tweets from tweets
ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
# percentage of negative tweets
print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
# percentage of neutral tweets
print("Neutral tweets percentage: {} % \
    ".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)))
