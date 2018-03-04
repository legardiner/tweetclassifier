from flask import Flask, render_template, request
import os, sys
sys.path.insert(0, os.path.abspath('.'))
sys.path.append('..')
from develop.src.models import predictModel
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, select
from dotenv import load_dotenv, find_dotenv


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)



@app.route("/")
def my_form():
	return render_template('tweet_form.html')

@app.route("/", methods=['POST'])
def my_form_post():
	# Get input from form
	user_tweet = request.form['tweet']

	# Find .env automagically by walking up directories until it's found
	dotenv_path = find_dotenv()

	# Load up the entries as environment variables
	load_dotenv(dotenv_path)

	# Get connection string from environment variables
	connection_string = os.environ.get("SQLALCHEMY_DATABASE_URI")

	# Create sqlalchemy database connection
	conn = create_engine(connection_string)
	# Get user_tweets table
	meta = MetaData(conn,reflect=True)
	table = meta.tables['user_tweets']
	# Query to check if tweet is in table
	select_st = select([table]).where(table.c.tweet == user_tweet)
	result = conn.execute(select_st)
	count = 0
	obama_prob = 0
	trump_prob = 0
	classification = ''
	for row in result:
		count += 1
	if count == 0:
		# Predict tweet classification with user inputed tweet
		obama_prob, trump_prob, classification = predictModel.classify_tweet(user_tweet)

		# Store results in dataframe to load into database
		df = pd.DataFrame({'tweet': user_tweet, 'obama_prob': [obama_prob], 'trump_prob': [trump_prob], 'classification': classification})

		# Append user input and results to database
		df.to_sql('user_tweets', conn, index=False, if_exists='append')
	else:
		select_st = select([table]).where(table.c.tweet == user_tweet)
		result = conn.execute(select_st)
		results = []
		for row in result:
			results.append(row)
		obama_prob = results[0][1]
		trump_prob = results[0][2]
		classification = results[0][0]

	# Return html page with results
	return render_template('classifier_results.html', classification=classification, obama_prob=obama_prob, trump_prob=trump_prob)

if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0")