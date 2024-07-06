from googleapiclient.discovery import build
import re
import config

# Set up the API client
youtube = build('youtube', 'v3', developerKey=config.api_key)

def get_recent_live_video(channel_id):
    # Retrieve the channel's uploads playlist ID
    channels_response = youtube.channels().list(
        part='contentDetails',
        id=channel_id
    ).execute()

    playlist_id = channels_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    # Get the most recent videos from the uploads playlist
    playlist_items_response = youtube.playlistItems().list(
        part='snippet',
        playlistId=playlist_id,
        maxResults=1  # Modify this if you want to retrieve more recent videos
    ).execute()

    if playlist_items_response['items']:
        video = playlist_items_response['items'][0]
        video_title = video['snippet']['title']
        video_id = video['snippet']['resourceId']['videoId']
        video_url = f'https://www.youtube.com/watch?v={video_id}'

        return video_id
    else:
        print("No recent videos found.")
        
# Specify the channel ID
channel_id = 'UCsfp0zw1hNxpy_wDig8oExA'

# Call the function to retrieve the recent video
vid = get_recent_live_video(channel_id)
