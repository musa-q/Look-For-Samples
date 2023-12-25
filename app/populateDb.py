import sqlite3
import time
from .discogsAccess import discogsManager
from discogs_client.exceptions import HTTPError
import json
from .config import COLOR, loadingBar
from .track import Track
from .db import dbManager

def get_tracks(startPage=1, endPage=5):
    if startPage > endPage:
        print(f"{COLOR.FAIL}[Error]{COLOR.ENDC} End page is larger than start page")
    else:
        tracks = discogsManager.getTracks(startPage=startPage, endPage=endPage)
        return tracks


def populate(tracks, commit_interval=25):
    print(f"{COLOR.CYAN}Commit interval set to {commit_interval}{COLOR.ENDC}")
    for trackNum, musicTrack in enumerate(tracks):
        try:
            tempTrack = Track()
            tempTrack.extractData(musicTrack)
            if tempTrack.youtubeLink == None:
                continue

            dbManager.addRow(tempTrack)

            if (trackNum + 1) % commit_interval == 0:
                dbManager.connection.commit()
                print(f"{COLOR.GREEN}[Committed]{COLOR.ENDC} {commit_interval} tracks to the database")

        except HTTPError as e:
            if e.status_code == 429:
                print(f"{COLOR.FAIL}[Error]{COLOR.ENDC} Rate limit hit - timeout for {COLOR.CYAN}60{COLOR.ENDC} seconds")
                loadingBar(60)
            else:
                raise

    dbManager.connection.commit()
    print(f"{COLOR.GREEN}[Committed]{COLOR.ENDC} Remaining tracks to the database")


def populateTracks(startPage=1, endPage=5, commit_interval=25):
    tracks = get_tracks(startPage, endPage)
    populate(tracks, commit_interval)
