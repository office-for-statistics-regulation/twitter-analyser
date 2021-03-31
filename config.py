import os

# Save and load path. Normally output folder in root directory.
file_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'output'))
file_name = 'tweets.csv'

# Tweepy Config
maxTweets = 10000
tweetsPerQry = 100  # this is the max the API permits

# Twitter Searches
topic_or_mentions = 'covid_data'
search_query = '(coronavirus AND government AND data)'

# ------ OR -------

# topic_or_mentions = 'OSR'
# search_query = '@UKStatsAuth OR @StatsRegulation -filter:retweets'
