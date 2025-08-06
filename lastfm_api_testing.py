import pylast
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("LASTFM_API_KEY")
api_secret = os.getenv("LASTFM_API_SECRET")
username = os.getenv("USERNAME")
password_hash = os.getenv("PASSWORD_HASH")
network = pylast.LastFMNetwork(
    api_key=api_key,
    api_secret=api_secret,
    username=username,
    password_hash=password_hash
)