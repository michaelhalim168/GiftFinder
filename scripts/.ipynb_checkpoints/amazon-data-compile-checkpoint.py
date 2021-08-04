import numpy as np
import pandas as pd
import gzip
import json

def parse(path):
    g = gzip.open(path, 'rb')
    count = 0
    for l in g:
        yield json.loads(l)
        count += 1
        if count == 2000000:
            break

def getDF(path):
    i = 0
    df = {}
    for d in parse(path):
        df[i] = d
        i += 1
        
    return pd.DataFrame.from_dict(df, orient='index')

def get_detailed_cat(desc):
    if len(desc) == 0:
        return np.nan
    else:
        return ', '.join(desc)

def get_features(desc):
    if len(desc) == 0:
        return 'No features'
    else:
        return ', '.join(desc)

def recommend(desc):
    if len(desc) == 0:
        return '0'
    else:
        return ', '.join(desc)

def convert_price(price):
    try:
        return float(price[1:])
    except:
        return float(0)

def get_reviews(path):

    df = getDF(path)

    df.drop(['reviewTime', 'unixReviewTime', 'style', 'image', 'reviewerName'],
                   axis=1, inplace=True)
    df.rename(columns={'overall': 'star_rating', 'asin': 'product_id', 
                               'reviewText': 'review_body', 'summary': 'review_headline',
                               'vote': 'upvotes', 'reviewerID': 'reviewer_id'}, inplace=True)

    columns = ['product_id', 'reviewer_id', 'verified', 'star_rating', 'upvotes', 
          'review_headline', 'review_body']
    df = df[columns]

    df['upvotes'].fillna(0, inplace=True)
    df.dropna(inplace=True)

    return df

def get_meta_data(path):

    df = getDF(path)
    
    df.drop(['tech1', 'tech2', 'similar_item', 'fit', 
            'details', 'imageURL', 'date', 'brand', 'rank'], axis=1, inplace=True)
    df.rename(columns={'main_cat': 'category', 'category': 'detailed_cat', 'asin': 'product_id',
                           'title': 'product_name', 'description': 'product_description'}, inplace=True)
    
    columns = ['product_id', 'product_name', 'product_description', 'category', 'detailed_cat',
          'feature', 'price', 'also_buy', 'also_view', 'imageURLHighRes']
    df = df[columns]

    df = df.replace('&amp;', '&', regex=True)

    df['product_description'] = df['product_description'].str[0]
    df['product_description'].fillna('No description.', inplace=True)

    df['detailed_cat'] = df['detailed_cat'].map(get_detailed_cat)
    df['detailed_cat'].fillna(df['category'], inplace=True)

    df['feature'] = df['feature'].map(get_features)

    df['also_buy'] = df['also_buy'].map(recommend)
    df['also_view'] = df['also_view'].map(recommend)    

    df['imageURLHighRes'] = df['imageURLHighRes'].str[0]  
    df['imageURLHighRes'].fillna('Missing link', inplace=True)

    df['price'].replace('', '$0', inplace=True)
    df['price'] = df['price'].map(convert_price).replace(float(0), float(-1))
    df.drop_duplicates(subset='product_id', keep='first', inplace=True)

    return df
    

def merged_reviews_meta(reviews, meta):
    df = pd.merge(meta, reviews, on='product_id', how='left')
    df.dropna(inplace=True)
    df = df[df['verified'] != False]
    review_summary = df.groupby('product_id').agg(num_reviews=('reviewer_id', 'size'), avg_rating=('star_rating', 'mean')).reset_index()  
    return pd.merge(df, review_summary, on='product_id', how='left')

def parse_backwards(path):
    g = gzip.open(path, 'rb')
    count = 0
    for l in reversed(list(g)):
        print(l)
        count += 1
        if count == 10:
            break