# Send an email

# Preparation, from https://developers.google.com/gmail/api/quickstart/python
# >> pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
# Download 'credentials.json' from 'https://console.developers.google.com -> Credentials -> OAuth'

import os.path
import pickle
import base64

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SCOPES = ['https://mail.google.com/']

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
  
  subject = 'test'
  body = 'body'
  recepient = 'gmail@gmail.com'
  
  service = auth()
  message = create_message(subject, body, recepient)
  result = send_message(service, user_id, message)
  
  print(result)
  print('\nEmail Sent')
  
# -------------
run()
  