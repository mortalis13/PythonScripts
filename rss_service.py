# Retrieves information from a RSS feed and send an email with the parsed data

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


RSS_URL = "https://stackoverflow.com/feeds/tag/android"
SCOPES = ['https://mail.google.com/']

# -- RSS service
def generate_feed_page(rss_url):
  feed = feedparser.parse(rss_url)
  
  today = datetime.today()
  prev_monday = (today - timedelta(days=today.weekday() + 7)).date()
  prev_sunday = prev_monday + timedelta(days=6)
  
  # Debugging block
  print('___All Entries___')
  text = ''
  for entry in feed.entries:
    publish_date = datetime.fromtimestamp(time.mktime(entry['published_parsed'])).date()
    feed_date = publish_date.strftime('%Y-%m-%d')
    feed_title = entry['title']
    text += f'{feed_date} :: {feed_title}\n'
  print(text)

  # Finds feeds from the previous week (from monday to sunday)
  text_html = text = ''
  for entry in feed.entries:
    publish_date = datetime.fromtimestamp(time.mktime(entry['published_parsed'])).date()
    if publish_date > prev_sunday:
      continue
    if publish_date < prev_monday:
      break
    
    feed_date = publish_date.strftime('%Y-%m-%d')
    feed_title = entry['title']
    feed_link = entry['link']
    text_html += f'<div style="padding: 2px;"><b>{feed_date}</b> :: <a style="color: #333; display: inline-block; text-decoration: none;" href="{feed_link}">{feed_title}</a></div>\n'
    text += f'{feed_date} :: {feed_title}\n'
  
  print(text)
  print(text_html)
    
  text_html = f'''
  <div><b>News</b></div><br>
  <div class="feed_table">
  {text_html}
  </div>
  '''

  return text_html


# -- GMail API
def auth():
  creds = None
  if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
      creds = pickle.load(token)
    if creds.scopes != SCOPES:
      creds = None
  
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
      creds = flow.run_local_server(port=0)
    with open('token.pickle', 'wb') as token:
      pickle.dump(creds, token)
  
  if creds:
    print('SCOPE:', creds.scopes)
  
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


def run():
  user_id = 'me'
  
  report_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  subject = f'News [{report_date}]'
  body = generate_feed_page(RSS_URL)
  recepient = 'gmail@gmail.com'
  
  service = auth()
  message = create_message(subject, body, recepient)
  result = send_message(service, user_id, message)
  
  print(result)
  print('\nEmail Sent')

# ---------
run()
