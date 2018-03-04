import sklearn
import os, sys
sys.path.insert(0, os.path.abspath('.'))
sys.path.append('../../..')
from develop.src.data import getTweets
from develop.src.data import makeDataset
from gensim.models import KeyedVectors
import pickle

def classify_tweet(tweet):
	model_path = './develop/models/model.pkl'
	glove_word2vec_path = './develop/data/external/word2vec.txt'
	cleaned_tweet = getTweets.clean_string(tweet)
	word_embeddings = KeyedVectors.load_word2vec_format(glove_word2vec_path, binary=False)
	tweet_vector = makeDataset.calculate_vector(cleaned_tweet, word_embeddings)
	tweet_vector = tweet_vector.reshape(1, -1)

	model = pickle.load(open(model_path, 'rb'))
	result = model.predict_proba(tweet_vector)
	obama_prob = result[0][0] * 100
	trump_prob = result[0][1] * 100
	classification = model.predict(tweet_vector)
	return obama_prob, trump_prob, classification[0]

def main():
	obama_prob, trump_prob, classification = classify_tweet(tweet)
	print(obama_prob, trump_prob, classification)

if __name__ == "__main__":
	main()