import gensim
import numpy as np
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath('.'))
sys.path.append('../../..')
from develop.src.data import makeDataset

glove_vectors_path = '../../../develop/data/external/glove.twitter.27B/glove.twitter.27B.200d.txt'
glove_word2vec_path = '../../../develop/data/external/word2vec.txt'
word_embeddings = makeDataset.load_vectors(glove_vectors_path,
                                           glove_word2vec_path)


def test_load_vectors_type():
    assert type(makeDataset.load_vectors(
            glove_vectors_path,
            glove_word2vec_path)) == \
            gensim.models.keyedvectors.KeyedVectors


def test_load_vectors_dim():
    assert makeDataset.load_vectors(
            glove_vectors_path,
            glove_word2vec_path).vector_size == 200


def test_calculate_vector_type():
    assert type(makeDataset.calculate_vector("this is a tweet classifier",
                                             word_embeddings)) == np.ndarray


def test_calculate_vector_dim():
    assert len(makeDataset.calculate_vector("this is a tweet classifier",
                                            word_embeddings)) == 200


def test_create_df_type():
    assert type(makeDataset.create_df('../../../develop/data/interim',
                                      '../../../develop/data/processed',
                                      word_embeddings)) == \
                                      pd.core.frame.DataFrame


def test_create_df_dim():
    assert makeDataset.create_df('../../../develop/data/interim',
                                 '../../../develop/data/processed',
                                 word_embeddings).shape == (6474, 3)


def test_create_df_cols():
    col_list = ['user', 'tweet', 'tweet_vectors']
    assert sum(makeDataset.create_df('../../../develop/data/interim',
                                     '../../../develop/data/processed',
                                     word_embeddings).columns == col_list) == 3
