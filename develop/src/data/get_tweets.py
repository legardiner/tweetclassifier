import tweepy
import argparse
from dotenv import load_dotenv, find_dotenv
import os

parser = argparse.ArgumentParser(description='Scrape users most recent tweets')
parser.add_argument('--screen_name', default = 'realDonaldTrump', help='Screen name to scrape tweets')
parser.add_argument('--output_path', default='../../data/interim', help='Path to directory to store tweets')


def create_API_access():
	# Find .env automagically by walking up directories until it's found
	dotenv_path = find_dotenv()

	# Load up the entries as environment variables
	load_dotenv(dotenv_path)

	# Get Twitter API credentials from environment variables
	consumer_key = os.environ.get("CONSUMER_KEY")
	consumer_secret = os.environ.get("CONSUMER_SECRET")
	access_token = os.environ.get("ACCESS_TOKEN")
	access_secret = os.environ.get("ACCESS_SECRET")

	# Set up authorization to Twitter API
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)

	# Create connection object
	api = tweepy.API(auth)
	return api

def get_user_tweets(api, screen_name):
	""" Twitter's API only allows you to pull a limited number of tweets at a time.
	Script pulls 200 tweets at a time working backwards in the timeline until the 3400 tweet limit is hit"""

	# Create empty list for tweet objects
    tweets = []
    # Pulls must recent 200 tweets    
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    tweets.extend(new_tweets) 
    oldest = tweets[-1].id - 1
    
    # Continues to pull tweets 200 at a time until limit is hit
    while len(new_tweets) > 0:
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        tweets.extend(new_tweets)
        oldest = tweets[-1].id - 1

        print("...%s tweets downloaded so far" % (len(tweets)))
    
    # Write all text of tweets to a file
    filename = screen_name + '.txt'   
    file = open(join(output_path, filename), 'w') 
    for tweet in tweets:
    	line = tweet.text + '\n'
    	file.write(line)
    print("Done")
    file.close()

def main():
	args = parser.parse_args()
	screen_name = args.screen_name
	output_path = args.output_path

	api = create_API_access()
	get_user_tweets(api, screen_name)

if __name__ == '__main__':
	main()
    