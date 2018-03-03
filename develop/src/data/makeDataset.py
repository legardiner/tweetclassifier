import argparse
import pandas as pd
import getTweets
import os
from os.path import join

parser = argparse.ArgumentParser(description='Make dataset for tweet classifier')
parser.add_argument('--input_path', default='./develop/data/interim', help='Path to directory to read in tweets')
parser.add_argument('--output_path', default='./develop/data/processed', help='Path to directory to store dataframe')
parser.add_argument('--user1', default='realDonaldTrump', help='First user Twitter handle')
parser.add_argument('--user2', default='BarackObama', help='Second user Twitter handle')

def create_df(input_path, output_path):
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
	df.to_csv(join(output_path, "allTweets.csv"), index=False)

def main():
	args = parser.parse_args()
	input_path = args.input_path
	output_path = args.output_path
	user1 = args.user1
	user2 = args.user2
	getTweets.main(user1, input_path)
	getTweets.main(user2, input_path)
	create_df(input_path, output_path)

if __name__ == "__main__":
	main()
