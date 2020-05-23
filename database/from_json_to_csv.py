import pandas as pd
import os
import json
from pandas.io.json import json_normalize  

path = os.path.dirname(os.path.abspath(__file__))
fpath = path + '/tweets.txt' # filepath
csv_path = path +'/tweets.csv' # csv filepath
with open (fpath) as f:
    data = [json.loads(line) for line in f]
# putting the data on DataFrame with columns:
# id, created at, text, retweeted status, retweeted.status_favcount, retweeted.status_retweet_count, retweeted,user, user.followers_count, user.friend count, user.favorite_count , user.statuses_count

data = json_normalize(data)
clean_df = data[['id', 'created_at','full_text', 'retweeted_status.id', 'retweeted_status.full_text','retweeted_status.retweet_count' ,'retweeted_status.favorite_count', 'user.followers_count', 'user.friends_count','user.statuses_count']]
clean_df.to_csv(csv_path, index = False)
