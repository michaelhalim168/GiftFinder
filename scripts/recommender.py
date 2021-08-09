from sklearn.metrics.pairwise import euclidean_distances
import numpy as np
import pandas as pd

def output_to_vector(model_output, matrix):
    df = pd.DataFrame(columns=matrix.columns)
    vector = list(np.zeros(16))
    for index in model_output:
        vector[index] = 1
    df.loc[0] = vector
    return df

def euclidean_rec(user_df, product_df, num_of_rec, labels):
    distances = euclidean_distances(product_df, user_df)
    distances = distances.reshape(-1)
    ordered_indices = distances.argsort()
    closest_indices = ordered_indices[:num_of_rec]
    item_list = product_df.iloc[closest_indices].index.to_list()
    recommended_products = labels.inverse_transform(item_list)
    return recommended_products

