import sqlite3
from .config import COLOR
from .track import Track

class db:
    def __init__(self):
        self.dbName = "tracks.db"
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = sqlite3.connect(self.dbName)
        self.cursor = self.connection.cursor()
        print(f"{ COLOR.GREEN}[Connected to database]{ COLOR.ENDC} {self.dbName}")

    def disconnect(self):
        try:
            self.cursor.close()
            self.connection.close()
            print(f"{ COLOR.GREEN}[Successfully disconnected from database]{ COLOR.ENDC} {self.dbName}")
        except:
            print(f"{ COLOR.FAIL}[Error in disconnecting from database]{ COLOR.ENDC} {self.dbName}")

    def create(self):
        try:
            self.cursor.execute("CREATE TABLE tracks \
                       (id NUMBER, song TEXT, artist TEXT, genre TEXT, year NUMBER, styles TEXT, country TEXT, albumCover TEXT, youtubeLink TEXT)")
            print(f"{ COLOR.BLUE}[Created database]{ COLOR.ENDC}")
        except sqlite3.OperationalError:
            print(f"{ COLOR.WARNING}[Skipping]{ COLOR.ENDC} Database exists already")
        except Exception as e:
            print(f"{ COLOR.FAIL}[Error]{ COLOR.ENDC} Creating database\n{e}")

    def reset(self):
        try:
            self.cursor.execute("DROP TABLE IF EXISTS tracks")
            print(f"{COLOR.BLUE}[Database table dropped]{COLOR.ENDC}")
            self.create()
        except Exception as e:
            print(f"{COLOR.FAIL}[Error]{COLOR.ENDC} Restarting database\n{e}")

    def addRow(self, trackObj, commit=False):
        rowData = trackObj.getData()
        if self.checkExisting(rowData['songName'], rowData['artist']):
            try:
                self.cursor.execute("INSERT INTO tracks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                    (rowData['id'], rowData['songName'], rowData['artist'], rowData['genre'], rowData['year'], rowData['styles'], rowData['country'], rowData['albumCover'], rowData['youtubeLink']))
                if commit:
                    self.connection.commit
                # print(f"{ COLOR.GREEN}[Row]{ COLOR.ENDC} inserted")
            except Exception as e:
                print(f"{ COLOR.FAIL}[Error]{ COLOR.ENDC} Inserting row\n{e}")
        else:
            print(f"{ COLOR.WARNING}[Error]{ COLOR.ENDC} Track already exists in database")

    def checkExisting(self, songName, artistName):
        try:
            query = "SELECT COUNT(*) FROM tracks WHERE song = ? AND artist = ?"
            params = (songName, artistName)

            self.cursor.execute(query, params)
            result = self.cursor.fetchone()

            if result and result[0] == 0: # No matching records
                return True
            else:
                return False

        except Exception as e:
            print(f"{ COLOR.FAIL}[Error]{ COLOR.ENDC} Checking existing record\n{e}")
            return False

    def output(self):
        self.countRows()
        print(f"{ COLOR.HEADER}[OUTPUT]{ COLOR.ENDC}")
        rows = self.getAllTracks()
        for idx, row in enumerate(rows):
            print(f"{COLOR.CYAN}[Row {idx + 1}]{COLOR.ENDC} {row}")

    def getAllTracks(self):
        rows = self.cursor.execute("SELECT * FROM tracks").fetchall()
        return rows

    def countRows(self):
        try:
            self.cursor.execute("SELECT COUNT(*) FROM tracks")
            count = self.cursor.fetchone()[0]
            print(f"{COLOR.CYAN}[Total Rows: {count}]{COLOR.ENDC}")
        except Exception as e:
            print(f"{COLOR.FAIL}[Error]{COLOR.ENDC} Counting rows\n{e}")

    def getRandomSong(self):
        return self.cursor.execute("SELECT * FROM tracks ORDER BY RANDOM() LIMIT 1").fetchone()


dbManager = db()
dbManager.connect()