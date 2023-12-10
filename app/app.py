from flask import Flask, render_template, request, g, send_file
from recommender import Recommender
from db import dbManager
import sqlite3
# from pytube import YouTube
import youtube_dl
import sys
import os


app = Flask(__name__)

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

# @app.route('/add', methods=['GET', 'POST'])
# def addmusic():
#     if request.method == 'POST':
#         song_name = request.form['song_name']
#         artist_name = request.form['artist_name']
#         genre = request.form['genre']
#         year_released = request.form['year_released']
#         country_released = request.form['country_released']
#         image_cover_link = request.form['image_cover_link']
#         youtube_link = request.form['youtube_link']
#         styles = request.form['styles']
#         return render_template("index.html")
#     else:
#         return render_template('add.html')



# @app.route('/empty_database', methods=['POST'])
# def empty_database():
#     with sqlite3.connect("music.db") as conn:
#         cursor = conn.cursor()
#         cursor.execute("DELETE FROM MUSIC")
#         conn.commit()

#     return "Database emptied successfully"

# def download_youtube_mp3(url):
#     ydl_opts = {
#         'format': 'bestaudio/best',
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'mp3',
#             'preferredquality': '192',
#         }],
#         'outtmpl': '%(title)s.%(ext)s',
#     }

#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         info_dict = ydl.extract_info(url, download=True)
#         mp3_filename = ydl.prepare_filename(info_dict)
#         return mp3_filename


# def download_youtube_mp3(url):
#     # Create a YouTube object
#     youtube = YouTube(url)

#     # Get the best audio stream
#     audio_stream = youtube.streams.filter(only_audio=True).first()

#     # Download the audio stream
#     audio_stream.download()

#     # Convert the video file to MP3
#     video_path = audio_stream.default_filename
#     mp3_path = video_path.replace(".mp4", ".mp3")

#     # Rename and move the MP3 file to the default downloads folder
#     default_output_folder = os.path.expanduser("~/Downloads")
#     new_path = os.path.join(default_output_folder, mp3_path)
#     os.rename(video_path, new_path)

#     return new_path

# @app.route('/download/<int:song_id>')
# def download_song(song_id):
#     with sqlite3.connect("music.db") as conn:
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM MUSIC WHERE ID = ?", (song_id,))
#         row = cursor.fetchone()

#         # Download the YouTube audio as MP3
#         youtube_url = row[7]
#         mp3_path = download_youtube_mp3(youtube_url)

#         # Move the MP3 file to the default downloads folder
#         default_output_folder = os.path.expanduser("~/Downloads")
#         new_path = os.path.join(default_output_folder, os.path.basename(mp3_path))
#         os.rename(mp3_path, new_path)

#         # Return the downloaded file to the user
#         return send_file(new_path, as_attachment=True)

# recommender = Recommender()
# current_song_id = None
# used_ids = []

# @app.route('/music', methods=['GET', 'POST'])
# def music():
#     global current_song_id
#     if request.method == 'POST':
#         # get like/dislike
#         # pass song to recommender
#         # check recommend song not played before
#         if request.form['decide_song_button'] == 'LIKE':
#             new_recommended = recommender.recommend_items(current_song_id, 10)
#             for new_id in new_recommended:
#                 if new_id not in used_ids:
#                     current_song_id = new_id
#                     break

#         elif request.form['decide_song_button'] == 'DISLIKE':
#             new_recommended = recommender.recommend_dissimilar_items(current_song_id, 10)
#             for new_id in new_recommended:
#                 if new_id not in used_ids:
#                     current_song_id = new_id
#                     break

#         else:
#             print("ERROR GETTING NEW SONG")

#         # pass song info to html
#         with sqlite3.connect("music.db") as conn:
#             cursor = conn.cursor()
#             cursor.execute("SELECT * FROM MUSIC WHERE ID = ?", (current_song_id,))
#             rows = cursor.fetchall()

#         return render_template("music.html", data=rows[0])

#     else:
#         with sqlite3.connect("music.db") as conn:
#             cursor = conn.cursor()
#             cursor.execute("SELECT * FROM MUSIC ORDER BY RANDOM() LIMIT 1")
#             random_row = cursor.fetchone()

#         current_song_id = random_row[0]
#         # print(f"current_song_id is {current_song_id}")
#         # print(random_row)
#         return render_template('music.html', data=random_row, current_song_id=current_song_id)

# @app.errorhandler(500)
# def handle_error(error):
#     # Perform any necessary cleanup tasks here
#     try:
#         connect.close()
#         cursor.close()
#     except:
#         pass

#     # Safely exit the application
#     sys.exit()


if __name__ == '__main__':
    app.run(debug=True)
