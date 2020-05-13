import tweepy
import csv
import sys
import pandas as pd
from twitter_authentication import *

Education = False

# Enter each search term inside quotes, between 'OR'e.g.  .
# The whole search query should be inside a single string.
if Education == True:
    search_query = '(coronavirus AND school AND closure) OR (covid AND school AND closure) OR (coronavirus AND school AND opening) OR (covid AND school AND opening) OR (coronavirus AND school AND statistics) OR (covid AND school AND statistics) OR (coronavirus AND school AND figures) OR (coronavirus AND schools)' # example search terms
    filename = 'data/education/sources/tweets.csv'
else:
    search_query = '(coronavirus AND data) OR (coronavirus AND statistics)' # example search terms
    filename = 'data/sources/tweets.csv'

maxTweets = 10000


# auth & api handlers
auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)

api = tweepy.API(auth, wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True)

if (not api):
    print("Can't Authenticate")
    sys.exit(-1)

tweetsPerQry = 100  # this is the max the API permits

# If results from a specific ID onwards are reqd, set since_id to that ID.
# else default to no lower limit, go as far back as API allows
sinceId = None

# If results only below a specific ID are, set max_id to that ID.
# else default to no upper limit, start from the most recent tweet matching the search query.
max_id = -1

# create output file and add header
with open(filename, 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    header = ['id_str', 'user_id_str', 'in_reply_to_status_id_str', 'in_reply_to_user_id_str', 'created_at',
              'in_reply_to_screen_name', 'source', 'user_name', 'user_screen_name', 'user_created_at',
              'user_statuses_count', 'user_description', 'user_location', 'user_verified', 'user_followers_count',
              'user_friends_count', 'user_url', 'text', 'entities_hashtags', 'entities_urls', 'entities_user_mentions',
              'retweeted_status_id']
    writer.writerow(header)


# function for adding data to csv file
def write_csv(row_data, filename):
    with open(filename, 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(row_data)


tweetCount = 0
print("Downloading max {0} tweets".format(maxTweets))
while tweetCount < maxTweets:
    try:
        if (max_id <= 0):
            if (not sinceId):
                new_tweets = api.search(
                    q=search_query,
                    count=tweetsPerQry, geocode="54.265760,-3.194647,430mi", tweet_mode='extended')
            else:
                new_tweets = api.search(
                    q=search_query,
                    count=tweetsPerQry,
                    since_id=sinceId, geocode="54.265760,-3.194647,430mi", tweet_mode='extended')
        else:
            if (not sinceId):
                new_tweets = api.search(
                    q=search_query,
                    count=tweetsPerQry,
                    max_id=str(max_id - 1), geocode="54.265760,-3.194647,430mi", tweet_mode='extended')
            else:
                new_tweets = api.search(
                    q=search_query,
                    count=tweetsPerQry,
                    max_id=str(max_id - 1),
                    since_id=sinceId, geocode="54.265760,-3.194647,430mi", tweet_mode='extended')
        if not new_tweets:
            print("No more tweets found")
            break
        for status in new_tweets:
            if hasattr(status, 'retweeted_status'): #status.text[0:3] == 'RT ' and
                try:
                    retweeted_status_text = status.retweeted_status.full_text
                    retweeted_status_id = status.retweeted_status.id_str
                except:
                    retweeted_status_text = status.retweeted_status.full_text
                    retweeted_status_id = status.retweeted_status.id_str
                try:
                    write_csv([status.id_str, status.user._json['id_str'], status.in_reply_to_status_id_str,
                               status.in_reply_to_user_id_str, status.created_at, status.in_reply_to_screen_name,
                               status.source, status.user._json['name'], status.user._json['screen_name'],
                               status.user._json['created_at'], status.user._json['statuses_count'],
                               status.user._json['description'], status.user._json['location'],
                               status.user._json['verified'], status.user._json['followers_count'],
                               status.user._json['friends_count'], status.user._json['url'], retweeted_status_text,
                               status.entities['hashtags'], status.entities['urls'], status.entities['user_mentions'],
                               retweeted_status_id], filename)
                except Exception as e:
                    print(e)
            else:
                try:
                    write_csv([status.id_str, status.user._json['id_str'], status.in_reply_to_status_id_str,
                               status.in_reply_to_user_id_str, status.created_at, status.in_reply_to_screen_name,
                               status.source, status.user._json['name'], status.user._json['screen_name'],
                               status.user._json['created_at'], status.user._json['statuses_count'],
                               status.user._json['description'], status.user._json['location'],
                               status.user._json['verified'], status.user._json['followers_count'],
                               status.user._json['friends_count'], status.user._json['url'],
                               status.full_text, status.entities['hashtags'], status.entities['urls'],
                               status.entities['user_mentions'], ''], filename)
                except:
                    try:
                        write_csv([status.id_str, status.user._json['id_str'], status.in_reply_to_status_id_str,
                                   status.in_reply_to_user_id_str, status.created_at, status.in_reply_to_screen_name,
                                   status.source, status.user._json['name'], status.user._json['screen_name'],
                                   status.user._json['created_at'], status.user._json['statuses_count'],
                                   status.user._json['description'], status.user._json['location'],
                                   status.user._json['verified'], status.user._json['followers_count'],
                                   status.user._json['friends_count'], status.user._json['url'], status.full_text,
                                   status.entities['hashtags'], status.entities['urls'],
                                   status.entities['user_mentions'], ''], filename)
                    except Exception as e:
                        print(e)
        tweetCount += len(new_tweets)
        print("Downloaded {0} tweets".format(tweetCount))
        max_id = new_tweets[-1].id
    #        time.sleep(0.25)
    except tweepy.TweepError as e:
        # Just exit if any error
        print("some error : " + str(e))
        break

print("Downloaded {0} tweets, Saved to {1}".format(tweetCount, filename))

