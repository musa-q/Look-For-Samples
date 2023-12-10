import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
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
        self.similarityMatrix = None
        self.userPreferences = {}

    def setup(self):
        df = pd.read_sql_query("SELECT * FROM tracks", dbManager.connection)
        print(f"{COLOR.GREEN}[Gathered data from database]{COLOR.ENDC}")
        self.df = df.copy()
        self.dfEncoded = df.copy()
        labelEncoder = LabelEncoder()
        self.dfEncoded['artist'] = labelEncoder.fit_transform(self.dfEncoded['artist'])
        self.dfEncoded['genre'] = labelEncoder.fit_transform(self.dfEncoded['genre'])
        self.dfEncoded['styles'] = labelEncoder.fit_transform(self.dfEncoded['styles'])
        self.dfEncoded['country'] = labelEncoder.fit_transform(self.dfEncoded['country'])

        # Scale Year
        scaler = StandardScaler()
        self.dfEncoded['yearScaled'] = scaler.fit_transform(self.dfEncoded[['year']])

        # One-Hot Encoding
        onehotEncoder = OneHotEncoder()
        encodedFeatures = onehotEncoder.fit_transform(self.dfEncoded[['genre', 'styles', 'country']]).toarray()

        # Combine Scaled Year with Encoded Features
        finalFeatures = np.hstack((encodedFeatures, self.dfEncoded[['yearScaled']].values))

        # Calculate cosine similarity with the updated features
        self.similarityMatrix = cosine_similarity(finalFeatures)

    def updateUserPreferences(self, userId, songId, likeDislike):
        if userId not in self.userPreferences:
            self.userPreferences[userId] = {'likes': [], 'dislikes': []}

        if likeDislike == 'LIKE':
            self.userPreferences[userId]['likes'].append(songId)
        elif likeDislike == 'DISLIKE':
            self.userPreferences[userId]['dislikes'].append(songId)

    def recommendBasedOnPreferences(self, userId, topN):
        if userId not in self.userPreferences:
            print(f"{COLOR.FAIL}[Error]{COLOR.ENDC} No user preferences found")
            return

        likedSongs = self.userPreferences[userId]['likes']
        dislikedSongs = self.userPreferences[userId]['dislikes']

        recommendations = []
        for songId in likedSongs:
            if songId in self.df['id'].values:
                songIndex = self.df[self.df['id'] == songId].index[0]
                similarSongs = sorted(list(enumerate(self.similarityMatrix[songIndex])), key=lambda x: x[1], reverse=True)[1:topN+1]
                for i, score in similarSongs:
                    recommendedSongId = self.df.iloc[i]['id']
                    if recommendedSongId not in likedSongs and recommendedSongId not in dislikedSongs:
                        recommendedSongData = self.df.iloc[i]
                        recommendations.append(recommendedSongData)
                        if len(recommendations) >= topN:
                            break
                if len(recommendations) >= topN:
                    break

        print(f"{COLOR.GREEN}[Song recommendation created]{COLOR.ENDC}")
        return recommendations


recommenderManager = Recommender()
recommenderManager.setup()

