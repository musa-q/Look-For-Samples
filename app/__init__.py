from .db import dbManager
import argparse
from .populateDb import populateTracks

def setup():
    dbManager.create()

def reset():
    dbManager.reset()

def outputDB():
    dbManager.output()

def countDB():
    dbManager.countRows()

def populateDB(startPage=1, endPage=5, commit_interval=25):
    populateTracks(startPage, endPage, commit_interval)

def disconnectDB():
    dbManager.disconnect()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--setup", action="store_true", help="Setup the database")
    parser.add_argument("-r", "--reset", action="store_true", help="Resets the database")
    parser.add_argument("-o", "--output", action="store_true", help="Prints the values from the database")
    parser.add_argument("-p", "--populate", action="store_true", help="Populate the database with tracks")
    parser.add_argument("-c", "--commitInterval", type=int, default=25, help="Specify commit interval for populate")
    parser.add_argument("-t", "--count", action="store_true", help="Count the number of rows in the database")
    parser.add_argument("-d", "--disconnect", action="store_true", help="Disconnect from the database")
    parser.add_argument("-sp", "--startPage", type=int, default=1, help="Specify the start page for populating the database")
    parser.add_argument("-ep", "--endPage", type=int, default=5, help="Specify the end page for populating the database")


    args = parser.parse_args()

    if args.setup:
        setup()
    if args.reset:
        reset()
    if args.output:
        outputDB()
    if args.count:
        countDB()
    if args.disconnect:
        disconnectDB
    if args.populate:
        populateDB(startPage=args.startPage, endPage=args.endPage, commit_interval=args.commitInterval)

