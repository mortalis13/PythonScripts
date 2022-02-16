# Permanently removes unread messages from a Gmail account

# Preparation, from https://developers.google.com/gmail/api/quickstart/python
# >> pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
# Download 'credentials.json' from 'https://console.developers.google.com -> Credentials -> OAuth'

import os.path
import pickle

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SCOPES = ['https://mail.google.com/']

def auth():
  print('>> auth()')
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

def get_unread(service):
  print('>> get_unread()')
  query = 'is:unread'
  response = service.users().messages().list(userId='me', includeSpamTrash=False, q=query).execute()
  
  messages = []
  if 'messages' in response:
    messages.extend(response['messages'])
    
  while 'nextPageToken' in response:
    page_token = response['nextPageToken']
    response = service.users().messages().list(userId='me', includeSpamTrash=False, q=query, pageToken=page_token).execute()
    messages.extend(response['messages'])

  msg_data = []
  print('\n=== MESSAGES [{}]'.format(len(messages)))
  for m in messages:
    res = service.users().messages().get(userId='me', id=m['id']).execute()
    msg_data.append(res)
    
  return msg_data

def delete_messages(service, messages):
  print('>> delete_messages()')
  for m in messages:
    headers = m['payload']['headers']
    subject = [h['value'] for h in headers if h['name'] == 'Subject']
    print('{} :: {}'.format(subject, m['id']))
  
  res = input('Confirm messages removal [y/n]\n')
  if res.lower() != 'y':
    return
  
  print('\n!! Deleting unread messages...\n')
  total = len(messages)
  for i in range(total):
    m = messages[i]
    res = service.users().messages().delete(userId='me', id=m['id']).execute()
    if not res:
      print('message deleted [{}/{}] [{}]'.format(i+1, total, m['id']))
    else:
      print(res)


def run():
  service = auth()
  messages = get_unread(service)
  delete_messages(service, messages)

# -------------
run()
