import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.preprocessing import LabelEncoder
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from data_cleaning import *

class OVR_SVC:

    def __init__(self, data):
        self.X = data['clean-text']
        self.y = data['category']

        le = LabelEncoder()
        self.y = le.fit_transform(self.y)

        self.reference = dict(zip(data['category'].to_numpy()), y)
        self.reference = {k:v for k,v in sorted(self.reference.items(), key=lambda item: item[1])}

        self.model = OneVsRestClassifier(LinearSVC(random_state=0))

        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.3)

    def vectorizer(self, type='tfidf'):
        if type == 'tfidf':
            vectorizer = TfidfVectorizer()
        elif type == 'count':
            vectorizer = CountVectorizer()

        self.x_train = vectorizer.fit_transform(self.x_train)
        self.x_test = vectorizer.transform(self.x_test)
    
    def train_model(self):
        self.model.fit(self.x_train, self.y_train)
    
    def evaluate_model(self):
        y_predicted = self.model.predict(self.x_test)
        accuracy = self.model.score(self.x_test, self.y_test)


class TweetCategory:

    def __init__(self, model, vectorizer, tweet_data, reference):
        self.data = tweet_data
        self.model = model
        self.vectorizer = vectorizer
        self.ref = reference
        self.analyzer = SentimentIntensityAnalyzer()

    def process_user_tweets(self):
        self.data['clean-tweet'] = self.data['Tweet Content'].map(tweet_preprocess)
        self.data = self.data[['Tweet Content', 'clean-tweet']].rename(columns={'Tweet Content': 'tweet'})

        self.data['vader-sentiment'] = self.data['tweet'].apply(lambda x: self.analyzer.polarity_scores(x))
        self.data['vader-pos'] = self.data['vader-sentiment'].apply(lambda x: x['pos'])
        self.data['vader-neu'] = self.data['vader-sentiment'].apply(lambda x: x['neu'])
        self.data['vader-neg'] = self.data['vader-sentiment'].apply(lambda x: x['neg'])
        self.data['vader-compound'] = self.data['vader-sentiment'].apply(lambda x: x['compound'])


    def predict_topics(self, sentiment_thresh, confidence_thresh):
        self.predict_df = self.data[(self.data['vader-compound'] >= sentiment_thresh) & (self.data['clean-tweet'] != '')]
        
        tweets_transformed = self.vectorizer.transform(self.predict_df['clean-tweet'])
        predicted_category = self.model.predict(tweets_transformed)

        p = np.array(self.model.decision_function(tweets_transformed))
        probability = np.exp(p)/np.sum(np.exp(p), axis=1, keepdims=True)
        probability_list = [max(prob) for prob in probability]

        self.predict_df['predicted'] = predicted_category
        self.predict_df['probability'] = probability_list

        top_categories = self.predict_df[self.predict_df['probability'] >= confidence_thresh]['predicted'].value_counts()[:3]       

        return self.predict_df, top_categories
