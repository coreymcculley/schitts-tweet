# <<< Schitts Tweets - Data Bootcamp Project-3 >>>

![proj_logo.png](static/css/Twitter_Code.png)

## Team

Christy Patrick, Igor Pavlunin, Corey McCulley


## Background

The agenda of this project is Twitter sentiment analysis and toxicity classification. In order to satisfy requirements, two NLP models were implemented. The sentiment analysis model identifies whenever a tweet is positive, neutral or negative by returning analysis scores from 0 to 1. Score 0 identifies absolute negative sentiment and Score 1 absolute positive sentiment accordingly. The toxicity model returns prediction scores for 6 categories - hate speech, Insulting, Threating, Obscenity, Toxicity and Severe Toxicity within a range of 0 - 100%. Higher score corresponding to predomination of a given category.

## Brief introduction to NLP

Natural Language Processing (NLP) discipline of computer science, artificial intelligence and linguistics that is concerned with the creation of computational models that process and understand natural language. These include: making the computer understand the semantic grouping of words (e.g. cat and dog are semantically more similar than cat and spoon), text to speech, language translation and many more.

## Models Construction

Model1 - Sequence NLP model that can perform sentiment analysis to categorize tweets as Positive, Negative or Neutral with a gradation pattern depending on score value. Dataset used to train and test model contains 1.6B tweets extracted Twitter API.