from flask import Flask, render_template, request, g, send_file, make_response
from recommender import recommenderManager
from db import dbManager


app = Flask(__name__)
userId = "user1"

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
    global currentSong
    if request.method == 'POST':
        recommenderManager.updateUserPreferences(userId, currentSong[0], request.form['decide_song_button'].upper())
        recommendations = recommenderManager.recommendBasedOnPreferences(userId, 3)
        currentSong = recommendations[0]
        response = make_response(render_template('music.html', data=currentSong))
        response.headers['Referrer-Policy'] = 'no-referrer'
        return response

    else:
        currentSong = dbManager.getRandomSong()
        response = make_response(render_template('music.html', data=currentSong))
        response.headers['Referrer-Policy'] = 'no-referrer'
        return response

if __name__ == '__main__':
    currentSong = None
    app.run(debug=True)
