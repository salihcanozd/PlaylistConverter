import spotipy
from spotipy.oauth2 import SpotifyOAuth
from googleapiclient.discovery import build

#YouTube API key 
youtube_api_key = '#'  

# Spotify API credentials
client_id = '#'
client_secret = '#'
redirect_uri = '#'

# YouTube playlist ID
youtube_playlist_id = input("Playlist ID: ")  # Replace with your YouTube playlist ID

# Create a YouTube client object
youtube = build('youtube', 'v3', developerKey=youtube_api_key)

# Create a Spotify client object
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope='playlist-modify-private'))

# Get YouTube playlist items
playlist_items = []
next_page_token = None
while True:
    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=youtube_playlist_id,
        maxResults=50,
        pageToken=next_page_token
    )

    response = request.execute()
    playlist_items.extend(response['items'])
    next_page_token = response.get('nextPageToken')
    if not next_page_token:
        break

# Extract video IDs from YouTube playlist items
video_ids = [item['snippet']['resourceId']['videoId'] for item in playlist_items]

# Search for each video on Spotify and add it to the playlist
playlist_name = input("New Playlist Name: ")
user_id = sp.me()['id']  # Retrieve the current user's ID
playlist = sp.user_playlist_create(user_id, playlist_name, public=False)

for item in playlist_items:
    title = item['snippet']['title']
    search_results = sp.search(q=title, type='track', limit=1)
    if search_results['tracks']['items']:
        track_uri = search_results['tracks']['items'][0]['uri']
        sp.user_playlist_add_tracks(user_id, playlist['id'], [track_uri])

print("Playlist conversion completed!")
