import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from flask import session
import numpy as np
from .config import COLOR
from .db import dbManager
import logging
import os

current_dir = os.getcwd()
logs_dir = os.path.join(current_dir, 'logs')
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)
log_file_path = os.path.join(logs_dir, 'users.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(message)s')
logging.info('Waiting for users...')


class Recommender:
    def __init__(self):
        self.df = None
        self.similarityMatrix = None

    def setup(self):
        df = pd.read_sql_query("SELECT * FROM tracks", dbManager.connection)
        print(f"{COLOR.GREEN}[Gathered data from database]{COLOR.ENDC}")
        self.df = df.copy()
        dfEncoded = df.copy()
        labelEncoder = LabelEncoder()
        dfEncoded['artist'] = labelEncoder.fit_transform(dfEncoded['artist'])
        dfEncoded['genre'] = labelEncoder.fit_transform(dfEncoded['genre'])
        dfEncoded['styles'] = labelEncoder.fit_transform(dfEncoded['styles'])
        dfEncoded['country'] = labelEncoder.fit_transform(dfEncoded['country'])

        # Scale Year
        scaler = StandardScaler()
        dfEncoded['yearScaled'] = scaler.fit_transform(dfEncoded[['year']])

        # One-Hot Encoding
        onehotEncoder = OneHotEncoder()
        encodedFeatures = onehotEncoder.fit_transform(dfEncoded[['genre', 'styles', 'country']]).toarray()

        # Combine Scaled Year with Encoded Features
        finalFeatures = np.hstack((encodedFeatures, dfEncoded[['yearScaled']].values))

        # Calculate cosine similarity with the updated features
        self.similarityMatrix = cosine_similarity(finalFeatures)

    def updateUserPreferences(self, songId, likeDislike):
        userPreferences = session.get('userPreferences', {})

        if 'likes' not in userPreferences:
            userPreferences['likes'] = []
        if 'dislikes' not in userPreferences:
            userPreferences['dislikes'] = []

        if likeDislike == 'LIKE':
            userPreferences['likes'].append(songId)
        elif likeDislike == 'DISLIKE':
            userPreferences['dislikes'].append(songId)

        session['userPreferences'] = userPreferences

    def recommendBasedOnPreferences(self, topN, ip_address):
        user_preferences = session.get('userPreferences', {})

        if 'likes' not in user_preferences:
            print(f"{COLOR.FAIL}[Error]{COLOR.ENDC} No user preferences found")
            logging.info(f'User joined from {ip_address}')
            return

        likedSongs = self.session.get('userPreferences', {}).get('likes', [])
        dislikedSongs = self.session.get('userPreferences', {}).get('dislikes', [])

        recommendations = []
        for songId in likedSongs:
            if songId in self.df['id'].values:
                songIndex = self.df[self.df['id'] == songId].index[0]
                similarSongs = sorted(list(enumerate(self.similarityMatrix[songIndex])), key=lambda x: x[1], reverse=True)[1:topN+1]
                for i, score in similarSongs:
                    recommendedSongId = self.df.iloc[i]['id']
                    if recommendedSongId not in likedSongs and recommendedSongId not in dislikedSongs:
                        recommendedSongData = self.df.iloc[i].to_dict()
                        recommendedSongData = {k: int(v) if isinstance(v, np.int64) else v for k, v in recommendedSongData.items()}
                        recommendations.append(recommendedSongData)
                        if len(recommendations) >= topN:
                            break
                if len(recommendations) >= topN:
                    break

        print(f"{COLOR.GREEN}[Song recommendation created]{COLOR.ENDC}")
        return recommendations

    def randomSong(self):
        try:
            likedSongs = session.get('userPreferences', {}).get('likes', [])
            dislikedSongs = session.get('userPreferences', {}).get('dislikes', [])
        except KeyError:
            likedSongs = {}
            dislikedSongs = {}

        while True:
            song = dbManager.getRandomSong()
            recommendedSongId = song[0]
            if recommendedSongId not in likedSongs and recommendedSongId not in dislikedSongs:
                return song

recommenderManager = Recommender()
recommenderManager.setup()

