import pandas as pd
import sqlite3
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re


'''''
Make it that it gives random ones at first then looks at history and recommends
Rather than just looking at current song
'''''
class Recommender:
    def __init__(self):
        self.df = None
        self.df_encoded = None
        self.data = self.get_data()
        self.items = self.df['id'].tolist()
        self.similarity_matrix = cosine_similarity(self.data)

    def get_data(self):
        with sqlite3.connect("./music.db") as conn:
            self.df = pd.read_sql_query("SELECT * FROM MUSIC", conn)

            self.df_encoded = self.df.copy()

        self.df_encoded['artist_name'] = self.df_encoded['artist_name'].apply(lambda x: re.sub(r'\s*\(\d+\)$', '', x))

        one_hot = pd.get_dummies(self.df_encoded['artist_name'])
        self.df_encoded = self.df.join(one_hot)

        one_hot = pd.get_dummies(self.df_encoded['year_released'])
        self.df_encoded = self.df.join(one_hot)

        self.df_encoded= self.df_encoded.drop(columns=['artist_name', 'year_released'])

        self.df_encoded['styles'] = self.df_encoded['styles'].str.split(', ')
        styles_dummies = self.df_encoded['styles'].apply(lambda x: pd.Series([1]*len(x), index=x)).fillna(0, downcast='infer')
        self.df_encoded = pd.concat([self.df_encoded.drop('styles', axis=1), styles_dummies], axis=1)

        self.df_encoded['genre'] = self.df_encoded['genre'].str.split(', ')
        styles_dummies = self.df_encoded['genre'].apply(lambda x: pd.Series([1]*len(x), index=x)).fillna(0, downcast='infer')
        self.df_encoded = pd.concat([self.df_encoded.drop('genre', axis=1), styles_dummies], axis=1)

        self.df_encoded['country_released'] = self.df_encoded['country_released'].str.split('& ')
        styles_dummies = self.df_encoded['country_released'].apply(lambda x: pd.Series([1]*len(x), index=x)).fillna(0, downcast='infer')
        self.df_encoded = pd.concat([self.df_encoded.drop('country_released', axis=1), styles_dummies], axis=1)
        self.df_encoded = self.df_encoded.drop(columns=['', 'song_name', 'image_cover_link', 'youtube_link'])

        return self.df_encoded.drop('id', axis=1)

    def recommend_items(self, user_id, top_k):
        user_id += 1
        similarity_scores = self.similarity_matrix[user_id]
        sorted_indices = np.argsort(similarity_scores)[::-1]
        top_k_indices = sorted_indices[:top_k]

        return [self.items[i] for i in top_k_indices]

    def recommend_dissimilar_items(self, user_id, top_k):
        user_id += 1
        similarity_scores = self.similarity_matrix[user_id]
        sorted_indices = np.argsort(similarity_scores)
        top_k_indices = sorted_indices[:top_k]

        return [self.items[i] for i in top_k_indices]