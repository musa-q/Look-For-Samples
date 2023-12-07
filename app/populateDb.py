import sqlite3
import time
from discogsAccess import DiscogsAccess
import json
from config import COLOR
from track import Track
from db import dbManager

def get_tracks(startPage=1, endPage=5):
    discogsManager = DiscogsAccess()
    tracks = discogsManager.getTracks(startPage=startPage, endPage=endPage)
    return tracks


def populate(tracks, commit_interval=25):
    print(f"{COLOR.CYAN}Commit interval set to {commit_interval}{COLOR.ENDC}")
    for trackNum, musicTrack in enumerate(tracks):
        tempTrack = Track()
        tempTrack.extractData(musicTrack)
        dbManager.addRow(tempTrack)

        if (trackNum + 1) % commit_interval == 0:
            dbManager.connection.commit()
            print(f"{COLOR.GREEN}[Committed]{COLOR.ENDC} {commit_interval} tracks to the database")

    dbManager.connection.commit()
    print(f"{COLOR.GREEN}[Committed]{COLOR.ENDC} remaining tracks to the database")


def populateTracks(startPage=1, endPage=5, commit_interval=25):
    tracks = get_tracks(startPage, endPage)
    populate(tracks, commit_interval)