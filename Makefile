develop/data/processed/allTweets.csv: develop/src/data/makeDataset.py develop/src/data/getTweets.py
	python develop/src/data/makeDataset.py

tweets: develop/data/processed/allTweets.csv

all: tweets
