### FLASK APP for Tweeter scrapping, models prediction and rendering results ###

# Import Libraries
import os
import tweepy
import time
import glob
from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import numpy as np
from keras.models import load_model
import tweepy
from config import consumer_key, consumer_secret, access_token, access_token_secret
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.preprocessing import text, sequence
from flask_table import Table, Col

app = Flask(__name__)

# function to load models


def models_load():
    global model1
    global tokens1
    global model2
    global tokens2

    with open('/Users/user/Desktop/Project3/model/tokenizer1.pickle', 'rb') as f1:
        tokens1 = pickle.load(f1)
        print("Tokenizer1 Loaded")

    model1 = load_model('/Users/user/Desktop/Project3/model/model1.h5')
    print("Model1 Loaded")

    with open('/Users/user/Desktop/Project3/model/tokenizer2.pickle', 'rb') as f2:
        tokens2 = pickle.load(f2)
        print("Tokenizer1 Loaded")

    model2 = load_model('/Users/user/Desktop/Project3/model/model2.h5')
    print("Model1 Loaded")


# function to scrap Tweeter
tweets = []


def username_tweets(username, count):
    try:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True)

        tweets = tweepy.Cursor(api.user_timeline, id=username).items(count)
        tweets_df = pd.DataFrame(tweets_list, columns=[
                                 'Username', 'Datetime', 'Tweet Id', 'Text'])
        html_tab = tweets_df.to_html()
        return html_tab

    except BaseException as e:
        print('failed on_status,', str(e))
        time.sleep(3)


@app.route('/', methods=['GET', 'POST'])
def tweet_table():
    # if request.method == 'GET':
    #username = request.form()
    if request.method == 'POST':
        count = 10
        username = request.form["tweeter-handle"]
        tab = username_tweets(username, count)
        return render_template('index.html', table=tab)

    return render_template('index.html')


@app.route('/pred_model1', methods=['GET', 'POST'])
def pred_model1():
    if request.method == 'POST':
        text = request.form["tweet-text"]
        score1 = model1.predict(pad_sequences(
            tokens1.texts_to_sequences([text]), maxlen=60))
        pred_text = model2.predict(sequence.pad_sequences(
            tokens2.texts_to_sequences([text]), maxlen=150))
        df = pd.DataFrame()
        df["toxic"], df["severe_toxic"], df["obscene"], df["threat"], df["insult"], df["identity_hate"] = pred_text.T
        score2 = df.values.tolist()
        return render_template('index.html', text=text, result_mod1=score1, result_mod2=score2)

    return render_template('index.html')


if __name__ == "__main__":
    models_load()
    app.run(debug=True)
