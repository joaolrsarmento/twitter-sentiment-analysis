import re
from nltk.tokenize import word_tokenize
from string import punctuation
from nltk.corpus import stopwords


class TweetFilter:
    def __init__(self):
        pass

    def processTweets(self, tweetsList):
        processedTweets = []
        for tweet in tweetsList:
            processedTweets.append(
                (self.__processTweet(tweet["text"]), tweet["label"]))
        return processedTweets

    def __processTweet(self, tweet):
        tweet = tweet.lower()
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))',
                       'URL', tweet) 
        tweet = re.sub('@[^\s]+', 'AT_USER', tweet)  
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)  
        tweet = word_tokenize(tweet)
        return tweet


filter = TweetFilter()

tweets = filter.processTweets([
    {"label": "desisto", "text": "@person1 retweeted @person2: Corn has got to be the most delllllicious crop in the world!!!! #corn #thoughts..."}])

print(tweets)
