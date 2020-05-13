import pandas as pd
import os
from datetime import timedelta
from nltk.corpus import stopwords
stop = stopwords.words('english')
from sklearn.feature_extraction.text import CountVectorizer

def applying_url(row):
    return "https://twitter.com/{}/status/{}".format(row['user_screen_name'], row['id_str'])

Education = False


if Education == True:
    source_folder = 'data/education/'
else:
    source_folder = 'data/'

def find_csv_filenames(path_to_dir, suffix=".csv" ):
    filenames = os.listdir(path_to_dir)
    return [filename for filename in filenames if filename.endswith(suffix)]

files = find_csv_filenames(source_folder + 'sources/')
file = files[0]

tweets_raw = pd.read_csv(str(source_folder + 'sources/' + file), usecols=['id_str',
                               'user_id_str',
                               'created_at',
                               'user_screen_name',
                               'user_created_at',
                               'user_statuses_count',
                               'text',
                               'entities_urls',
                               'retweeted_status_id'], parse_dates=['created_at'])


tweets_per_hour = tweets_raw.assign(time_floor=tweets_raw['created_at'].dt.floor('H'))\
    .groupby('time_floor')\
    .agg({'id_str': 'count'})\
    .rename(columns={'id_str': 'tweet_count'})

tweets_per_hour.to_csv(source_folder + 'tweets_per_hour.csv')


tidy_tweets = tweets_raw[['created_at', 'text']]\
    .assign(text=tweets_raw['text']
            .str.lower()\
            .replace("https://t.co/[A-Za-z\\d]+|http://[A-Za-z\\d]+|&amp;|&lt;|&gt;|RT|https", "", regex=True)\
            .replace("([^A-Za-z_\\d']|'(?![A-Za-z_\\d]))\d+", " ", regex=True)\
            .replace('"', '')\
            .replace("[.!?\\-%,():'+]", "", regex=True)
            .str.split()\
            .apply(lambda x: [item for item in x if item not in stop]))\
    .explode('text')\
    .rename(columns={'text': 'word'})

tidy_tweets = tidy_tweets.dropna(subset=['word'])

# ------------------------ Hashtags --------------------------------

hashtag_count = tidy_tweets\
    .loc[(tidy_tweets['word'].str.startswith("#"))]\
    .groupby('word') \
    .agg({'word': 'count'}) \
    .rename(columns={'word': 'n'})\
    .sort_values(by='n', ascending=False)

hashtag_count.to_csv(source_folder + 'hashtag_count.csv')

hashtag_count_24h = tidy_tweets\
    .loc[(tidy_tweets['word'].str.startswith("#"))]\
    .loc[(tweets_raw['created_at'] > max(tweets_raw['created_at']) - timedelta(days=1))]\
    .groupby('word') \
    .agg({'word': 'count'}) \
    .rename(columns={'word': 'n'})\
    .sort_values(by='n', ascending=False)

hashtag_count_24h.to_csv(source_folder + 'hashtag_count_24h.csv')


# -------------------------------- TRIGRAMS -----------------------------------------

tidy_trigrams = tweets_raw.dropna(subset=['retweeted_status_id'])\
    .loc[:, ['id_str','user_screen_name', 'created_at', 'text']] \
    .assign(text=tweets_raw['text']
            .str.lower() \
            .replace("https://t.co/[A-Za-z\\d]+|http://[A-Za-z\\d]+|&amp;|&lt;|&gt;|RT|https", "", regex=True) \
            .replace("([^A-Za-z_\\d']|'(?![A-Za-z_\\d]))\d+", " ", regex=True) \
            .replace('"', '') \
            .replace("[.!?\\-%,():'+]", "", regex=True)\
            .str.split() \
            .apply(lambda x: [item for item in x if item not in stop])\
            .str.join(' '))

tidy_trigrams_24h = tidy_trigrams.loc[(tidy_trigrams['created_at'] > max(tidy_trigrams['created_at']) - timedelta(days=1))]

word_vectorizer = CountVectorizer(ngram_range=(3,3), analyzer='word')


sparse_matrix = word_vectorizer.fit_transform(tidy_trigrams['text'])
frequencies = sum(sparse_matrix).toarray()[0]
d = {'trigram': word_vectorizer.get_feature_names(), 'n': frequencies}
trigrams = pd.DataFrame(data=d)\
        .sort_values(by='n', ascending=False)

