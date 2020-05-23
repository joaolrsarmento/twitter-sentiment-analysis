import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import re
import emoji


path = os.path.dirname(os.path.abspath(__file__))
final_path = path +'/data.csv' # csv filepath

#Count vectorizer for N grams
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer

# Nltk for tekenize and stopwords

from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

def count_values_in_column(data,feature):
    """
    Use when we have a batch test set
    """
    total = data.loc[:,feature].value_counts(dropna = False)
    percentage=round(data.loc[:,feature].value_counts(dropna = False, normalize = True)*100,2)
    return pd.concat([total,percentage], axis = 1, keys = ['Total','Percentage'])

def duplicated_values_data(data):
    dup=[]
    columns=data.columns
    for i in data.columns:
        dup.append(sum(data[i].duplicated()))
    return pd.concat([pd.Series(columns),pd.Series(dup)],axis=1,keys=['Columns','Duplicate count'])

def missing_value_of_data(data):
    total = data.isnull().sum().sort_values(ascending=False)
    percentage = round (total/data.shape[0]*100,2)
    return pd.concat([total,percentage], axis = 1, keys = ['Total','Percentage'])

def find_punct(text):
    line = re.findall(r'[!"\$%&\'()*+,\-.\/:;=#@?\[\\\]^_`{|}~]*', text)
    string="".join(line)
    return list(string)

def find_number(text):
    line=re.findall(r'[0-9]+',text)
    return " ".join(line)

def find_url(string): 
    text = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',string)
    return "".join(text) # converting return value from list to string

def find_emoji(text):
    emo_text=emoji.demojize(text)
    line=re.findall(r'\:(.*?)\:',emo_text)
    return line

def find_at(text):
    line=re.findall(r'(?<=@)\w+',text)
    return " ".join(line)

def find_email(text):
    line = re.findall(r'[\w\.-]+@[\w\.-]+',str(text))
    return ",".join(line)

def find_hash(text):
    line=re.findall(r'(?<=#)\w+',text)
    return " ".join(line)

def rep(text):
    grp = text.group(0)
    if len(grp) > 1:
        return grp[0:4] # can change the value here on repetition

def unique_char(rep,sentence):
    convert = re.sub(r'(\w)\1+', rep, sentence) 
    return convert

def or_cond(text,key1,key2):
    """
    use to search for key1 or key2 word
    """
    line=re.findall(r"{}|{}".format(key1,key2), text) 
    return " ".join(line)

def and_cond(text):
    """
    use to search for key1 and key2 words
    """
    line=re.findall(r'(?=.*do)(?=.*die).*', text) 
    return " ".join(line)

def only_words(text):
    line=re.findall(r'\b[^\d\W]+\b', text)
    return " ".join(line)

    stop_words = set(stopwords.words('english')) 
    word_tokens = word_tokenize(text) 
    non_stop_words = [w for w in word_tokens if not w in stop_words] 
    stop_words= [w for w in word_tokens if w in stop_words] 
    return stop_words

def remove_emoji(text):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def ngrams_top(corpus,ngram_range,n=None):
    """
    List the top n words in a vocabulary according to occurrence in a text corpus.
    example use : ngrams_top(data['full_text'],(2,2),n=10), top 10 n_grans of 2 words
    """
    vec = CountVectorizer(stop_words = 'english',ngram_range=ngram_range).fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    total_list=words_freq[:n]
    df=pd.DataFrame(total_list,columns=['text','count'])
    return df

path = os.path.dirname(os.path.abspath(__file__))
csv_path = path +'/tweets.csv' # csv filepath

data = pd.read_csv(csv_path)
data = data.drop_duplicates('retweeted_status.id') # droping same retweets
#data['url'] = data['full_text'].apply(lambda x:find_url(x))
data['emoji'] = data['full_text'].apply(lambda x: find_emoji(x))
data['full_text'] = data['full_text'].apply(lambda x: remove_emoji(x))
data['unique_char'] = data['full_text'].apply(lambda x : unique_char(rep,x))
data['only_words'] = data['full_text'].apply(lambda x : only_words(x))
data['at_mention'] = data['full_text'].apply(lambda x: find_at(x))
data['punctuation'] = data['full_text'].apply(lambda x : find_punct(x))

data.to_csv(final_path, index = False)