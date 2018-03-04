import pandas as pd
import sklearn
import numpy as np
from sklearn import model_selection
from sklearn import svm
import pickle
import argparse

parser = argparse.ArgumentParser(description='Train tweet clasificaiton model')
parser.add_argument('--input_path', default='./develop/data/processed/allTweets.csv', help='Path to directory to read in all tweets')
parser.add_argument('--output_path', default='./develop/models/model.pkl', help='Path to directory to store pickled model')

def load_data(input_path):
	"""This function loads in the `.csv` file contained the data, converts the vector string into a numpy array, and 
	returns the X and Y values for model input

    Args:
        input_path (str): Path to dataset

    Returns:
        X and Y values for model input
    """
	df = pd.read_csv(input_path)
	df['tweet_vectors'] = df['tweet_vectors'].apply(lambda x: 
							np.fromstring(x.replace('\n','')
								.replace('[','')
								.replace(']','')
								.replace('  ',' '), sep=' ', dtype='float32'))
	X = df['tweet_vectors']
	X = np.array(list(X), dtype=np.float)
	y = df['user']
	return X, y

def train_model(X, y, output_path):
	"""This function trains the model with sklearn and pickles the model for later user. Model development was done in a Jupyter notebook
	and chosen with cross-validation accuracy as the performance metric.

	Args:
		y (Series): Series of labels of tweets
		X (Series): Series of vector representations of tweet text
		output_path (str): Path to store pickled model

	"""
	# X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2, random_state=0)
	# Fit the model on 33%
	model = svm.SVC(kernel='linear', probability=True)
	model.fit(X, y)
	# save the model to disk
	pickle.dump(model, open(output_path, 'wb'))

def main():
	args = parser.parse_args()
	input_path = args.input_path
	output_path = args.output_path

	X, y = load_data(input_path)
	train_model(X, y, output_path)

if __name__ == '__main__':
	main()