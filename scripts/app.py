#Import Standard Libraries
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
import base64

#Import API and Modelling Functions
from keys import *
from data_collection import get_user_tweets
from data_cleaning import spacy_lemmatize, deEmojify, tweet_preprocess
from classifier import user_tweet_df, TweetCategory
from recommender import output_to_vector, euclidean_rec

#Path of Tweets
MODEL_PATH = '/Users/michaelhalim/Desktop/Lighthouse Labs/gift-recommender/final-outputs/models/linear_svc_final_model.sav'
VECTORIZER_PATH = '/Users/michaelhalim/Desktop/Lighthouse Labs/gift-recommender/final-outputs/models/tfidf_vectorizer_final.sav'
REFERENCE_PATH = '/Users/michaelhalim/Desktop/Lighthouse Labs/gift-recommender/final-outputs/models/reference-dict.pickle'
PRODUCT_PATH = '/Users/michaelhalim/Desktop/Lighthouse Labs/gift-recommender/final-outputs/datasets/amazon_gift_items_clean.csv'

#Define Variables for Data Cleaning
stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(['im', "oh", "i'm", "lol", "gonna", 'ill'])
punctuations = string.punctuation
nlp = spacy.load('en_core_web_sm')

#Import Models
ovr_svc = pickle.load(open(MODEL_PATH, 'rb'))
tfidf_model = pickle.load(open(VECTORIZER_PATH, 'rb'))
ref = pickle.load(open(REFERENCE_PATH, 'rb'))

#Import Product Dataframe
le = LabelEncoder()
product_df = pd.read_csv(PRODUCT_PATH)
product_df.drop('Unnamed: 0', axis=1, inplace=True)
product_df['product_label'] = le.fit_transform(product_df['product_name'])
product_matrix = product_df.drop(['product_name', 'rating', 'price', 'product_desc', 'categories', 
                                    'main_category', 'image_link', 'link'], axis=1).set_index('product_label')
#Import Twitter API Keys
twitter = TwitterKeys()
consumer_key = twitter.consumer_key
consumer_secret = twitter.consumer_secret
access_token = twitter.access_token
access_secret = twitter.access_secret


def draw_header():
    st.set_page_config(layout="wide")
    LOGO_IMAGE = 'app-image/logo-final.png'
    st.markdown("""
        <style>
        .container {
            justify-content: center !important;
            width:800px !important;
            margin: auto !important;
        }

        .logo-text {
            font-weight:700 !important;
            font-size:60px !important;
            color:#571089 !important;
            padding-top: 55px !important;
            font-family: inter !important;
        }

        .sub-text {
            font-size: 18px !important;
            color: black !important;
            font-family: montserrat !important;
            font-style: italic !important;
        }
        
        .logo-img {
            float: left !important;
            width: 250px !important;
            height: 270px !important;
        }
        </style
        """, unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="container">
            <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}"">
            <p class="logo-text">GiftFinder</p>
            <p class="sub-text">Harness the power of social media to find the perfect gift</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        f"""
        <hr>
        """, unsafe_allow_html=True
    )

def error_message(warning):
    st.markdown("""
        <style>
        .warning-font {
            font-size:20px !important;
            font-family: avenir !important;
            text-align: center !important;
        }
        </style>
        """, unsafe_allow_html=True)
    if warning == 'user_not_found':
        st.markdown('<p class="warning-font">Sorry, Twitter account cannot be accessed. Is this user public?</p>', unsafe_allow_html=True)
    elif warning == 'tweet_not_found':
        st.markdown('<p class="warning-font">Sorry, there are no Tweets in this account. Is this user active?</p>', unsafe_allow_html=True)
    elif warning == 'no_categories':
        st.markdown('<p class="warning-font">Sorry, we\'re not able to identify any gift categories.</p>', unsafe_allow_html=True)

def show_topics(twitter_handle, outcome):
    st.markdown("""
        <style>
        .recommend-font {
            font-size:30px !important;
            font-family: avenir !important;
            text-align: center !important;
            font-weight: bold !important;
        }

        .text-font {
            font-size:20px !important;
            font-family: avenir !important;
            text-align: center !important;
        }
        </style>
        """, unsafe_allow_html=True)
    recommended_text = "Gift Categories for {}:".format(twitter_handle)
    recommended_html = '<p class="recommend-font">' + recommended_text + '</p>'
    recommended_products = "{}, {}, {}".format(outcome[0], outcome[1], outcome[2])
    recommended_products_html = '<p class="text-font">' + recommended_products + '</p>'
    st.markdown('<hr>', unsafe_allow_html=True)
    st.markdown(recommended_html, unsafe_allow_html=True)
    st.markdown(recommended_products_html, unsafe_allow_html=True)

