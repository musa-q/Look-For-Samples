from flask import session
from datetime import timedelta

class SessionHandler:
    def __init__(self, session):
        self.session = session

    def getUserId(self):
        return self.session.get('user_id', None)

    def addToUserHistory(self, song):
        userHistory = self.session.get('userHistory', [])
        userHistory.append(song[0])
        self.session['userHistory'] = userHistory

    def setUserHistory(self, history):
        session['history'] = history

    def getUserHistory(self):
        return self.session.get('userHistory', [])

    def getUserPreferences(self):
        return session.get('userPreferences', {})

    def setUserPreferences(self, userPreferences):
        session['userPreferences'] = userPreferences

    def isSessionExpired(self):
        return 'permanent' in session

    def setCurrentSong(self, current_song):
        self.session['current_song'] = current_song

    def getCurrentSong(self):
        return self.session.get('current_song', None)

    def setRecommendations(self, recommendations):
        self.session['recommendations'] = recommendations

    def getRecommendations(self):
        return self.session.get('recommendations', [])

