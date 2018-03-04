from flask import Flask, render_template, request
import os, sys
sys.path.insert(0, os.path.abspath('.'))
sys.path.append('..')
from develop.src.models import predictModel

app = Flask(__name__)


@app.route("/")
def my_form():
	return render_template('tweet_form.html')

@app.route("/", methods=['POST'])
def my_form_post():
	tweet = request.form['tweet']
	obama_prob, trump_prob, classification = predictModel.classify_tweet(tweet)
	return render_template('classifier_results.html', classification=classification, obama_prob=obama_prob, trump_prob=trump_prob)

if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0")