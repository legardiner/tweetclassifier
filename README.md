# tweetclassifier
Trump or Obama Tweet Classifier for Analytics Value Chain Course

Vincent Wang, Product Manager
Lauren Gardiner, Developer
Rishabh Joshi, Quality Assurance

## Product Charter

Boost web traffic by using Presidential Twitter data to create a timely and engaging Trump/Obama tweet classifier to increase blog popularity, number of subscribers, and ultimately advertising revenue.

### Vision
Increase blog popularity, number of subscribers, and ultimately advertising revenue.

### Mission
Boost web traffic by using Presidential tweets to create a timely and engaging Trump/Obama tweet classifier.

### Success Criteria
An accuracy of at least 85% to measure the performance of the text classifier and demonstrate the effectiveness of the web application.

The Pivotal Tracker associated with the project can be viewed [here](https://www.pivotaltracker.com/n/projects/2143919)

## Getting Started

### Set Up Your Virtual Environment

Create a new virtual environment

```
virtualenv -p python3 TweetClassifier
source TweetClassifier/bin/activate
```

Install requirements

```
pip install -r requirements.txt
```

### Get GloVe vectors

Download pretrained word embeddings from [here](http://nlp.stanford.edu/data/glove.twitter.27B.zip)
Unzip and store in `/develop/data/external/`

### Set up your `.evn` file

Please create a `.env` file at your local directory and include the following your `CONSUMER_KEY` (Twitter), `CONSUMER_SECRET` (Twitter), ACCESS_TOKEN (Twitter), `ACCESS_SECRET`, and  `SQLALCHEMY_DATABASE_URI` (RDS Connection String)

### Run tests on code

```
cd develop/src/tests
py.tests
```

### Run code

```
cd ../../..
make all
python app/flaskapp.py
```

You can then go to the IP address where the app is running and use the app.
