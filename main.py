import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from dotenv import load_dotenv
import os
import pandas as pd

# generating auth key

load_dotenv()
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri="http://127.0.0.1:3000",
                                               scope="user-library-read"))


# okay the actual program
with open('streaming_history/Streaming_History_Audio_2021-2023_0.json') as json_file:
    data = json.load(json_file)

#filterning through the dictionary to delete those that don't fit a certain criteria.
# to explain the criteria,
# i only counts streams >30 seconds, and those with a title. i delete duplicate streams.
# for some reason, some of the songs have no title and are left blank, and i'm really not sure why.
data = pd.DataFrame([entry for entry in data if entry["ms_played"] >30000 and entry['master_metadata_track_name']])
data = data.drop_duplicates(subset=['ts', 'spotify_track_uri'])
def entire_streaming_history():
    return data['master_metadata_track_name']
def entire_uri_history():
    return data['spotify_track_uri']
def streaming_numbers():
    formatted_data = data.groupby(['master_metadata_album_artist_name', 'master_metadata_track_name', 'spotify_track_uri']).size().reset_index(name='count').sort_values('count', ascending=False)
    return formatted_data

#temporary function. this is just for testing
def fetch_most_streamed_song_uri():
    most_streamed_uri = streaming_numbers()['spotify_track_uri'].iloc[0]
    return most_streamed_uri

def fetch_most_streamed_song():
    most_streamed_song = streaming_numbers()[['master_metadata_album_artist_name', 'master_metadata_track_name']].iloc[0]
    return most_streamed_song

#spotify stores three different copies of an image, one for each varying level of quality.
#0 represents highest quality, 1 is medium, 2 is low.
def fetch_image_from_track(uri, quality):
    track = sp.track(uri)
    image = track['album']['images'][quality]
    return image['url']


#okay actually useful functions
def fetch_top_uris(number):
    top_uris = streaming_numbers()['spotify_track_uri'].iloc[:50]
    return top_uris

def fetch_top_songs(number):
    top_songs = streaming_numbers()[['master_metadata_album_artist_name', 'master_metadata_track_name']].iloc[:50]
    return top_songs

#essentially the reason why this function is required is because the spotify api only allows the fetching of 20 images at a time, 10 times a second
#this function returns a list with all of the uris split into groups of 20
def split_uris(top_uris):
    #firstly, repeat int(number/20) times
    number = len(top_uris)
    uri_list = []
    for lower_bracket in range(0, number-20, 20):
        upper_bracket = lower_bracket + 20
        uri_list.append(top_uris.iloc[lower_bracket:upper_bracket])
    uri_list.append(top_uris.iloc[number-(number%20): number])
    return uri_list


#uri = fetch_most_streamed_song_uri()
#print(fetch_image_from_track(uri, 1))
#top_50_songs = fetch_top_songs(50)
#print(top_50_songs)
#print(fetch_most_streamed_song())
print(split_uris(fetch_top_uris(50)))








