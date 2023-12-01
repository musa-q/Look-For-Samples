import sqlite3
from discogsAccess import DiscogsAccess

# GET DATA FROM discogsAccess
# EXTRACT DATA + VALIDATE
# INSERT DATA INTO db

# print("ALL DATA RETRIEVED\n")

# cursor = conn.cursor()
# TRACK_COUNT = 1

# for track in tracks:
#     time.sleep(1.5)
#     styles = track.data.get("style", [])
#     styles = ", ".join(styles)
#     year_released = track.year if track.year != 0 else 2000
#     country_released = track.country

#     try:
#         artist_name = track.artists[0].name
#         song_name = track.title
#         genre = track.data.get("genre", [])
#         genre = ", ".join(genre)
#         image_cover_link = track.data.get("cover_image", "")
#         youtube_link = track.videos[0].data.get("uri", "")
#         cursor.execute(
#             "SELECT song_name FROM MUSIC WHERE song_name = ?", (song_name,))
#         existing_song = cursor.fetchone()

#         if existing_song:
#             print(
#                 f"SKIPPED: Song '{song_name}' already exists in the database.")
#             continue

#         print(f"Track number: {TRACK_COUNT}")
#         TRACK_COUNT += 1

#     except IndexError:
#         print(f"SKIPPED: {track}")
#         continue

#     cursor.execute("INSERT INTO MUSIC \
#                     (song_name, artist_name, genre, year_released, country_released, image_cover_link, youtube_link, styles) \
#                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
#                     (song_name, artist_name, genre, year_released, country_released, image_cover_link, youtube_link, styles))

#     if TRACK_COUNT % 50 == 0:
#         conn.commit()
#         print("-------------------------\n50 TRACKS ADDED TO THE DATABASE\n-------------------------")

# conn.commit()
