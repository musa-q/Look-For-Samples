import sqlite3

class db:
    def __init__(self):
        self.connection = sqlite3.connect("tracks.db")
        self.cursor = self.connection.cursor()

    def createDb(self):
        try:
            self.cursor.execute("CREATE TABLE tracks \
                       (song TEXT, artist TEXT, genre TEXT, year NUMBER, country TEXT, albumCover TEXT)")
            print("[Created database]")
        except sqlite3.OperationalError:
            print("[Skipping] Database exists already")
        except Exception as e:
            print(f"[Error] Creating database\n{e}")


    def addRow(self, rowJson):
        try:
            self.cursor.execute("INSERT INTO tracks VALUES (?, ?, ?, ?, ?, ?)",
                                (rowJson['song'], rowJson['artist'], rowJson['genre'], rowJson['year'], rowJson['country'], rowJson['albumCover']))
            self.connection.commit()
            print("[Row inserted]")
        except Exception as e:
            print(f"[Error] Inserting row\n{e}")

    def printDb(self):
        print("[OUTPUT]")
        rows = self.cursor.execute("SELECT * FROM tracks").fetchall()
        for row in rows:
            print(row)

dbManager = db()