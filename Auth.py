import base64
import requests
import datetime


class SpotifyAPISession(object):
    client_id = None        # public id
    client_secret = None    # Private id
    access_token = None     # Token used for the session
    access_token_expires = None # Time that the token expires
    

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
            print("Valid Request {}".format(r.status_code))
            return r.json()
        else:
            raise ValueError("Request failed {}".format(r.status_code))
            
    # Request and set access token
    def requestAccessToken(self):
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
        print("token = {}".format(self.access_token))
        
        
    # Return true if the token is expired
    def checkTokenExpiry(self):
        now = datetime.datetime.now()
        expires = now + datetime.timedelta(seconds=self.access_token_expires)
        if expires < now:
            return True
        else:
            return False
        






