import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth


# Spotify Authentication
SPOTIPY_CLIENT_ID = "####################"
SPOTIPY_CLIENT_SECRET = "####################"
SPOTIPY_REDIRECT_URI = "####################"

scope = 'playlist-modify-public'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=scope
))


def scrape_billboard_data():
    URL = "https://www.billboard.com/charts/year-end/hot-100-songs/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, "html.parser")

    chart_items = soup.find_all("li", class_="o-chart-results-list__item")

    songs = []

    for item in chart_items:
        title_tag = item.find('h3', class_='c-title')
        artist_tag = item.find('span', class_='c-label')
        
        if title_tag and artist_tag:
            title = title_tag.get_text(strip=True)
            artist = artist_tag.get_text(strip=True)
            songs.append({'title': title, 'artist': artist})

    return songs

def create_spotify_playlist(song_list):
    user_id = sp.me()['id']
    playlist = sp.user_playlist_create(user=user_id, name="Billboard Top 100", public=True)
    
    track_uris = []
    for song in song_list: 
        query = f"track:{song['title']} artist:{song['artist']}"
        result = sp.search(q=query, type='track', limit=1)
        tracks = result.get('tracks', {}).get('items', [])
        if tracks:
            track_uris.append(tracks[0]['uri'])
            
    if track_uris:
        sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist['id'], tracks=track_uris)

    return playlist['external_urls']['spotify']

if __name__ == "__main__":
    songs = scrape_billboard_data()
    playlist_url = create_spotify_playlist(songs)
    print(f"Successfully created Spotify playlist! Check it out here: {playlist_url}")





    



