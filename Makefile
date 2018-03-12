develop/data/processed/allTweets.csv: develop/src/data/makeDataset.py develop/src/data/getTweets.py
	python develop/src/data/makeDataset.py

tweets: develop/data/processed/allTweets.csv

develop/models/model.pkl: develop/src/models/trainModel.py
	python develop/src/models/trainModel.py

model: develop/models/model.pkl

all: tweets model
