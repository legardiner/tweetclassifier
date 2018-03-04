import tweepy
import argparse
from dotenv import load_dotenv, find_dotenv
import os
import re
from os.path import join

parser = argparse.ArgumentParser(description='Scrape users most recent tweets')
parser.add_argument('--screen_name', default = 'realDonaldTrump', help='Screen name to scrape tweets')
parser.add_argument('--output_path', default='../../data/interim', help='Path to directory to store tweets')


def create_API_access():
	"""This function creates twitter API access point.

	Requirements: `CONSUMER_KEY`, `CONSUMER_SECRET`, `ACCESS_TOKEN`, and `ACCESS_SECRET` must be created at https://apps.twitter.com/
	Credential should be stored in a `.env` file in your root directory.

    Returns:
        api: connection object for Twitter API

    """
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

def clean_string(tweet):
	"""This function takes the text from a tweet and clean its according to GloVe's twitter word embeddings preprocessing.
	The ruby script can be found here: https://nlp.stanford.edu/projects/glove/.

	The cleaning includes converting hashtags, usernames, and emojis into readable tokens and removing repitions, urls, commas, and apostrophes

	Args:
		tweet (str): Text string of a user's tweet

	Returns:
		Cleaned tweet text string
	"""
	# Remove new lines
	tweet = re.sub("\n", " ", tweet)
	# Replace urls with token
	tweet = re.sub("https?:\/\/\S+|www\.(\w+\.)+\S*","<url>", tweet)
	# Split words with slashes
	tweet = re.sub("/"," / ", tweet)
	# Remove apostrophes and commas
	tweet = re.sub("['\"’,]", "", tweet)
	# Replace user handles with token
	tweet = re.sub("@\w+", "<user>", tweet)
	# Replace smile with token
	tweet = re.sub("[8:=;]['`\-]?[\)d]|[\(d]['`\-]?[8:=;]", " <smile> ", tweet)
	# Replace sad face with token
	tweet = re.sub("[8:=;]['`\-]?[\(d]|[\)d]['`\-]?[8:=;]", " <sadface> ", tweet)
	# Replace lol face with token
	tweet = re.sub("[8:=;]['`\-]?p", " <lolface> ", tweet)
	# Replace neutral face with token
	tweet = re.sub("[8:=;]['`\-]?[\/|l*]|[\/|l*]['`\-]?[8:=;]", " <neutralface> ", tweet)
	# Repalce heart with token
	tweet = re.sub("<3", " <heart> ", tweet)
	# Replace hashtag with token
	tweet = re.sub("#", "<hashtag> ", tweet)
	# Replace number with token
	tweet = re.sub("[-+]?[.\d]*[\d]+[:,.\d]*", "<number>", tweet)
	# Replace punctuation repetitions with one and token
	tweet = re.sub("([!?.]){2,}", r'\1 <repeat>', tweet)
	# Replace elongated words with regular word and token
	tweet = re.sub('\b(\S*?)(.)\2{2,}\b', r'\1\2 <elong>', tweet)
	# Add padding around punctuation
	tweet = re.sub('([!?.%^&\(\)\[\]${}-])', r' \1 ', tweet)
	# Remove casing
	clean_tweet = tweet.lower()
	return clean_tweet

def get_user_tweets(api, screen_name, output_path):
	"""This function pulls tweet text for a specified username, cleans them with `clean_string`, and outputs to a `.csv`

	Twitter's API only allows you to pull a limited number of tweets at a time.
	Script pulls 200 tweets at a time working backwards in the timeline until the 3400 tweet limit is hit

	Args:
		api (connection object): Connection object for the Twitter API that is returned from `create_API_access`
		screen_name (str): User handle for Twitter user that you want tweets for
		output_path (str): The path to the output directory to store the `.csv` of tweets
	"""

	# Create empty list for tweet objects
	tweets = []
	# Pulls users must recent 200 tweets    
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
	filename = screen_name + '.csv'   
	file = open(join(output_path, filename), 'w') 

	# Iterates through all tweets and cleans them before outputting
	for tweet in tweets:
		clean_tweet = clean_string(tweet.text)
		line = screen_name + ', ' +  clean_tweet + '\n'
		file.write(line)
	print("Done")
	file.close()

def main(screen_name, output_path):
	api = create_API_access()
	get_user_tweets(api, screen_name, output_path)

if __name__ == '__main__':
	args = parser.parse_args()
	screen_name = args.screen_name
	output_path = args.output_path
	main(screen_name, output_path)
    