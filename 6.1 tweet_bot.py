import tweepy
import time

# getting authentication keys for authorization

all_keys = open("twitterkeys.txt", "r").read().splitlines()
consumer_key = all_keys[0]
consumer_secret = all_keys[1]
access_key = all_keys[2]
access_secret = all_keys[3]

# authorization

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

# creating tweepy object

api = tweepy.API(auth)

# verifying credentials

try:
    api.verify_credentials()
    print("Authentication Ok")
except:
    print("Error during exception")

# defining functions to read and store last id that have been checked by the bot

def last_seen(file):
    file_to_read = open(file, 'r')
    last_seen_id = int(file_to_read.read().strip())
    file_to_read.close()
    return (last_seen_id)

def store_seen(file, last_seen_id):
    file_to_write = open(file, 'w')
    file_to_write.write(str(last_seen_id))
    file_to_write.close()
    return

# defining function for replying to happy birthday wishes

def reply():
    tweets = api.mentions_timeline(since_id=last_seen("seen.txt"), tweet_mode='extended')
    # most recent tweets are output first, so we have to reverse the order
    for tweet in reversed(tweets):
        if '#happybirthday' in tweet.full_text:  # to see full text
            api.update_status(status="@" + tweet.user.screen_name + "  Thank you :)", in_reply_to_status_id=tweet.id) # reply to the tweet
            api.create_favorite(tweet.id) # like the tweet
            api.retweet(tweet.id) # retweet the tweet
            store_seen("seen.txt", tweet.id)


while True:
    reply()
    time.sleep(15)
