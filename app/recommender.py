import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import sqlite3
import numpy as np
from config import COLOR
from db import dbManager

'''''
Make it that it gives random ones at first then looks at history and recommends
Rather than just looking at current song
'''''

class Recommender:
    def __init__(self):
        self.df = None
        self.dfEncoded = None
        self.similarity_matrix = None
        self.userPreferences = {}

    def setup(self):
        df = pd.read_sql_query("SELECT * FROM tracks", dbManager.connection)
        print(f"{COLOR.GREEN}[Gathered data from database]{COLOR.ENDC}")
        self.df = df.copy()
        self.dfEncoded = df.copy()
        label_encoder = LabelEncoder()
        self.dfEncoded['artist'] = label_encoder.fit_transform(self.dfEncoded['artist'])
        self.dfEncoded['genre'] = label_encoder.fit_transform(self.dfEncoded['genre'])
        self.dfEncoded['styles'] = label_encoder.fit_transform(self.dfEncoded['styles'])
        self.dfEncoded['country'] = label_encoder.fit_transform(self.dfEncoded['country'])

        # Scale Year
        scaler = StandardScaler()
        self.dfEncoded['year_scaled'] = scaler.fit_transform(self.dfEncoded[['year']])

        # One-Hot Encoding
        onehot_encoder = OneHotEncoder()
        encoded_features = onehot_encoder.fit_transform(self.dfEncoded[['genre', 'styles', 'country']]).toarray()

        # Combine Scaled Year with Encoded Features
        final_features = np.hstack((encoded_features, self.dfEncoded[['year_scaled']].values))

        # Calculate cosine similarity with the updated features
        self.similarity_matrix = cosine_similarity(final_features)

    def update_user_preferences(self, user_id, song_name, like_dislike):
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {'likes': [], 'dislikes': []}

        if like_dislike == 'like':
            self.user_preferences[user_id]['likes'].append(song_name)
        elif like_dislike == 'dislike':
            self.user_preferences[user_id]['dislikes'].append(song_name)

    def recommend_based_on_preferences(self, user_id, top_n):
        if user_id not in self.user_preferences:
            print(f"{COLOR.FAIL}[Error]{COLOR.ENDC} No user preferences found")
            return

        liked_songs = self.user_preferences[user_id]['likes']
        disliked_songs = self.user_preferences[user_id]['dislikes']

        recommendations = []
        for song in liked_songs:
            if song in self.df['song'].values:
                song_index = self.df[self.df['song'] == song].index[0]
                similar_songs = sorted(list(enumerate(self.similarity_matrix[song_index])), key=lambda x: x[1], reverse=True)[1:top_n+1]
                for i, score in similar_songs:
                    recommended_song = self.df.iloc[i]['song']
                    if recommended_song not in liked_songs and recommended_song not in disliked_songs:
                        recommendations.append(recommended_song)
                        if len(recommendations) >= top_n:
                            break
                if len(recommendations) >= top_n:
                    break

        print(f"{COLOR.GREEN}Recommendations for user {user_id}: {recommendations}{COLOR.ENDC}")


recommenderManager = Recommender()
recommenderManager.setup()

