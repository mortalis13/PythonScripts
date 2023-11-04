# Get information from youtube channels

# Preparation, from https://developers.google.com/youtube/v3/quickstart/python
# >> pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
# Download 'credentials.json' from 'https://console.developers.google.com -> Credentials -> OAuth'

import os
import pickle
import json
import time

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
CLIENT_SECRETS_FILE = "credentials.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

def auth():
  token_name = f'token_{API_SERVICE_NAME}.pickle'

  creds = None
  if os.path.exists(token_name):
    with open(token_name, 'rb') as token:
      creds = pickle.load(token)
    if creds.scopes != SCOPES:
      creds = None
  
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      # Get credentials and create an API client
      flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
      creds = flow.run_local_server(port=0)
    with open(token_name, 'wb') as token:
      pickle.dump(creds, token)
  
  if creds:
    print('SCOPE:', creds.scopes)
  
  service = build(API_SERVICE_NAME, API_VERSION, credentials=creds)
  return service


def test():
    service = auth()
    
    request = service.channels().list(part="contentDetails", forUsername="GoogleDevelopers")
    # request = service.playlists().list(part="contentDetails", channelId="UC_x5XG1OV2P6uZZ5FSM9Ttw", maxResults=50)
    # request = service.playlistItems().list(part="contentDetails,snippet", playlistId="UU_x5XG1OV2P6uZZ5FSM9Ttw", maxResults=50)
    
    response = request.execute()

    text = json.dumps(response, indent=2)
    print(text)
    with open('youtube_output.json', 'w', encoding='utf8') as f:
      f.write(text)


def get_all_videos(service, playlist_id=None):
  items = []
  next_page = None
  
  if playlist_id:
    while True:
      print(f'page: {next_page}')
      request = service.playlistItems().list(part="contentDetails,id,snippet,status", playlistId=playlist_id, maxResults=50, pageToken=next_page)
      response = request.execute()
      
      items.extend(response['items'])
      
      next_page = response.get('nextPageToken')
      if not next_page:
        break
      time.sleep(0.5)
      
    return items


def process_all_videos():
  service = auth()
  videos = get_all_videos(service, playlist_id='UU_x5XG1OV2P6uZZ5FSM9Ttw')
  
  if not videos:
    print('videos empty')
    return
  
  print(f'total videos: {len(videos)}')

  def filter_videos_data(item):
    return [item['snippet']['title'], item['contentDetails']['videoId']]
  result = list(map(filter_videos_data, videos))

  output = 'youtube_videos.json'
  with open(output, 'w', encoding='utf8') as f:
    f.write(json.dumps(result, indent=2))
  print(f'written to {output}')


def run():
  process_all_videos()


run()
# test()
