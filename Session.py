import base64
import requests
import datetime
from urllib.parse import urlencode
from requests.models import codes
import six
from bottle import route, run, request
import spotipy
from spotipy import oauth2



class SpotifyAPISession(object):
    client_id = None        # public id
    client_secret = None    # Private id
    access_token = None     # Token used for the session
    access_token_expires = None # Time that the token expires
    base_url = "https://api.spotify.com/v1"
    

    def __init__(self, client_id):
        self.client_id = client_id

        with open('secret.txt') as f:
            line = f.readline()
            self.client_secret = line
            f.close()

    # Generic function to send HTTP request returning data in JSON form
    def sendRequest(self, r_url, r_data, r_headers, r_type):
        # Make request given data
        r = requests.request(r_type, url=r_url, data=r_data, headers=r_headers)
        
        # Determine whether request is valid and handle both cases
        valid_request = r.status_code in range(200, 299)

        if valid_request:
            #print("Valid Request {}".format(r.status_code))
            return r.json()
        else:
            raise ValueError("Request failed {}".format(r.status_code))
            
    # Request and set access token
    def requestAccessToken(self):
        SPOTIPY_CLIENT_ID = self.client_id
        SPOTIPY_CLIENT_SECRET = self.client_secret
        SPOTIPY_REDIRECT_URI = 'http://localhost:8080'
        SCOPE = 'user-read-playback-state'
        CACHE = '.spotipyoauthcache'

        sp_oauth = oauth2.SpotifyOAuth( SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope=SCOPE,cache_path=CACHE )

        @route('/')
        def index():
                
            access_token = ""

            token_info = sp_oauth.get_cached_token()

            if token_info:
                print("Found cached token!")
                access_token = token_info['access_token']
            else:
                url = request.url
                code = sp_oauth.parse_response_code(url)
                if code != url:
                    print("Found Spotify auth code in Request URL! Trying to get valid access token...")
                    token_info = sp_oauth.get_access_token(code)
                    access_token = token_info['access_token']

            if access_token:
                print("Access token available! Trying to get user information...")
                sp = spotipy.Spotify(access_token)
                results = sp.current_user()
                return results

            else:
                return htmlForLoginButton()

        def htmlForLoginButton():
            auth_url = getSPOauthURI()
            htmlLoginButton = "<a href='" + auth_url + "'>Login to Spotify</a>"
            return htmlLoginButton

        def getSPOauthURI():
            auth_url = sp_oauth.get_authorize_url()
            return auth_url

        run(host='', port=8080)

        

        '''
        auth_url = "https://accounts.spotify.com/authorize?" + urlencode({
                                                                'client_id': self.client_id, 
                                                                'response_type': 'code',
                                                                'redirect_uri': 'http://localhost:8080'
                                                                })





        url = "https://accounts.spotify.com/api/token" 
        auth_header = base64.b64encode(six.text_type(self.client_id + ':' + self.client_secret).encode('ascii')) 
        

        headers = {
            'Authorization':'Basic %s' % auth_header.decode('ascii')
        }
        
        data = {
            'grant_type': 'authorization_code',
            'scope': scopes,


        }




        client_creds = f"{self.client_id}:{self.client_secret}"     # client information formatted
        client_creds_b64 = base64.b64encode(client_creds.encode())  # client information in b64

        # Post Request to Spotify details
        token_url = "https://accounts.spotify.com/api/token"        

        token_data = {
            "grant_type": "client_credentials"
        }

        token_headers = {
            "Authorization": f"Basic {client_creds_b64.decode()}"
        }

        # Send Post request and if the response is valid, record the information
        response = self.sendRequest(token_url, token_data, token_headers, 'POST')
        
        self.access_token = response['access_token']
        self.access_token_expires = response['expires_in']
        #print("token = {}".format(self.access_token))
        '''


        



    # Simply request and return a user's top tracks as a json    
    def requestUserTopTracks(self):
        print(self.access_token)
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        data = urlencode({
            "limit": 5,
            "offset": 0,
            "time_range": "short_term"
        })
        endpoint = self.base_url + "/me/top/tracks"
        lookup_url = f"{endpoint}?{data}"
        print(lookup_url)
        r = requests.get(lookup_url, headers=headers)
        print(r.status_code)
        
        




    # Return true if the token is expired
    def checkTokenExpiry(self):
        now = datetime.datetime.now()
        expires = now + datetime.timedelta(seconds=self.access_token_expires)
        if expires < now:
            print("expired")
            return True
        else:
            print("not expired")
            return False
        






