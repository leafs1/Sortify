# This script when run will remove all old songs from a playlist given the playlist name
import Session

# Start new session with API and get token
session = Session.SpotifyAPISession('fa735535f8424e409a0ee7537cc4dd7f')

#print("{}\n{}\n{}\n{}\n".format(session.client_id, session.client_secret, session.access_token, session.access_token_expires))
session.requestAccessToken()

#print("{}\n{}\n{}\n{}\n".format(session.client_id, session.client_secret, session.access_token, session.access_token_expires))
#session.checkTokenExpiry()

#session.requestUserTopTracks()