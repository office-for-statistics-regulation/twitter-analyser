from datetime import datetime
import pandas as pd

pd.options.mode.chained_assignment = None
import numpy as np
import tweepy
import sys
import re
import regex as re
import os

import credentials
import config


def addRow(df, ls):
	"""
	Given a dataframe and a list, append the list as a new row to the dataframe.

	:param df: <DataFrame> The original dataframe
	:param ls: <list> The new row to be added
	:return: <DataFrame> The dataframe with the newly appended row
	"""
	numEl = len(ls)
	newRow = pd.DataFrame(np.array(ls, dtype=object).reshape(1, numEl),
						  columns=['id_str', 'user_id_str', 'in_reply_to_status_id_str', 'in_reply_to_user_id_str',
								   'created_at',
								   'in_reply_to_screen_name', 'source', 'user_name', 'user_screen_name',
								   'user_created_at',
								   'user_statuses_count', 'user_description', 'user_location', 'user_verified',
								   'user_followers_count',
								   'user_friends_count', 'user_url', 'text', 'entities_hashtags', 'entities_urls',
								   'entities_user_mentions',
								   'retweeted_status_id'])
	df = df.append(newRow, ignore_index=True)
	return df


def save_to_csv(df, topic):
	filename = 'tweets.csv'
	save_path = os.path.dirname(os.path.abspath(__file__)) + '/data/' + filename
	return df.to_csv(save_path)


def scraping_topic(search_term, topic):
	print('Scraping tweets on search term:', search_term)
	# auth & api handlers
	auth = tweepy.AppAuthHandler(credentials.consumer_key, credentials.consumer_secret)

	api = tweepy.API(auth, wait_on_rate_limit=True,
					 wait_on_rate_limit_notify=True)

	if (not api):
		print("Can't Authenticate")
		sys.exit(-1)

	# If results from a specific ID onwards are reqd, set since_id to that ID.
	# else default to no lower limit, go as far back as API allows
	sinceId = None

	# If results only below a specific ID are, set max_id to that ID.
	# else default to no upper limit, start from the most recent tweet matching the search query.
	max_id = -1

	df = pd.DataFrame(
		columns=['id_str', 'user_id_str', 'in_reply_to_status_id_str', 'in_reply_to_user_id_str', 'created_at',
				 'in_reply_to_screen_name', 'source', 'user_name', 'user_screen_name', 'user_created_at',
				 'user_statuses_count', 'user_description', 'user_location', 'user_verified', 'user_followers_count',
				 'user_friends_count', 'user_url', 'text', 'entities_hashtags', 'entities_urls',
				 'entities_user_mentions', 'retweeted_status_id'])

	tweetCount = 0
	print(f"Downloading max {config.maxTweets} tweets")

	while tweetCount < config.maxTweets:
		try:
			if (max_id <= 0):
				if (not sinceId):
					new_tweets = api.search(
						q=search_term,
						count=config.tweetsPerQry, geocode="54.265760,-3.194647,430mi", tweet_mode='extended')
				else:
					new_tweets = api.search(
						q=search_term,
						count=config.tweetsPerQry,
						since_id=sinceId, geocode="54.265760,-3.194647,430mi", tweet_mode='extended')
			else:
				if (not sinceId):
					new_tweets = api.search(
						q=search_term,
						count=config.tweetsPerQry,
						max_id=str(max_id - 1), geocode="54.265760,-3.194647,430mi", tweet_mode='extended')
				else:
					new_tweets = api.search(
						q=search_term,
						count=config.tweetsPerQry,
						max_id=str(max_id - 1),
						since_id=sinceId, geocode="54.265760,-3.194647,430mi", tweet_mode='extended')
			if not new_tweets:
				break
			for status in new_tweets:
				if hasattr(status, 'retweeted_status'):  # status.text[0:3] == 'RT ' and
					try:
						retweeted_status_text = status.retweeted_status.full_text
						retweeted_status_id = status.retweeted_status.id_str
					except:
						retweeted_status_text = status.retweeted_status.full_text
						retweeted_status_id = status.retweeted_status.id_str
					try:
						df = addRow(df, [status.id_str, status.user._json['id_str'], status.in_reply_to_status_id_str,
										 status.in_reply_to_user_id_str, status.created_at,
										 status.in_reply_to_screen_name,
										 status.source, status.user._json['name'], status.user._json['screen_name'],
										 status.user._json['created_at'], status.user._json['statuses_count'],
										 status.user._json['description'], status.user._json['location'],
										 status.user._json['verified'], status.user._json['followers_count'],
										 status.user._json['friends_count'], status.user._json['url'],
										 retweeted_status_text,
										 status.entities['hashtags'], status.entities['urls'],
										 status.entities['user_mentions'],
										 retweeted_status_id])
					except Exception as e:
						print(e)
				else:
					try:
						df = addRow(df, [status.id_str, status.user._json['id_str'], status.in_reply_to_status_id_str,
										 status.in_reply_to_user_id_str, status.created_at,
										 status.in_reply_to_screen_name,
										 status.source, status.user._json['name'], status.user._json['screen_name'],
										 status.user._json['created_at'], status.user._json['statuses_count'],
										 status.user._json['description'], status.user._json['location'],
										 status.user._json['verified'], status.user._json['followers_count'],
										 status.user._json['friends_count'], status.user._json['url'],
										 status.full_text, status.entities['hashtags'], status.entities['urls'],
										 status.entities['user_mentions'], ''])
					except:
						try:
							df = addRow(df,
										[status.id_str, status.user._json['id_str'], status.in_reply_to_status_id_str,
										 status.in_reply_to_user_id_str, status.created_at,
										 status.in_reply_to_screen_name,
										 status.source, status.user._json['name'], status.user._json['screen_name'],
										 status.user._json['created_at'], status.user._json['statuses_count'],
										 status.user._json['description'], status.user._json['location'],
										 status.user._json['verified'], status.user._json['followers_count'],
										 status.user._json['friends_count'], status.user._json['url'], status.full_text,
										 status.entities['hashtags'], status.entities['urls'],
										 status.entities['user_mentions'], ''])
						except Exception as e:
							print(e)

			tweetCount += len(new_tweets)
			print(f"Downloaded {tweetCount} tweets")
			max_id = new_tweets[-1].id

		except tweepy.TweepError as e:
			# Just exit if any error'
			print("An Error was found: " + str(e))
			break

	column_list = ['id_str', 'user_id_str', 'in_reply_to_status_id_str', 'in_reply_to_user_id_str',
				   'in_reply_to_screen_name',
				   'source', 'user_name', 'user_screen_name', 'user_created_at', 'user_statuses_count',
				   'user_description',
				   'user_location', 'user_verified', 'user_followers_count', 'user_friends_count', 'user_url', 'text',
				   'entities_hashtags', 'entities_user_mentions', 'retweeted_status_id']

	# for col in list(df.select_dtypes(include='object').columns):
	for col in list(column_list):
		df[col] = df[col].apply(lambda x: re.sub('[^A-Za-z0-9#:/.@"%]+', ' ', str(x)))

	# Add topic and date
	df['topic'] = topic
	df['date'] = datetime.now().strftime("%d/%m/%Y")

	return save_to_csv(df, topic)


def scrape_topic_or_mentions():
	"""
	Either scrape for terms or for mentions of an account

	:param topic_or_mentions: <string> The topic or the account (hard-coded)
	"""

	print(f'Searching terms related to topic or account: {config.topic_or_mentions}')
	scraping_topic(config.search_query, config.topic_or_mentions)


if __name__ == '__main__':
	scrape_topic_or_mentions()
