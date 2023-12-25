from flask import session
from datetime import timedelta

class SessionHandler:
    def __init__(self, session):
        self.session = session

    def get_user_id(self):
        return self.session.get('user_id', None)

    def add_to_user_history(self, song):
        user_history = self.session.get('user_history', [])
        user_history.append(song)
        self.session['user_history'] = user_history

    def set_user_history(self, history):
        session['history'] = history

    def get_user_preferences(self):
        return session.get('userPreferences', {})

    def set_user_preferences(self, userPreferences):
        session['userPreferences'] = userPreferences

    def is_session_expired(self):
        return 'permanent' in session

    def set_current_song(self, current_song):
        self.session['current_song'] = current_song

    def get_current_song(self):
        return self.session.get('current_song', None)

    def set_recommendations(self, recommendations):
        self.session['recommendations'] = recommendations

    def get_recommendations(self):
        return self.session.get('recommendations', [])

