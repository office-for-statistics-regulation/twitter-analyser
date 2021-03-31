from datetime import datetime
import pandas as pd

pd.options.mode.chained_assignment = None
import os
from sklearn.feature_extraction.text import CountVectorizer
from datetime import timedelta
import tweepy

from nltk.corpus import stopwords
import nltk

nltk.download('stopwords', quiet=True)
stop = stopwords.words('english')

import credentials
import config


def apply_account_link(row):
	return "https://twitter.com/{}".format(row['user_screen_name'])


def add_tick(row):
	if row['user_verified'] == True:
		return row['user_name'] + ' ☑️'
	else:
		return row['user_name']


# Quick and easy functions for dataframe manipulation.
def applying_url(row):
	return "https://twitter.com/{}/status/{}".format(row['user_screen_name'], row['id_str'])


def save_to_csv(df, name):
	filename = f'{name}.csv'
	save_path = config.file_path + '/' + filename
	return df.to_csv(save_path)


def find_original_tweet(merged_all, tweets_raw):
	auth = tweepy.AppAuthHandler(credentials.consumer_key, credentials.consumer_secret)

	api = tweepy.API(auth, wait_on_rate_limit=True,
					 wait_on_rate_limit_notify=True)

	for index, row in merged_all.iterrows():

		if pd.isnull(row.tweet_url):
			tweet_id = int(tweets_raw[tweets_raw.text == row.text].retweeted_status_id.values[0])
			try:
				status = api.get_status(tweet_id, tweet_mode="extended")
				user_name = status.user.screen_name
				merged_all.at[index, 'tweet_url'] = "https://twitter.com/{}/status/{}".format(user_name, tweet_id)
			except:
				merged_all.at[index, 'tweet_url'] = "N/A"


