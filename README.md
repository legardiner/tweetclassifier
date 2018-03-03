# tweetclassifier
Trump or Obama Tweet Classifier for Analytics Value Chain Course

## Product Charter

Boost web traffic by using Presidential Twitter data to create a timely and engaging Trump/Obama tweet classifier to increase blog popularity, number of subscribers, and ultimately advertising revenue.

### Vision
Increase blog popularity, number of subscribers, and ultimately advertising revenue.

### Mission
Boost web traffic by using Presidential tweets to create a timely and engaging Trump/Obama tweet classifier.

### Success Criteria
An accuracy of at least 85% to measure the performance of the text classifier and demonstrate the effectiveness of the web application.

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

Download pretrained word embeddings from [here]http://nlp.stanford.edu/data/glove.twitter.27B.zip
Unzip and store in `/develop/data/external/`

