import base64
import requests
import datetime


class SpotifyAPISession(object):
    client_id = None
    client_secret = None
    access_token = None
    access_token_expires = None

    def __init__(self, client_id, client_secret):
        self.client_id = client_id

        with open('secret.txt') as f:
            line = f.readline()
            self.client_secret = line
            f.close()

        
    






