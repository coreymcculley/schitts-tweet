# FLASK APP for Tweeter scrapping, models prediction and rendering results
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
