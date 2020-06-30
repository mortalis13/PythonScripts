import os.path
import pickle

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# Removes unread messages permanently

# Preparation, from https://developers.google.com/gmail/api/quickstart/python
# >> pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
# Download 'credentials.json' from 'https://console.developers.google.com -> Credentials'


SCOPES = [
  # 'https://www.googleapis.com/auth/gmail.readonly',
  # 'https://www.googleapis.com/auth/gmail.modify',
  'https://mail.google.com/'
]

def get_unread(service):
  query = 'is:unread'
  response = service.users().messages().list(userId='me', q=query).execute()
  
  messages = []
  if 'messages' in response:
    messages.extend(response['messages'])
    
  while 'nextPageToken' in response:
    page_token = response['nextPageToken']
    response = service.users().messages().list(userId='me', q=query, pageToken=page_token).execute()
    messages.extend(response['messages'])

  msg_data = []
  print('\n=== MESSAGES [{}]'.format(len(messages)))
  for m in messages:
    res = service.users().messages().get(userId='me', id=m['id']).execute()
    msg_data.append(res)
    
  return msg_data

def delete_messages(service, messages):
  for m in messages:
    mid = m['id']
    headers = m['payload']['headers']
    subject = [h['value'] for h in headers if h['name'] == 'Subject']
    print('{} :: {}'.format(subject[0], mid))
  
  res = input('Confirm messages removal [y/n]\n')
  if res.lower() != 'y':
    return
  
  print('\n!! Deleting unread messages...\n')
  for m in messages:
    mid = m['id']
    res = service.users().messages().delete(userId='me', id=mid).execute()
    if not res:
      print('.. message deleted [{}]'.format(mid))
    else:
      print(res)


def main():
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
  
  # === Messages
  messages = get_unread(service)
  delete_messages(service, messages)
    

if __name__ == '__main__':
  main()
  