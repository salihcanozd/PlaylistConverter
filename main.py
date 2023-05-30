import os
import googleapiclient.discovery
from googleapiclient.errors import HttpError

# Set up the API client
api_service_name = "youtube"
api_version = "v3"
api_key = ""  # Replace with your own YouTube Data API key

# Function to retrieve video names from a playlist
def get_video_names(playlist_id):
    try:
        # Create a YouTube Data API client
        youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)

        # Retrieve the playlist items
        playlist_items = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=150  # Adjust the maximum number of results as needed
        ).execute()

        # Extract video names from the playlist items
        video_names = [item["snippet"]["title"] for item in playlist_items["items"]]

        return video_names

    except HttpError as e:
        print("An HTTP error occurred:")
        print(e)
        return None

# Main function
def main():
    # Prompt the user to enter the YouTube playlist ID
    playlist_id = input("Enter the YouTube playlist ID: ")

    # Retrieve video names from the playlist
    video_names = get_video_names(playlist_id)
    counter = 0
    # Display the video names
    if video_names:
        print("\nVideo Names:")
        for name in video_names:
            counter = counter + 1
            print(str(counter)+ ". " + name)
    else:
        print("Failed to retrieve video names.")

if __name__ == "__main__":
    main()
