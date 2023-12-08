import time
import discogs_client
import os
from dotenv import load_dotenv, set_key
from config import COLOR

class DiscogsAccess:
    def __init__(self):
        self.discogsClient = None
        self.allTracks = []
        load_dotenv('./app/.env')

    def setup(self):
        consumerKey = os.getenv('DISCOGS_CONSUMER_KEY')
        consumerSecret = os.getenv('DISCOGS_CONSUMER_SECRET')
        userAgent = os.getenv('DISCOGS_USER_AGENT')

        if os.getenv('DISCOGS_TOKEN') and os.getenv('DISCOGS_SECRET'):
            discogsToken = os.getenv('DISCOGS_TOKEN')
            discogsSecret = os.getenv('DISCOGS_SECRET')

            self.discogsClient = discogs_client.Client(userAgent,
                                                    consumer_key=consumerKey,
                                                    consumer_secret=consumerSecret,
                                                    token=discogsToken,
                                                    secret=discogsSecret)
            self.testDiscogs()

        else:
            self.discogsClient = discogs_client.Client(userAgent,
                                                    consumer_key=consumerKey,
                                                    consumer_secret=consumerSecret)
            (reqToken, reqSecret, authUrl) = self.discogsClient.get_authorize_url()
            print(f"{COLOR.CYAN}Request token :{COLOR.ENDC} {reqToken}")
            print(f"{COLOR.CYAN}Request secret :{COLOR.ENDC} {reqSecret}")
            print(f"{COLOR.CYAN}Authorization URL :{COLOR.ENDC} {authUrl}")
            print(f"{COLOR.HEADER}[Please complete authorization]{COLOR.ENDC}")
            self.setupAddOAuthToken(reqToken, reqSecret)

    def setupAddOAuthToken(self, reqToken, reqSecret):
        token = input(f"{COLOR.BLUE}Please enter your verifier token : {COLOR.ENDC}")
        if token:
            accessToken, accessTokenSecret = self.discogsClient.get_access_token(token)
            set_key('./app/.env', 'DISCOGS_TOKEN', accessToken)
            set_key('./app/.env', 'DISCOGS_SECRET', accessTokenSecret)
            print(f"{COLOR.CYAN}Your request token and request secret have been stored in ./app/.env{COLOR.ENDC}")
        self.testDiscogs()


    def testDiscogs(self):
        user = self.discogsClient.identity()
        if user:
            print(f"{COLOR.GREEN}[Successful authorization]{COLOR.ENDC} Welcome {user.username}")
        else:
            print(f"{COLOR.FAIL}[Unsuccessful authorization]{COLOR.ENDC}")



    def getTracks(self, startPage=1, endPage=5, timeout=2):
        tracks = []
        print(f"{COLOR.CYAN}Start page: {startPage}, end page: {endPage}{COLOR.ENDC}")
        for page in range(startPage, endPage+1):
            try:
                results = self.discogsClient.search(type='release', page=page)
                tracks.extend(results.page(1))
                print(f"{COLOR.BLUE}[Page retrieved]{COLOR.ENDC} Page : {page}")
                time.sleep(timeout)
            except discogs_client.exceptions.HTTPError as e:
                print(f"{COLOR.FAIL}[Rate limit exceeded]{COLOR.ENDC} waiting to retry...")
                time.sleep(60)
                continue
        return tracks

    def searchTracks(self, searchItem, searchType='release'):
        results = self.discogsClient.search(searchItem, type=searchType)
        return results
