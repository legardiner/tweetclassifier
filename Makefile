develop/data/processed/allTweets.csv: develop/src/data/makeDataset.py
	python develop/src/data/makeDataset.py

tweets: develop/data/processed/allTweets.csv

all: tweets