import argparse
import pandas as pd
import getTweets
import os
from os.path import join

parser = argparse.ArgumentParser(description='Make dataset for tweet classifier')
parser.add_argument('--input_path', default='../../data/interim', help='Path to directory to store tweets')
parser.add_argument('--output_path', default='../../data/processed', help='Path to directory to store tweets')


def create_df(input_path, output_path):
	df = pd.DataFrame(columns=['user', 'tweet'])
	for filename in os.listdir(input_path):
		if filename.endswith('.csv'):
			file_path = join(input_path, filename)
			temp_df = pd.read_csv(file_path, names=['user','tweet'])
			df = df.append(temp_df)
	df.to_csv(join(output_path, "allTweets.csv"), index=False)

def main():
	args = parser.parse_args()
	input_path = args.input_path
	output_path = args.output_path
	getTweets.main('realDonaldTrump', input_path)
	getTweets.main('BarackObama', input_path)
	create_df(input_path, output_path)

if __name__ == "__main__":
	main()
