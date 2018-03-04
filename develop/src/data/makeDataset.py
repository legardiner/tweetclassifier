import argparse
import pandas as pd
import getTweets
import os
from os.path import join
from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.models import KeyedVectors

parser = argparse.ArgumentParser(description='Make dataset for tweet classifier')
parser.add_argument('--input_path', default='./develop/data/interim', help='Path to directory to read in tweets')
parser.add_argument('--output_path', default='./develop/data/processed', help='Path to directory to store dataframe')
parser.add_argument('--user1', default='realDonaldTrump', help='First user Twitter handle')
parser.add_argument('--user2', default='BarackObama', help='Second user Twitter handle')
parser.add_argument('--glove_vectors_path', default='./develop/data/external/glove.twitter.27B/glove.twitter.27B.200d.txt', help='Path to directory containing glove vectors')
parser.add_argument('--glove_word2vec_path', default='./develop/data/external/word2vec.txt', help='Path to directory containing glove vectors')

def load_vectors(glove_vectors_path, glove_word2vec_path):
    glove2word2vec(glove_vectors_path, glove_word2vec_path)
    word_embeddings = KeyedVectors.load_word2vec_format(glove_word2vec_path, binary=False)
    return word_embeddings

def calculate_vector(tweet, word_embeddings):
    """This function utilizes GloVe pretrained Twitter word vectors to calculate an averaged sentence embeding for each tweet.
    Word embeddings are averaged and not summed to not give larger weight to sentences with more words.

    TO-DO: Further improvement on calculations could be done by weight with TF-IDF

    Args:
        tweet (str): Cleaned text string of a user's tweet
        glove_vectors_path (str): Path to the data directory where the glove vectors are stored
        glove_word2vec_path (str): Path to store the glove vectors once they've been transformed to the word2vec load_word2vec_format

    Returns:
        A tweet embedding that consists of an average of the word embeddings that make up the sentences
    """

    # Tokenize tweet
    tokens = tweet.split()
    counter = 0
    # Iterate through tokens and get their vector value
    for token in tokens:
        counter += 1
        if counter == 1:
            if token in word_embeddings.wv.vocab:
                tweet_vec = word_embeddings[token]
            else:
                counter = 0
        else:
            if token in word_embeddings.wv.vocab:
                tweet_vec = tweet_vec + word_embeddings[token]
            else:
                counter -= 1
    avg_tweet_vec = (tweet_vec / counter)
    return avg_tweet_vec

def create_df(input_path, output_path, word_embeddings):
	"""This function reads all outputed `.csv` from the interim data directory and combines them into a single data frame

	Args:
		input_path (str): The path to the input directory to read in tweet `.csv` for each user
		output_path (str): The path to the output directory to store the `.csv` of all tweets
	"""
	df = pd.DataFrame(columns=['user', 'tweet'])
	for filename in os.listdir(input_path):
		if filename.endswith('.csv'):
			file_path = join(input_path, filename)
			temp_df = pd.read_csv(file_path, names=['user','tweet'])
			df = df.append(temp_df)
	df['tweet_vectors'] = df['tweet'].apply(lambda x: calculate_vector(x, word_embeddings))
	df.to_csv(join(output_path, "allTweets.csv"), index=False)


def main():
	args = parser.parse_args()
	input_path = args.input_path
	output_path = args.output_path
	user1 = args.user1
	user2 = args.user2
	glove_vectors_path = args.glove_vectors_path
	glove_word2vec_path = args.glove_word2vec_path


	getTweets.main(user1, input_path)
	getTweets.main(user2, input_path)
	word_embeddings = load_vectors(glove_vectors_path, glove_word2vec_path)
	create_df(input_path, output_path, word_embeddings)

if __name__ == "__main__":
	main()
