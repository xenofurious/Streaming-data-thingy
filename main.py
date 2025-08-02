import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from dotenv import load_dotenv
import os

# generating auth key
load_dotenv()
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri="http://127.0.0.1:3000",
                                               scope="user-library-read"))


# taylor swift no way
taylor_uri = 'spotify:artist:06HL4z0CvFAxyc27GXpf02'
results = sp.artist_albums(taylor_uri, album_type='album')
albums = results['items']
while results['next']:
    results = sp.next(results)
    print(results["items"])
    albums.extend(results['items'])

for album in albums:
    print(album['name'])


