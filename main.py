import spotipy
from bs4 import BeautifulSoup
import requests
from spotipy.oauth2 import SpotifyOAuth

ENDPOINT = "https://www.billboard.com/charts"
SPOTIPY_CLIENT_ID = 'your client id'
SPOTIPY_CLIENT_SECRET = 'your client secret'
SPOTIPY_REDIRECT_URI = 'https://examle.com/callback/'

scope = "user-library-read"
create_playlist = "playlist-modify-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=scope,
))


user_id = sp.current_user()["id"]


date = input("enter the date you want type the date format like this YYYY-MM-DD\n")
response = requests.get(f"{ENDPOINT}/hot-100/{date}/")
data = response.text
soup = BeautifulSoup(data, "lxml")
songs_list = [song.get_text().strip() for song in soup.select("li h3#title-of-a-story")]

year = date.split("-")[0]
songs_uri = []

for song in songs_list:
    try:
        result = sp.search(q=f"track:{song} year:{year}", type="track")
        uri = result["tracks"]["items"][0]["uri"]
        songs_uri.append(uri)
    except IndexError:
        print("song not found")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
playlist_id = playlist["id"]
sp.playlist_add_items(playlist_id=playlist["id"], items=songs_uri)
