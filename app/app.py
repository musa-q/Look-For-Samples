from flask import Flask, render_template, request, g, make_response, session
from datetime import timedelta
from .recommender import recommenderManager
from .db import dbManager
from .sessionHandler import SessionHandler


app = Flask(__name__, static_url_path='/static')
app.secret_key = 'SECRET_KEY'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)

@app.before_request
def before_request():
    g.db = dbManager.connect()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        dbManager.disconnect()

@app.route("/")
@app.route('/home')
def index():
    return render_template("index.html")

@app.route('/view-all-tracks')
def view_all_tracks():
    all_tracks = dbManager.getAllTracks()
    return render_template("viewAllTracks.html", data=all_tracks)


@app.route('/music', methods=['GET', 'POST'])
def music():
    user_session = SessionHandler(session)
    currentSong = None
    recommendations = []

    if request.method == 'POST':
        if request.form['decide_song_button'].upper() == 'SKIP':
            try:
                for track in recommendations:
                    if track not in user_session.getUserHistory():
                        currentSong = track
                        user_session.addToUserHistory(currentSong)
                        response = make_response(render_template('music.html', data=currentSong))
                        response.headers['Referrer-Policy'] = 'no-referrer'
                        return response
            except:
                pass
            currentSong = recommenderManager.randomSong()
            user_session.addToUserHistory(currentSong)
            response = make_response(render_template('music.html', data=currentSong))
            response.headers['Referrer-Policy'] = 'no-referrer'
            return response

        else:
            try:
                recommenderManager.updateUserPreferences(currentSong[0], request.form['decide_song_button'].upper())
                recommendations = recommenderManager.recommendBasedOnPreferences(3)
            except TypeError:
                currentSong = recommenderManager.randomSong()
                user_session.addToUserHistory(currentSong)
                response = make_response(render_template('music.html', data=currentSong))
                response.headers['Referrer-Policy'] = 'no-referrer'
                return response

            if not recommendations:
                currentSong = recommenderManager.randomSong()
            else:
                currentSong = recommendations[0]

            user_session.addToUserHistory(currentSong)
            response = make_response(render_template('music.html', data=currentSong))
            response.headers['Referrer-Policy'] = 'no-referrer'
            return response

    else:
        current_song = recommenderManager.randomSong()
        user_session.addToUserHistory(current_song)

        recommendations = recommenderManager.recommendBasedOnPreferences(3)

        user_session.setCurrentSong(current_song)
        user_session.setRecommendations(recommendations)

        response = make_response(render_template('music.html', data=current_song))
        response.headers['Referrer-Policy'] = 'no-referrer'
        return response

if __name__ == '__main__':
    app.run()
