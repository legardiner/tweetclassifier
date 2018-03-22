import gensim
import numpy as np
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath('.'))
sys.path.append('../../..')
from develop.src.models import trainModel
from develop.src.models import predictModel

input_path = '../../../develop/data/processed/allTweets.csv'
output_path = '../../../develop/models/model.pkl'


def test_load_data_type():
    assert type(trainModel.load_data(input_path)) == tuple


def test_load_data_X_type():
    assert type(trainModel.load_data(input_path)[0]) == np.ndarray


def test_load_data_X_dim():
    assert trainModel.load_data(input_path)[0].shape == (6474, 200)


def test_load_data_y_type():
    assert type(trainModel.load_data(input_path)[1]) == pd.core.series.Series


def test_load_data_y_dim():
    assert trainModel.load_data(input_path)[1].shape == (6474,)


def test_classify_tweet_type():
    assert type(predictModel.classify_tweet("this is a test")) == tuple


def test_classify_tweet_obama_prob_type():
    assert type(predictModel.classify_tweet("this is a test")[0]) == float


def test_classify_tweet_trump_prob_type():
    assert type(predictModel.classify_tweet("this is a test")[1]) == float


def test_classify_tweet_classification_type():
    assert type(predictModel.classify_tweet("this is a test")[0]) == str