def mine_tweets(df):
	tweets_raw = df[['id_str',
					 'user_id_str',
					 'created_at',
					 'user_screen_name',
					 'user_name',
					 'user_created_at',
					 'user_statuses_count',
					 'user_verified',
					 'text',
					 'entities_urls',
					 'retweeted_status_id']]

	tweets_raw['created_at'] = pd.to_datetime(tweets_raw['created_at'], format='%Y-%m-%d %H:%M:%S')

	tweets_per_hour = tweets_raw.assign(time_floor=tweets_raw['created_at'].dt.floor('H')) \
		.groupby('time_floor') \
		.agg({'id_str': 'count'}) \
		.rename(columns={'id_str': 'tweet_count'})

	tweets_per_hour = tweets_per_hour.reset_index()

	tweets_per_hour['topic'] = df['topic'][0]
	tweets_per_hour['date_created'] = df['date'][0]

	save_to_csv(tweets_per_hour, 'tweets_per_hour')

	tidy_tweets = tweets_raw[['created_at', 'text']] \
		.assign(text=tweets_raw['text']
				.str.lower() \
				.replace("https://t.co/[A-Za-z\\d]+|http://[A-Za-z\\d]+|&amp;|&lt;|&gt;|RT|https", "", regex=True) \
				.replace("([^A-Za-z_\\d']|'(?![A-Za-z_\\d]))\d+", " ", regex=True) \
				.replace('"', '') \
				.replace("[.!?\\-%,():'+]", "", regex=True)
				.str.split() \
				.apply(lambda x: [item for item in x if item not in stop])) \
		.explode('text') \
		.rename(columns={'text': 'word'})

	tidy_tweets = tidy_tweets.dropna(subset=['word'])

	print("Searching for hashtags")

	hashtag_count = tidy_tweets \
		.loc[(tidy_tweets['word'].str.startswith("#"))] \
		.groupby('word') \
		.agg({'word': 'count'}) \
		.rename(columns={'word': 'n'}) \
		.sort_values(by='n', ascending=False)

	hashtag_count['topic'] = df['topic'][0]
	hashtag_count['date_created'] = datetime.now().strftime("%d/%m/%Y")

	hashtag_count = hashtag_count.reset_index()

	save_to_csv(hashtag_count, 'hashtag_count')

	hashtag_count_24h = tidy_tweets \
		.loc[(tidy_tweets['word'].str.startswith("#"))] \
		.loc[(tweets_raw['created_at'] > max(tweets_raw['created_at']) - timedelta(days=1))] \
		.groupby('word') \
		.agg({'word': 'count'}) \
		.rename(columns={'word': 'n'}) \
		.sort_values(by='n', ascending=False)

	hashtag_count_24h['topic'] = df['topic'][0]
	hashtag_count_24h['date_created'] = datetime.now().strftime("%d/%m/%Y")

	hashtag_count_24h = hashtag_count_24h.reset_index()

	save_to_csv(hashtag_count_24h, 'hashtag_count_24h')

	# -------------------------------- TRIGRAMS -----------------------------------------

	print("Searching for trigrams")

	tidy_trigrams = tweets_raw.dropna(subset=['retweeted_status_id']) \
						.loc[:, ['id_str', 'user_screen_name', 'created_at', 'text']] \
		.assign(text=tweets_raw['text']
				.str.lower() \
				.replace("https://t.co/[A-Za-z\\d]+|http://[A-Za-z\\d]+|&amp;|&lt;|&gt;|RT|https", "", regex=True) \
				.replace("([^A-Za-z_\\d']|'(?![A-Za-z_\\d]))\d+", " ", regex=True) \
				.replace('"', '') \
				.replace("[.!?\\-%,():'+]", "", regex=True) \
				.str.split() \
				.apply(lambda x: [item for item in x if item not in stop]) \
				.str.join(' '))

	tidy_trigrams_24h = tidy_trigrams.loc[
		(tidy_trigrams['created_at'] > max(tidy_trigrams['created_at']) - timedelta(days=1))]

	word_vectorizer = CountVectorizer(ngram_range=(3, 3), analyzer='word', token_pattern=r"(?u)\b\w+\b")
	# print(tidy_trigrams['text'])
	sparse_matrix = word_vectorizer.fit_transform(tidy_trigrams['text'])
	frequencies = sum(sparse_matrix).toarray()[0]
	d = {'trigram': word_vectorizer.get_feature_names(), 'n': frequencies}
	trigrams = pd.DataFrame(data=d) \
		.sort_values(by='n', ascending=False)

	trigrams['topic'] = df['topic'][0]
	trigrams['date_created'] = datetime.now().strftime("%d/%m/%Y")

	save_to_csv(trigrams, 'trigrams')

	try:
		sparse_matrix_24 = word_vectorizer.fit_transform(tidy_trigrams_24h['text'])
		frequencies_24 = sum(sparse_matrix_24).toarray()[0]
		d_24 = {'trigram': word_vectorizer.get_feature_names(), 'n': frequencies_24}
		trigrams_24 = pd.DataFrame(data=d_24) \
			.sort_values(by='n', ascending=False)

		trigrams_24['topic'] = df['topic'][0]
		trigrams_24['date_created'] = datetime.now().strftime("%d/%m/%Y")

		save_to_csv(trigrams_24, 'trigrams_24')

	except ValueError:
		None

	# ------------------------------------ URL -------------------------------

	print("Searching for linked URLs")

	url_list = tweets_raw.drop(tweets_raw[tweets_raw.entities_urls == '[]'].index) \
				   .loc[:, ['entities_urls']] \
		.assign(url=tweets_raw['entities_urls']
				.replace("\\[\\{'url': 'htt(\\S)* 'expanded_url': '", "", regex=True) \
				.replace("', 'display_url': '(\\S)*', .*$", "", regex=True)) \
		.groupby('url') \
		.agg({'url': 'count'}) \
		.rename(columns={'url': 'count'}) \
		.sort_values(by='count', ascending=False)

	url_list['topic'] = df['topic'][0]
	url_list['date_created'] = datetime.now().strftime("%d/%m/%Y")

	url_list = url_list.reset_index()

	save_to_csv(url_list, 'url_list')

	url_list_24 = tweets_raw \
					  .drop(tweets_raw[tweets_raw.entities_urls == '[]'].index) \
					  .loc[:, ['entities_urls']] \
		.loc[(tweets_raw['created_at'] > max(tweets_raw['created_at']) - timedelta(days=1))] \
		.assign(url=tweets_raw['entities_urls']
				.replace("\\[\\{'url': 'htt(\\S)* 'expanded_url': '", "", regex=True) \
				.replace("', 'display_url': '(\\S)*', .*$", "", regex=True)) \
		.groupby('url') \
		.agg({'url': 'count'}) \
		.rename(columns={'url': 'count'}) \
		.sort_values(by='count', ascending=False)

	url_list_24['topic'] = df['topic'][0]
	url_list_24['date_created'] = datetime.now().strftime("%d/%m/%Y")

	url_list_24 = url_list_24.reset_index()

	save_to_csv(url_list_24, 'url_list_24')

	# -------------------------------- MOST RETWEETS ---------------------------

	print("Searching for popular retweets")

	tweets_raw['tweet_url'] = tweets_raw.apply(applying_url, axis=1)
	most_retweeted_tweet = tweets_raw.dropna(subset=['retweeted_status_id']) \
		.groupby('text') \
		.agg({'id_str': 'count'}) \
		.rename(columns={'id_str': 'n'}) \
		.sort_values(by='n', ascending=False)

	most_retweeted_tweet['topic'] = df['topic'][0]
	most_retweeted_tweet['date_created'] = datetime.now().strftime("%d/%m/%Y")

	most_retweeted_tweet = most_retweeted_tweet.reset_index()

	save_to_csv(most_retweeted_tweet, 'most_retweeted_tweet')

	most_retweeted_tweet_24h = tweets_raw.dropna(subset=['retweeted_status_id']) \
		.loc[
		(pd.to_datetime(tweets_raw['created_at']) > max(pd.to_datetime(tweets_raw['created_at'])) - timedelta(days=1))] \
		.groupby('text') \
		.agg({'id_str': 'count'}) \
		.rename(columns={'id_str': 'n'}) \
		.sort_values(by='n', ascending=False)

	most_retweeted_tweet_24h['topic'] = df['topic'][0]
	most_retweeted_tweet_24h['date_created'] = datetime.now().strftime("%d/%m/%Y")

	most_retweeted_tweet_24h = most_retweeted_tweet_24h.reset_index()

	save_to_csv(most_retweeted_tweet_24h, 'most_retweeted_tweet_24h')

	# ----------------------- MERGING TO GET THE LINK --------------------------------
	# tweets_filled = tweets_raw['retweeted_status_id'].fillna('0.0', inplace=True)
	# tweets_filled = tweets_raw['retweeted_status_id'].replace(pd.na(), '0.0') #r'^\s*$' regex=True
	tweets_filled = tweets_raw
	tweets_filled = tweets_filled.fillna(value='0.0')
	tweets_orig_url = tweets_filled.loc[tweets_filled.retweeted_status_id == '0.0']

	tweets_org_reduced = tweets_orig_url[['text', 'tweet_url', 'retweeted_status_id']]

	cols = ['text']
	merged_orig = most_retweeted_tweet.join(tweets_org_reduced.set_index(cols), on='text')

	merged_all = merged_orig.loc[~merged_orig.index.duplicated(keep='first')]

	merged_all['topic'] = df['topic'][0]
	merged_all['date_created'] = datetime.now().strftime("%d/%m/%Y")

	find_original_tweet(merged_all, tweets_raw)

	save_to_csv(merged_all, 'merged_all')

	# -----------------------------------

	merged_orig_24 = most_retweeted_tweet_24h.join(tweets_org_reduced.set_index(cols), on='text')

	merged_24 = merged_orig_24.loc[~merged_orig_24.index.duplicated(keep='first')]

	merged_24['topic'] = df['topic'][0]
	merged_24['date_created'] = datetime.now().strftime("%d/%m/%Y")

	find_original_tweet(merged_24, tweets_raw)

	save_to_csv(merged_24, 'merged_24')

	# -------------------------- WHO IS BEING TWEETED THE MOST --------------------

	print("Searching for mentions")

	tweet_accounts = tweets_raw[['text', 'user_name']] \
		.groupby('text') \
		.agg({'user_name': 'count'}) \
		.rename(columns={'user_name': 'n'}) \
		.sort_values(by='n', ascending=False)
	# print('tweet_accounts:', tweet_accounts)
	tweet_account_1 = tweets_orig_url[['text', 'user_name', 'user_screen_name', 'user_verified']]
	# print('tweet_account_1:', tweet_account_1)
	tweet_accounts_2 = tweet_accounts.join(tweet_account_1.set_index(cols), on='text')
	tweet_accounts_2['account_link'] = tweet_accounts_2.apply(apply_account_link, axis=1)
	tweet_accounts_2['user_name'] = tweet_accounts_2.apply(add_tick, axis=1)
	tweet_accounts_2 = tweet_accounts_2.reset_index().dropna(subset=['user_name']) \
		.drop(['user_screen_name', 'text'], axis=1) \
		.set_index('user_name')

	tweet_accounts_2_reset_index = tweet_accounts_2.reset_index()
	percentage_verified = tweet_accounts_2_reset_index.groupby('user_verified').agg({'n': 'sum'})

	percentage_verified['topic'] = df['topic'][0]
	percentage_verified['date_created'] = datetime.now().strftime("%d/%m/%Y")

	percentage_verified = percentage_verified.reset_index()

	save_to_csv(percentage_verified, 'percentage_verified')

	accounts_list = tweet_accounts_2.groupby(['user_name', 'account_link']).agg({'n': 'sum'}).sort_values(by='n',
																										  ascending=False)

	accounts_list['topic'] = df['topic'][0]
	accounts_list['date_created'] = datetime.now().strftime("%d/%m/%Y")

	accounts_list = accounts_list.reset_index()

	save_to_csv(accounts_list[0:50], 'accounts_list')


def mine_topic():
	"""
	Mines tweets
	"""
	df = pd.read_csv(config.file_path + '/' + config.file_name)
	mine_tweets(df)


if __name__ == '__main__':
	mine_topic()
