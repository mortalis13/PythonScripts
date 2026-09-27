# Gets information from YouTube channels

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

config = {}


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


def get_channel_details(channel_name):
  service = config.get('service')
  if not service:
    return None

  request = service.channels().list(part="contentDetails", forUsername=channel_name)
  response = request.execute()

  text = json.dumps(response, indent=2)
  print(text)
  with open('youtube_output.json', 'w', encoding='utf8') as f:
    f.write(text)

  return response


def get_channel_playlists(channel_name):
  service = config.get('service')
  if not service:
    return None

  channel = get_channel_details(channel_name)
  channel_id = channel['items'][0]['id']

  request = service.playlists().list(part="contentDetails", channelId=channel_id, maxResults=50)

  response = request.execute()

  text = json.dumps(response, indent=2)
  print(text)
  with open('youtube_output.json', 'w', encoding='utf8') as f:
    f.write(text)


def get_all_videos(channel_name=None, playlist_id=None):
  service = config.get('service')
  if not service:
    return None

  if not channel_name and not playlist_id:
    return

  if channel_name:
    channel = get_channel_details(channel_name)
    playlist_id = channel['items'][0]['contentDetails']['relatedPlaylists']['uploads']

  videos = []
  next_page = None

  while True:
    print(f'Page: {next_page}')
    request = service.playlistItems().list(part="contentDetails,id,snippet,status", playlistId=playlist_id, maxResults=50, pageToken=next_page)
    response = request.execute()

    videos.extend(response['items'])

    next_page = response.get('nextPageToken')
    if not next_page:
      break
    time.sleep(0.5)

  if not videos:
    print(f'No videos found for playlist {playlist_id}')
    return

  print(f'Total videos: {len(videos)}')

  def _filter_videos_data(item):
    return [item['snippet']['title'], item['contentDetails']['videoId']]
  result = list(map(_filter_videos_data, videos))

  output = 'youtube_videos.json'
  with open(output, 'w', encoding='utf8') as f:
    f.write(json.dumps(result, indent=2))
  print(f'Written to {output}')


def run():
  config['service'] = auth()

  get_channel_playlists('GoogleDevelopers')
  # get_all_videos(channel_name='GoogleDevelopers')


run()
