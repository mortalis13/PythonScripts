# Retrieves information from a RSS feed and sends an email with the parsed data

# Preparation, from https://developers.google.com/gmail/api/quickstart/python
# >> pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
# Download 'credentials.json' from 'https://console.developers.google.com -> Credentials -> OAuth'

# pip install feedparser

import feedparser
import time

import os.path
import pickle
import base64

from datetime import datetime, timedelta

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SUBJECT = 'Stack Overflow [ffmpeg]'
TITLE = SUBJECT

RSS_URL_PREFIX = "https://stackoverflow.com/feeds/tag/"
TAGS = ['ffmpeg', 'android-ffmpeg', 'flutter-ffmpeg', 'mobile-ffmpeg', 'ffmpegkit']

SCOPES = ['https://mail.google.com/']


# -- RSS service
def generate_feed_page(start_datetime = None):
  def get_feeds(rss_url):
    feed = feedparser.parse(rss_url)
    if start_datetime:
      print(f"Entries for {rss_url} after {start_datetime}\n--------------")
    else:
      print(f'\nAll entries for {rss_url}\n--------------')
    
    text_html = ''
    for entry in feed.entries:
      publish_datetime = datetime.fromtimestamp(time.mktime(entry['published_parsed']))
      publish_date = publish_datetime.date()
      
      if start_datetime and publish_datetime <= start_datetime:
        continue
      
      feed_date = publish_date.strftime('%Y-%m-%d')
      feed_title = entry['title']
      feed_link = entry['link']
      text_html += f'''
        <div style="padding: 2px;"><b>{feed_date}</b> ::
        <a class="link" style="color: #333; display: inline-block; text-decoration: none;"
          onMouseOver="this.style.textDecoration=\'underline\'"
          onMouseOut="this.style.textDecoration=\'none\'"
          href="{feed_link}">{feed_title}</a>
        </div>\n
      '''
      
      print(f'{feed_date} :: {feed_title}')
    print()
    return text_html
  
  text_html = ''
  for tag in TAGS:
    rss_url = RSS_URL_PREFIX + tag
    feeds_html = get_feeds(rss_url)
    if not feeds_html:
      continue
    text_html += f'''
      <div><b>[{tag}]</b></div>
      <div>{feeds_html}</div>
      <br>
    '''
    
  if not text_html:
    return ''
  
  title = TITLE
  if start_datetime:
    title += f' after {start_datetime}'
  
  text_html = f'''
    <head>
      <style>
        .link {{text-decoration: none;}}
        .link:hover {{text-decoration: underline !important;}}
      </style>
    </head>
    <div><b>{title}</b></div><br>
    <div class="feed_table">
    {text_html}
    </div>
  '''

  return text_html


# -- GMail API
def auth():
  creds = None
  if os.path.exists('token.pickle'):
    print('token.pickle exists')
    with open('token.pickle', 'rb') as token:
      creds = pickle.load(token)
  
  if creds and not creds.valid:
    print('not creds.valid')
    if creds.expired:
      print('creds.expired, trying to refresh')
      try:
        creds.refresh(Request())
      except Exception as ex:
        print(f'Failed to refresh: {ex}')
        creds = None
    else:    
      creds = None
  
  if not creds:
    print('not creds, login')
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
  
  with open('token.pickle', 'wb') as token:
    pickle.dump(creds, token)
  
  service = build('gmail', 'v1', credentials=creds)
  return service

def create_message(subject, body, recepient, sender='test'):
  body_base64 = base64.b64encode(body.encode()).decode()
  
  message = f'''
Content-Type: text/html; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: base64
to: {recepient}
from: {sender}
subject: {subject}

{body_base64}
'''.strip()
  
  message_base64 = base64.urlsafe_b64encode(message.encode()).decode()
  return {'raw': message_base64}

def send_message(service, user_id, message):
  return service.users().messages().send(userId=user_id, body=message).execute()


def get_start_time():
  start_datetime = None
  try:
    with open('rss_so_start_time') as f:
      start_datetime = datetime.strptime(f.read(), '%Y-%m-%d %H:%M:%S')
  except:
    pass
  return start_datetime

def save_start_time():
  with open('rss_so_start_time', 'w') as f:
    f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


def send():
  start_datetime = get_start_time()
  body = generate_feed_page(start_datetime)
  
  if not body:
    print('\nNo new feeds found\n')
    return
  
  user_id = 'me'
  recepient = 'gmail@gmail.com'
  report_date = datetime.now().strftime('%Y-%m-%d %H:%M')
  subject = f'{SUBJECT} [{report_date}]'
  
  service = auth()
  message = create_message(subject, body, recepient)
  result = send_message(service, user_id, message)
  
  save_start_time()
  
  print(result)
  print('\nEmail Sent')


def debug():
  start_datetime = get_start_time()
  body = generate_feed_page(start_datetime)

  with open('rss.html', 'w') as f:
    f.write(body)

  if not body:
    print('\nNo new feeds found\n')
    return
  save_start_time()
  

# ---------
send()
# debug()
