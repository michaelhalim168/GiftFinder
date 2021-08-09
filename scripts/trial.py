import numpy as np
import pandas as pd
import streamlit as st
import tweepy
import pickle
import string
import re
import nltk
import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.preprocessing import LabelEncoder

from keys import *
from data_collection import get_user_tweets
from data_cleaning import spacy_lemmatize, deEmojify, tweet_preprocess
from classifier import user_tweet_df, TweetCategory
from recommender import output_to_vector, euclidean_rec

stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(['im', "oh", "i'm", "lol", "gonna", 'ill'])
punctuations = string.punctuation
nlp = spacy.load('en_core_web_sm')

ovr_svc = pickle.load(open('linear_svc_baseline2.sav', 'rb'))
tfidf_model = pickle.load(open('tfidf_vectorizer2.sav', 'rb'))
ref = pickle.load(open('reference-dict.pickle', 'rb'))

le = LabelEncoder()

product_df = pd.read_csv('amazon_gift_items_clean.csv')
product_df.drop('Unnamed: 0', axis=1, inplace=True)
product_df['product_label'] = le.fit_transform(product_df['product_name'])
product_matrix = product_df.drop(['product_name', 'rating', 'price', 'product_desc', 'categories', 
                                    'main_category', 'image_link', 'link'], axis=1).set_index('product_label')
print(product_df[product_df['product_name'] == 'Scotch and Bourbon Glasses']['image_link'].iloc[0])


    '''
             display: flex !important;
                justify-content: center !important;

       /*.column{
                display: block !important;
                margin-left: auto !important;
                margin-right: auto !important;
                width: 33.33%;
            }*/
    col1, col2, col3 = st.beta_columns(3)

    with col1:
        item1_text = "{}".format(products[0])
        item1_html = '<p class="title-font">' + item1_text + '</p>'
        image1_link = product_df[product_df['product_name'] == products[0]]['image_link'].iloc[0]
        st.markdown(item1_html, unsafe_allow_html=True)
        st.image(image1_link, width=100)
    
    with col2:
        item2_text = "{}".format(products[1])
        item2_html = '<p class="title-font">' + item2_text + '</p>'
        image2_link = product_df[product_df['product_name'] == products[1]]['image_link'].iloc[0]
        st.markdown(item2_html, unsafe_allow_html=True)
        st.image(image2_link, width=100)
    
    with col3:
        item3_text = "{}".format(products[2])
        item3_html = '<p class="title-font">' + item3_text + '</p>'
        image3_link = product_df[product_df['product_name'] == products[2]]['image_link'].iloc[0]
        st.markdown(item3_html, unsafe_allow_html=True)
        st.image(image3_link, width=100)
    
    with col1:
        item4_text = "{}".format(products[3])
        item4_html = '<p class="title-font">' + item4_text + '</p>'
        image4_link = product_df[product_df['product_name'] == products[3]]['image_link'].iloc[0]
        st.markdown(item4_html, unsafe_allow_html=True)
        st.image(image4_link, use_column_width='always')

    with col2:
        item5_text = "{}".format(products[4])
        item5_html = '<p class="title-font">' + item5_text + '</p>'
        image5_link = product_df[product_df['product_name'] == products[4]]['image_link'].iloc[0]
        st.markdown(item5_html, unsafe_allow_html=True)
        st.image(image5_link, use_column_width='always')

    with col3:
        item6_text = "{}".format(products[5])
        item6_html = '<p class="title-font">' + item6_text + '</p>'
        image6_link = product_df[product_df['product_name'] == products[5]]['image_link'].iloc[0]
        st.markdown(item6_html, unsafe_allow_html=True)
        st.image(image6_link, use_column_width='always')    
    '''