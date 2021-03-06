from gensim.models import KeyedVectors
import pickle
import os
import sys
sys.path.insert(0, os.path.abspath('.'))
sys.path.append('../../../develop/src/data/')
import getTweets
import makeDataset


def classify_tweet(tweet):
    """This function predicts a tweet classification for a given text string.

    Args:
        tweet (str): Tweet text string to classify

    Returns:
        A classification for the tweet and its probability for the two classes.
    """
    model_path = './develop/models/model.pkl'
    glove_word2vec_path = './develop/data/external/word2vec.txt'

    # Clean text string
    cleaned_tweet = getTweets.clean_string(tweet)
    # Load word embeddings
    word_embeddings = KeyedVectors.load_word2vec_format(glove_word2vec_path,
                                                        binary=False)
    # Convert text string into vector representation
    tweet_vector = makeDataset.calculate_vector(cleaned_tweet, word_embeddings)
    # Reshape array for single sample skleanr prediction
    tweet_vector = tweet_vector.reshape(1, -1)

    # Load pickled model
    model = pickle.load(open(model_path, 'rb'))
    # Predict probability of each class
    result = model.predict_proba(tweet_vector)
    obama_prob = result[0][0] * 100
    trump_prob = result[0][1] * 100
    # Predict class
    classification = model.predict(tweet_vector)
    return obama_prob, trump_prob, classification[0]
