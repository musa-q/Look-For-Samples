from flask import Blueprint, render_template, request, g, make_response, session
from .recommender import recommenderManager
from .db import dbManager
from .sessionHandler import SessionHandler
import json

views_bp = Blueprint('views', __name__, static_url_path='/static')

@views_bp.before_request
def before_request():
    g.db = dbManager.connect()

@views_bp.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        dbManager.disconnect()

@views_bp.route("/")
@views_bp.route('/home')
def index():
    return render_template("index.html")

@views_bp.route('/view-all-tracks')
def view_all_tracks():
    all_tracks = dbManager.getAllTracks()
    return render_template("viewAllTracks.html", data=all_tracks)


@views_bp.route('/music', methods=['GET', 'POST'])
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

@views_bp.route('/report-track', methods=['POST'])
def report_track():
    reported_track = request.form.get('current_track')
    save_reported_track(reported_track)
    return "Reported"

def save_reported_track(reported_track):
    try:
        with open('reported_tracks.json', 'r') as json_file:
            reported_tracks = json.load(json_file)
    except FileNotFoundError:
        reported_tracks = []

    reported_tracks.append(reported_track)

    with open('reported_tracks.json', 'w') as json_file:
        json.dump(reported_tracks, json_file)