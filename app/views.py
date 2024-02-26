from flask import Blueprint, render_template, request, g, make_response, session, jsonify
from .recommender import recommenderManager
from .db import dbManager
from .sessionHandler import SessionHandler
import json
from datetime import datetime
import logging
import os

views_bp = Blueprint('views', __name__, static_url_path='/static')


current_dir = os.getcwd()
logs_dir = os.path.join(current_dir, 'logs')
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)
log_file_path = os.path.join(logs_dir, 'app.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(message)s')
logging.info('Starting server...')


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

# @views_bp.route('/view-all-tracks')
# def view_all_tracks():
#     all_tracks = dbManager.getAllTracks()
#     return render_template("viewAllTracks.html", data=all_tracks)


@views_bp.route('/music', methods=['GET', 'POST'])
def music():
    user_session = SessionHandler(session)
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
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
                recommendations = recommenderManager.recommendBasedOnPreferences(3, ip_address)
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

        recommendations = recommenderManager.recommendBasedOnPreferences(3, ip_address)

        user_session.setCurrentSong(current_song)
        user_session.setRecommendations(recommendations)

        response = make_response(render_template('music.html', data=current_song))
        response.headers['Referrer-Policy'] = 'no-referrer'
        return response

@views_bp.route('/report-track', methods=['POST'])
def report_track():
    reported_track = json.loads(request.data.decode('utf-8'))
    save_track_to_file(reported_track, 'reported_tracks.json')
    return "Reported"

@views_bp.route('/add-track', methods=['GET', 'POST'])
def add_track():
    if request.method == 'POST':
        track_data = json.loads(request.data.decode('utf-8'))
        if dbManager.checkExisting(track_data['songName'], track_data['artistName']):
            save_track_to_file(track_data, 'track_requests.json')
            return jsonify({'success': True, 'message': 'Track request sent successfully!'})
        else:
            return jsonify({'success': False, 'message': 'Track already exists. Please provide a unique track.'})
    return render_template('addTrack.html')

@views_bp.route('/add-feedback', methods=['POST'])
def add_feedback():
    feedback_info = json.loads(request.data.decode('utf-8'))
    feedback_info['time'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    try:
        save_track_to_file(feedback_info, 'feedback.json')
    except:
        return jsonify({'success': False, 'message': 'Error with sending'})
    return jsonify({'success': True, 'message': 'Sent feedback'})

def save_track_to_file(track_data, filename):
    try:
        with open(filename, 'r') as json_file:
            temp_req = json.load(json_file)
    except FileNotFoundError:
        temp_req = []

    temp_req.append(track_data)

    with open(filename, 'w') as json_file:
        json.dump(temp_req, json_file)