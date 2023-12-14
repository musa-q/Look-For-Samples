import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from config import COLOR
from db import dbManager
import joblib

'''''
Make it that it gives random ones at first then looks at history and recommends
Rather than just looking at current song
'''''

class Recommender:
    def __init__(self):
        self.df = None
        self.similarityMatrix = None
        self.userPreferences = {}
        # self.matrixFilename = "similarityMatrix.pkl"

    def setup(self):
        df = pd.read_sql_query("SELECT * FROM tracks", dbManager.connection)
        print(f"{COLOR.GREEN}[Gathered data from database]{COLOR.ENDC}")
        self.df = df.copy()
        # try:
        #     # Try to load the similarity matrix from a file
        #     self.similarityMatrix = joblib.load(self.matrixFilename)
        #     print(f"{COLOR.GREEN}[Loaded similarity matrix from file]{COLOR.ENDC} {self.matrixFilename}")
        # except:
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

            # joblib.dump(self.similarityMatrix, self.matrixFilename)
            # print(f"{COLOR.GREEN}[Saved similarity matrix to file]{COLOR.ENDC} {self.matrixFilename}")


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
                        recommendedSongData = recommendedSongData.tolist()
                        recommendations.append(recommendedSongData)
                        if len(recommendations) >= topN:
                            break
                if len(recommendations) >= topN:
                    break

        print(f"{COLOR.GREEN}[Song recommendation created]{COLOR.ENDC}")
        return recommendations

    def randomSong(self, userId):
        try:
            likedSongs = self.userPreferences[userId]['likes']
            dislikedSongs = self.userPreferences[userId]['dislikes']
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

