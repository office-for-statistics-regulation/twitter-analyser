import pandas as pd
import plotly.graph_objects as go
import layouts

# -------------------------- GENERAL -------------------------------
# --------------------------            -------------------------------
# ----------------------- Most retweeted 24 hours ------------------

most_retweet_24 = pd.read_csv('data/merged_24.csv')


# ----------------------- Most retweeted all time ------------------

most_retweeted_tweet = pd.read_csv('data/merged_all.csv')

# ---------------------- Other retweeted 24 hr ---------------------

other_retweet_24 = pd.read_csv('data/merged_24.csv', skiprows=range(1, 2))
other_retweet_24 = other_retweet_24.rename(columns={"text": "Tweet", "n": "Number of retweets", "tweet_url": "Link to tweet"})

# ---------------------- Other retweeted all ---------------------

other_retweet_all = pd.read_csv('data/merged_all.csv', skiprows=range(1, 2))
other_retweet_all = other_retweet_all.rename(columns={"text": "Tweet", "n": "Number of retweets", "tweet_url": "Link to tweet"})

# ----------------------- Hashtags 24 hr ------------------

hashtags_24 = pd.read_csv('data/hashtag_count_24h.csv')
hashtags_24 = hashtags_24.head(30)

data_1 = go.Bar(y=hashtags_24['word'], x=hashtags_24['n'], orientation='h', marker_color='#6495ED')
hashtag_24_fig = go.Figure(data=data_1, layout=layouts.layout_hashtag_24)

# ----------------------- Hashtags all ------------------

hashtags_all = pd.read_csv('data/hashtag_count.csv')
hashtags_all = hashtags_all.head(30)


data_2 = go.Bar(y=hashtags_all['word'], x=hashtags_all['n'], orientation='h', marker_color='#6495ED')
hashtag_all_fig = go.Figure(data=data_2, layout=layouts.layout_hashtag_all)

# ----------------------- Trigrams 24 hr ------------------

trigrams_24 = pd.read_csv('data/trigrams_24h.csv')
trigrams_24 = trigrams_24.head(30)



data_3 = go.Bar(y=trigrams_24['trigram'], x=trigrams_24['n'], orientation='h', marker_color='#6495ED')
trigrams_24_fig = go.Figure(data=data_3, layout=layouts.layout_trigram_24)

# ----------------------- Trigrams all ------------------

trigrams_all = pd.read_csv('data/trigrams.csv')
trigrams_all = trigrams_all.head(30)

data_4 = go.Bar(y=trigrams_all['trigram'], x=trigrams_all['n'], orientation='h', marker_color='#6495ED')
trigrams_all_fig = go.Figure(data=data_4, layout=layouts.layout_trigram_all)

# ---------------------- url 24 hour ---------------------

url_24 = pd.read_csv('data/url_list_24h.csv', header=0)
url_24 = url_24.rename(columns={"url": "Popular url", "count": "number of mentions"})

# ---------------------- url 24 hour ---------------------

url_all = pd.read_csv('data/url_list.csv', header=0)
url_all = url_all.rename(columns={"url": "Popular url", "count": "number of mentions"}).head(30)

# ----------------------- Number of tweets per hour ------------------
tweets_per_hour = pd.read_csv('data/tweets_per_hour.csv')

data = go.Bar(x=tweets_per_hour['time_floor'], y=tweets_per_hour['tweet_count'], marker_color='#6495ED')
tweets_per_hour_fig = go.Figure(data=data, layout=layouts.layout_num_tweets_per_hour)


# -------------------------- EDUCATION -------------------------------
# --------------------------            -------------------------------

# ----------------------- Most retweeted 24 hours loneliness ------------------

most_retweet_24_e = pd.read_csv('data/education/merged_24.csv')

# ----------------------- Most retweeted all time ------------------

most_retweeted_tweet_e = pd.read_csv('data/education/merged_all.csv')

# ---------------------- Other retweeted 24 hr ---------------------

other_retweet_24_e = pd.read_csv('data/education/merged_24.csv', skiprows=range(1, 2))
other_retweet_24_e = other_retweet_24_e.rename(columns={"text": "Tweet", "n": "Number of retweets", "tweet_url": "Link to tweet"})

# ---------------------- Other retweeted all ---------------------

other_retweet_all_e = pd.read_csv('data/education/merged_all.csv', skiprows=range(1, 2))
other_retweet_all_e = other_retweet_all_e.rename(columns={"text": "Tweet", "n": "Number of retweets", "tweet_url": "Link to tweet"})

# ----------------------- Hashtags 24 hr ------------------

hashtags_24_e = pd.read_csv('data/education/hashtag_count_24h.csv')
hashtags_24_e = hashtags_24_e.head(30)

data_1_e = go.Bar(y=hashtags_24_e['word'], x=hashtags_24_e['n'], orientation='h', marker_color='#6495ED')
hashtag_24_fig_e = go.Figure(data=data_1_e, layout=layouts.layout_hashtag_24)

# ----------------------- Hashtags all ------------------

hashtags_all_e = pd.read_csv('data/education/hashtag_count.csv')
hashtags_all_e = hashtags_all_e.head(30)


data_2_e = go.Bar(y=hashtags_all_e['word'], x=hashtags_all_e['n'], orientation='h', marker_color='#6495ED')
hashtag_all_fig_e = go.Figure(data=data_2_e, layout=layouts.layout_hashtag_all)

# ----------------------- Trigrams 24 hr ------------------

trigrams_24_e = pd.read_csv('data/education/trigrams_24h.csv')
trigrams_24_e = trigrams_24_e.head(30)


data_3_e = go.Bar(y=trigrams_24_e['trigram'], x=trigrams_24_e['n'], orientation='h', marker_color='#6495ED')
trigrams_24_fig_e = go.Figure(data=data_3_e, layout=layouts.layout_trigram_24)

# ----------------------- Trigrams all ------------------

trigrams_all_e = pd.read_csv('data/education/trigrams.csv')
trigrams_all_e = trigrams_all_e.head(30)

data_4_e = go.Bar(y=trigrams_all_e['trigram'], x=trigrams_all_e['n'], orientation='h', marker_color='#6495ED')
trigrams_all_fig_e = go.Figure(data=data_4_e, layout=layouts.layout_trigram_all)

# ---------------------- url 24 hour ---------------------

url_24_e = pd.read_csv('data/education/url_list_24h.csv', header=0)
url_24_e = url_24_e.rename(columns={"url": "Popular url", "count": "number of mentions"})

# ---------------------- url 24 hour ---------------------

url_all_e = pd.read_csv('data/education/url_list.csv', header=0)
url_all_e = url_all_e.rename(columns={"url": "Popular url", "count": "number of mentions"}).head(30)

# ----------------------- Number of tweets per hour ------------------
tweets_per_hour_e = pd.read_csv('data/education/tweets_per_hour.csv')

data_e = go.Bar(x=tweets_per_hour_e['time_floor'], y=tweets_per_hour_e['tweet_count'], marker_color='#6495ED')
tweets_per_hour_fig_e = go.Figure(data=data_e, layout=layouts.layout_num_tweets_per_hour)