trigrams.to_csv(source_folder + 'trigrams.csv')


sparse_matrix_24 = word_vectorizer.fit_transform(tidy_trigrams_24h['text'])
frequencies_24 = sum(sparse_matrix_24).toarray()[0]
d_24 = {'trigram': word_vectorizer.get_feature_names(), 'n': frequencies_24}
trigrams_24 = pd.DataFrame(data=d_24)\
        .sort_values(by='n', ascending=False)

trigrams_24.to_csv(source_folder + 'trigrams_24h.csv')

# ------------------------------------ URLs -------------------------------

url_list = tweets_raw.drop(tweets_raw[tweets_raw.entities_urls == '[]'].index)\
    .loc[:, ['entities_urls']]\
    .assign(url=tweets_raw['entities_urls']
            .replace("\\[\\{'url': 'htt(\\S)* 'expanded_url': '", "", regex=True) \
            .replace("', 'display_url': '(\\S)*', .*$", "", regex=True)) \
    .groupby('url') \
    .agg({'url': 'count'}) \
    .rename(columns={'url': 'count'}) \
    .sort_values(by='count', ascending=False)

url_list.to_csv(source_folder + 'url_list.csv')

url_list_24 = tweets_raw\
    .drop(tweets_raw[tweets_raw.entities_urls == '[]'].index)\
    .loc[:, ['entities_urls']]\
    .loc[(tweets_raw['created_at'] > max(tweets_raw['created_at']) - timedelta(days=1))]\
    .assign(url=tweets_raw['entities_urls']
            .replace("\\[\\{'url': 'htt(\\S)* 'expanded_url': '", "", regex=True) \
            .replace("', 'display_url': '(\\S)*', .*$", "", regex=True)) \
    .groupby('url') \
    .agg({'url': 'count'}) \
    .rename(columns={'url': 'count'}) \
    .sort_values(by='count', ascending=False)

url_list_24.to_csv(source_folder + 'url_list_24h.csv')

# -------------------------------- MOST RETWEETS ---------------------------

tweets_raw['tweet_url'] = tweets_raw.apply(applying_url, axis=1)

most_retweeted_tweet = tweets_raw.dropna(subset=['retweeted_status_id'])\
    .groupby('text') \
    .agg({'id_str': 'count'}) \
    .rename(columns={'id_str': 'n'})\
    .sort_values(by='n', ascending=False)

most_retweeted_tweet.to_csv(source_folder + 'most_retweeted_tweet_all.csv')

most_retweeted_tweet_24h = tweets_raw.dropna(subset=['retweeted_status_id'])\
    .loc[(tweets_raw['created_at'] > max(tweets_raw['created_at']) - timedelta(days=1))]\
    .groupby('text') \
    .agg({'id_str': 'count'}) \
    .rename(columns={'id_str': 'n'})\
    .sort_values(by='n', ascending=False)

most_retweeted_tweet_24h.to_csv(source_folder + 'most_retweeted_tweet_all_24h.csv')

# ----------------------- MERGING TO GET THE LINK TO ORIGINAL TWEET --------------------------------

tweets_filled = tweets_raw.fillna(0.0)
tweets_orig_url = tweets_raw[tweets_filled.retweeted_status_id == 0.0]
# tweets_url_retweets = tweets_raw[tweets_filled.retweeted_status_id != 0.0]
tweets_org_reduced = tweets_orig_url[['text', 'tweet_url']]
# tweets_retweet_reduced = tweets_url_retweets[['text', 'tweet_url']]

cols = ['text']
merged_orig = most_retweeted_tweet.join(tweets_org_reduced.set_index(cols), on='text')
# merged_retweet = merged_orig.join(tweets_retweet_reduced.set_index(cols), on='text')

merged_all = merged_orig.loc[~merged_orig.index.duplicated(keep='first')]
merged_all.to_csv(source_folder + 'merged_all.csv')

merged_orig_24 = most_retweeted_tweet_24h.join(tweets_org_reduced.set_index(cols), on='text')
# merged_retweet = merged_orig.join(tweets_retweet_reduced.set_index(cols), on='text')

merged_24 = merged_orig_24.loc[~merged_orig_24.index.duplicated(keep='first')]
merged_24.to_csv(source_folder + 'merged_24.csv')