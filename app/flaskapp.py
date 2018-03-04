from flask import Flask, render_template, request
import os, sys
sys.path.insert(0, os.path.abspath('.'))
sys.path.append('..')
from develop.src.models import predictModel
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv, find_dotenv


app = Flask(__name__)


@app.route("/")
def my_form():
	return render_template('tweet_form.html')

@app.route("/", methods=['POST'])
def my_form_post():
	# Get input from form
	tweet = request.form['tweet']
	# Predict tweet classification with user inputed tweet
	obama_prob, trump_prob, classification = predictModel.classify_tweet(tweet)

	# Store results in dataframe to load into database
	df = pd.DataFrame({'tweet': tweet, 'obama_prob': [obama_prob], 'trump_prob': [trump_prob], 'classification': classification})

	# Find .env automagically by walking up directories until it's found
	dotenv_path = find_dotenv()

	# Load up the entries as environment variables
	load_dotenv(dotenv_path)

	# Get connection string from environment variables
	connection_string = os.environ.get("SQLALCHEMY_DATABASE_URI")

	# Create sqlalchemy database connection
	conn = create_engine(connection_string)

	# Append user input and results to database
	df.to_sql('user_tweets', conn, index=False, if_exists='append')

	# Return html page with results
	return render_template('classifier_results.html', classification=classification, obama_prob=obama_prob, trump_prob=trump_prob)

if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0")