def show_products(twitter_handle, products, product_df):
    st.markdown("""
        <style>
        .heading-font {
            font-size: 30px !important;
            font-family: avenir !important;
            text-align: center !important;
            font-weight: bold !important;
        }

        .title-font {
            font-size: 20px !important;
            font-family: avenir !important;
            text-align: center !important;
        }
        </style>
    """, unsafe_allow_html=True)

    recommend_text = "{} may like...".format(twitter_handle)
    recommend_html = '<p class="heading-font">' + recommend_text + '</p>'
    st.markdown(recommend_html, unsafe_allow_html=True)

    st.markdown("""
        <style>
            .row {
                display: flex !important;
                justify-content: center !important;
            }
            .column{
                width: 33.33% !important;
            }
            .image-class {
                width: 200px !important;
                height: 200px !important;
                display: block !important;
                margin-left: auto !important;
                margin-right: auto !important;
            }
            a, a:hover, a:focus, a:active {
            text-decoration: none;
            color: inherit;
            }
        </style>
    """, unsafe_allow_html=True)

    item1_text = "{}".format(products[0])
    item1_link = product_df[product_df['product_name'] == products[0]]['link'].iloc[0]
    item1_html = '<p class="title-font">' + '<a href=' + item1_link + '>' + item1_text + '</a></p>'
    image1_link = product_df[product_df['product_name'] == products[0]]['image_link'].iloc[0]

    item2_text = "{}".format(products[1])
    item2_link = product_df[product_df['product_name'] == products[1]]['link'].iloc[0]
    item2_html = '<p class="title-font">' + '<a href=' + item2_link + '>' + item2_text + '</a></p>'
    image2_link = product_df[product_df['product_name'] == products[1]]['image_link'].iloc[0]

    item3_text = "{}".format(products[2])
    item3_link = product_df[product_df['product_name'] == products[2]]['link'].iloc[0]
    item3_html = '<p class="title-font">' + '<a href=' + item3_link + '>' + item3_text + '</a></p>'
    image3_link = product_df[product_df['product_name'] == products[2]]['image_link'].iloc[0]

    item4_text = "{}".format(products[3])
    item4_link = product_df[product_df['product_name'] == products[3]]['link'].iloc[0]
    item4_html = '<p class="title-font">' + '<a href=' + item4_link + '>' + item4_text + '</a></p>'
    image4_link = product_df[product_df['product_name'] == products[3]]['image_link'].iloc[0]

    item5_text = "{}".format(products[4])
    item5_link = product_df[product_df['product_name'] == products[4]]['link'].iloc[0]
    item5_html = '<p class="title-font">' + '<a href=' + item5_link + '>' + item5_text + '</a></p>'
    image5_link = product_df[product_df['product_name'] == products[4]]['image_link'].iloc[0]

    item6_text = "{}".format(products[5])
    item6_link = product_df[product_df['product_name'] == products[5]]['link'].iloc[0]
    item6_html = '<p class="title-font">' + '<a href=' + item6_link + '>' + item6_text + '</a></p>'
    image6_link = product_df[product_df['product_name'] == products[5]]['image_link'].iloc[0]

    div1_html = """
    <div class="row"> 
        <div class="column">
    """ + item1_html +  '''<img class="image-class" src="''' + image1_link + '''"</img>
    </div>''' + """<div class="column">
    """ + item2_html +  '''<img class="image-class" src="''' + image2_link + '''"</img></div>''' + """<div class="column">
    """ + item3_html +  '''<img class="image-class" src="''' + image3_link + '''"</img></div></div>''' 
    
    div2_html = """
    <div class="row"> 
        <div class="column">
    """ + item4_html +  '''<img class="image-class" src="''' + image4_link + '''"</img>
    </div>''' + """<div class="column">
    """ + item5_html +  '''<img class="image-class" src="''' + image5_link + '''"</img></div>''' + """<div class="column">
    """ + item6_html +  '''<img class="image-class" src="''' + image6_link + '''"</img></div></div>''' 

    st.markdown(div1_html, unsafe_allow_html=True)
    st.markdown(div2_html, unsafe_allow_html=True)

def main():

    draw_header()

    buff, col, buff2 = st.beta_columns([1,2,1])
    label_format = st.markdown("""
        <style>
        .font-prop {
            font-family: 'avenir' !important;
            font-size: 30px !important;
            font-weight: bold;
            text-align: center;
        }
        }
        </style>""", unsafe_allow_html=True)
    col.markdown('<p class="font-prop">Who are you buying a gift for?</p>', unsafe_allow_html=True)
    twitter_handle = col.text_input("Enter Twitter Handle/Username!")
    button_format = st.markdown("""
        <style>
        div.stButton > button:first-child {
            font-family: avenir !important;
            font-size: 18px !important;
            text-align: center !important;
            justify-content: center !important;
        }
        </style>""", unsafe_allow_html=True)
    enter = col.button('Enter')

    if enter:
        try:
            tweets = get_user_tweets(twitter_handle, consumer_key, consumer_secret, access_token, access_secret)
        except:
            error_message('user_not_found')
        else:
            try:
                tweet_df = user_tweet_df(tweets)
            except:
                error_message('tweet_not_found')
            else:
                key = {v: k for k, v in ref.items()}
                user_tweet = TweetCategory(ovr_svc, tfidf_model, tweet_df, key)
                user_tweet.process_user_tweets()
                top_topics = user_tweet.predict_topics(0, 0.2)

                try:
                    outcome = top_topics.reset_index()['index'].to_list()
                    show_topics(twitter_handle, outcome)
                except:
                    error_message('no_categories')
                else:
                    topic_labels = [ref[i] for i in outcome]
                    user_df = output_to_vector(topic_labels, product_matrix)
                    rec_prod = euclidean_rec(user_df, product_matrix, 6, le)
                    show_products(twitter_handle, rec_prod, product_df)

main()