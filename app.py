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

# Route to Index.html
@app.route("/index.html")
def homepage():
    return render_template("index.html")
# Route to explore.html
@app.route('/explore.html', methods=['GET', 'POST'])
def explore():
    if request.method == 'POST':
        return redirect(url_for('index.html'))
    return render_template('explore.html')
# Route to model.html
@app.route('/model.html', methods=['GET', 'POST'])
def modelpage():
    if request.method == 'POST':
        return redirect(url_for('index.html'))
    return render_template('model.html')
# Route to created_by.html
@app.route('/created_by.html', methods=['GET', 'POST'])
def created_by():
    if request.method == 'POST':
        return redirect(url_for('index.html'))
    return render_template('created_by.html')


# Loading Models
def models_load():
    global tokens1
    global model1
    global tokens2
    global model2
    with open('model/tokenizer1.pickle', 'rb') as f1:
        tokens1 = pickle.load(f1)
        print("Tokenizer1 loaded")

    model1 = load_model('model/model1.h5')
    #model1.summary()
    print("Model1 loaded")
    
    with open('model/tokenizer2.pickle', 'rb') as f2:
        tokens2 = pickle.load(f2)
        print("Tokenizer2 loaded")

    model2 = load_model('model/model2.h5')
    #model2.summary()
    print("Model2 loaded")

    
    
#Function to scrap Tweeter
tweets = []

def username_tweets(username,count):
    
    try:
        
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth,wait_on_rate_limit=True)
        
        # Creation of query method using parameters
        tweets = tweepy.Cursor(api.user_timeline,id=username).items(count)

        # Pulling information from tweets iterable object
        tweets_list = [[username, tweet.created_at, tweet.id, tweet.text] for tweet in tweets]

        # Creation of dataframe from tweets list
        # Add or remove columns as you remove tweet information
        tweets_df = pd.DataFrame(tweets_list,columns=['Username', 'Datetime', 'Tweet Id', 'Text'])
        
        # text = tweets_df['Text']
        # length = len(text)
        # for i in length:
        #     df['Negativity'][i] = model1.predict(pad_sequences(tokens1.texts_to_sequences(text[i]), maxlen=60))
        # negativity = model1.predict(pad_sequences(tokens1.texts_to_sequences("text"), maxlen=60))
        # df = []
        # df = model2.predict(sequence.pad_sequences(tokens2.texts_to_sequences([text]), maxlen=150))
        # html_tab1 = df.to_html()


        html_tab = tweets_df.to_html()
        
        return html_tab

    except BaseException as e:
          print('failed on_status,',str(e))
          time.sleep(3)
        
    
    
                
@app.route('/', methods=['GET', 'POST'])
def tweet_table():
    #if request.method == 'GET':
        #username = request.form()
    if request.method == 'POST':
        count = 10
        username = request.form["tweeter-handle"]
        tab = username_tweets(username,count)

        return render_template('index.html', table=tab)
        

    return render_template('index.html')



@app.route('/pred_model1', methods=['GET', 'POST'])
def pred_model1():
    if request.method == 'POST':
        text = request.form["tweet-text"]
        score1 = str(np.round(100*model1.predict(pad_sequences(tokens1.texts_to_sequences([text]), maxlen=60)),2))
        score1 = score1[2:6]

        pred_text = model2.predict(sequence.pad_sequences(tokens2.texts_to_sequences([text]), maxlen=150))
        df = pd.DataFrame()
        df["toxic"], df["severe_toxic"], df["obscene"],df["threat"],df["insult"],df["identity_hate"] = np.round(100*pred_text.T,2)
        
        score_toxic = str(np.round(df[["toxic"]].values.tolist(),2))
        score_sevtoxic = str(np.round(df[["severe_toxic"]].values.tolist(),2))
        score_obscene = str(np.round(df[["obscene"]].values.tolist(),2))
        score_threat = str(np.round(df[["threat"]].values.tolist(),2))
        score_insult = str(np.round(df[["insult"]].values.tolist(),2))
        score_hate = str(np.round(df[["identity_hate"]].values.tolist(),2))

        score_toxic = score_toxic[2:6]
        score_sevtoxic = score_sevtoxic[2:6]
        score_obscene = score_obscene[2:6]
        score_threat = score_threat[2:6]
        score_insult = score_insult[2:6]
        score_hate = score_hate[2:6]


        # html_tab = df.to_html()
        return render_template('index.html',
                                text=text, 
                                result_mod1=score1, 
                                result_mod2_toxic=score_toxic, 
                                result_mod2_sevtoxic=score_sevtoxic,
                                result_mod2_obscene=score_obscene,
                                result_mod2_threat=score_threat,
                                result_mod2_insult=score_insult,
                                result_mod2_hate=score_insult)
    
    return render_template('index.html')

if __name__ == "__main__":
    models_load()
    app.run(debug=True)
