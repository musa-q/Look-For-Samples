from db import dbManager
import argparse
from populateDb import populateTracks

def setup():
    dbManager.create()

def reset():
    dbManager.reset()

def outputDB():
    dbManager.output()

def countDB():
    dbManager.countRows()

def populateDB(commit_interval=25):
    populateTracks(commit_interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--setup", action="store_true", help="Setup the database")
    parser.add_argument("-r", "--reset", action="store_true", help="Resets the database")
    parser.add_argument("-o", "--output", action="store_true", help="Prints the values from the database")
    parser.add_argument("-p", "--populate", action="store_true", help="Populate the database with tracks")
    parser.add_argument("-c", "--commitInterval", type=int, default=25, help="Specify commit interval for populate")
    parser.add_argument("-t", "--count", action="store_true", help="Count the number of rows in the database")

    args = parser.parse_args()

    if args.setup:
        setup()
    if args.reset:
        reset()
    if args.output:
        outputDB()
    if args.populate:
        populateDB(args.commitInterval)
    if args.count:
        countDB()
