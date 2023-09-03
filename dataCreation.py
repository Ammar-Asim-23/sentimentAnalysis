import pandas as pd
from pathlib import Path
import nltk

nltk.download('stopwords')
SERVER_FOLDER = Path(__file__).parent.parent.resolve()
commments = pd.read_csv('server/Data/redditData/comment.csv')

import keras
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.layers import Embedding, LSTM, Dense, Dropout, SpatialDropout1D, Bidirectional, Flatten, BatchNormalization
import tensorflow as tf
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
import re
import numpy as np


def commentCleaner(comments):
    cleaned_comments = []
    for comment in comments:
        # Remove special symbols, emojis, reddit username mentions, and hyperlinks
        comment = re.sub(r"[^\w\s]|http\S+|www\S+|u/[A-Za-z0-9_-]+", "", comment)
        comment = comment.lower()
        # Tokenize the comment
        tokens = comment.split()
        # tokens = comment.split(' ')
        # Remove stop words
        stop_words = set(stopwords.words("english"))
        tokens = [token for token in tokens if token not in stop_words]
        
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(token) for token in tokens]
        
        # Join the tokens back into a single string
        cleaned_comment = " ".join(tokens)
        cleaned_comments.append(cleaned_comment)   
    return cleaned_comments


def tokenizeComments(comments, tokenizer):
    print("Comments recieved for tokenization: ")
    print(comments)
    print("Fitted tokenizer to sample texts")
    tokenized_comments = tokenizer.texts_to_sequences(comments)
    print("Converted to sequences")
    tokenized_comments = pad_sequences(tokenized_comments, 235)
    print("Padded succesfully")
    print(tokenized_comments)
    return tokenized_comments

cleaned_comments = commentCleaner(commments['Comment'])
tokenized_comments = tokenizeComments(cleaned_comments, Tokenizer())
print(tokenized_comments)