# Exports Google Keep notes to a text file

# Based on 'https://github.com/kiwiz/gkeepapi'
# and 'https://stackoverflow.com/questions/22832104/how-can-i-see-hidden-app-data-in-google-drive/36487545#36487545'


import base64, hashlib, binascii
import sys, codecs
import requests, webbrowser, uuid

from datetime import datetime
from getpass import getpass
from uuid import getnode as get_mac
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP


# Enable account access for the Google account
# https://accounts.google.com/b/0/DisplayUnlockCaptcha


def keep_api_test():
  # a package from the 'https://github.com/kiwiz/gkeepapi' project
  # pip install gkeepapi
  import gkeepapi

  print('--keep_api_test')
  with open('usr') as f: usr = f.read()
  # with open('psw') as f: psw = f.read()
  psw = getpass('')
  keep = gkeepapi.Keep()
  success = keep.login(usr, psw)

  print('connected:', success)


# -- Utils
def bytes_to_long(s):
  return int.from_bytes(s, "big")
def long_to_bytes(lnum, padmultiple=1):
  if lnum == 0:
    return b'\0' * padmultiple
  elif lnum < 0:
    raise ValueError("Can only convert non-negative numbers.")
  s = hex(lnum)[2:]
  s = s.rstrip('L')
  if len(s) & 1:
    s = '0' + s
  s = binascii.unhexlify(s)
  if (padmultiple != 1) and (padmultiple != 0):
    filled_so_far = len(s) % padmultiple
    if filled_so_far != 0:
      s = b'\0' * (padmultiple - filled_so_far) + s
  return s

def key_to_struct(key):
  mod = long_to_bytes(key.n)
  exponent = long_to_bytes(key.e)
  return b'\x00\x00\x00\x80' + mod + b'\x00\x00\x00\x03' + exponent

def key_from_b64(b64_key):
  binaryKey = base64.b64decode(b64_key)

  i = bytes_to_long(binaryKey[:4])
  mod = bytes_to_long(binaryKey[4:4+i])

  j = bytes_to_long(binaryKey[i+4:i+4+4])
  exponent = bytes_to_long(binaryKey[i+8:i+8+j])

  key = RSA.construct((mod, exponent))
  return key

def g_signature(email, password, key):
  signature = bytearray(b'\x00')

  struct = key_to_struct(key)
  signature.extend(hashlib.sha1(struct).digest()[:4])

  cipher = PKCS1_OAEP.new(key)
  encrypted_login = cipher.encrypt((email + u'\x00' + password).encode('utf-8'))

  signature.extend(encrypted_login)
  return base64.urlsafe_b64encode(signature)

def parse_auth_response(text):
  response_data = {}
  for line in text.split('\n'):
    if not line:
      continue
    key, _, val = line.partition('=')
    response_data[key] = val
  return response_data


# -- Main
def run():
  print('== Google Keep Exporter v1.0 ==')
  
  # --- I - API Data
  __version__ = '0.4.1'
  auth_url = 'https://android.clients.google.com/auth'
  api_url = 'https://www.googleapis.com/notes/v1/changes'
  useragent = 'gpsoauth/' + __version__
  
  b64_key_7_3_29 = (b"AAAAgMom/1a/v0lblO2Ubrt60J2gcuXSljGFQXgcyZWveWLEwo6prwgi3"
                    b"iJIZdodyhKZQrNWp5nKJ3srRXcUW+F1BD3baEVGcmEgqaLZUNBjm057pK"
                    b"RI16kB0YppeGx5qIQ5QjKzsR8ETQbKLNWgRY0QRNVz34kMJR3P/LgHax/"
                    b"6rmf5AAAAAwEAAQ==")
  
  android_key_7_3_29 = key_from_b64(b64_key_7_3_29)
  # session_id = str(uuid.uuid1())
  session_id = 's2'
  
  # --- II - Token
  email = '<mail>@gmail.com'
  password = '<gmail_pass>'
  service = 'ac2dm'
  # android_id = get_mac()
  android_id = None
  device_country = 'us'
  lang = 'en'
  sdk_version = 17
  
  print('Your pass...')
  password = getpass('')
  
  print('\nAuthorizing...')
  data = {
    'accountType': 'HOSTED_OR_GOOGLE',
    'Email':   email,
    'has_permission':  1,
    'add_account': 1,
    'EncryptedPasswd': g_signature(email, password, android_key_7_3_29),
    'service': service,
    'source':  'android',
    'androidId':   android_id,
    'device_country':  device_country,
    'operatorCountry': device_country,
    'lang':    lang,
    'sdk_version': sdk_version
  }
  
  session = requests.session()
  res = session.post(auth_url, data, headers={'User-Agent': useragent})
  if not res.status_code == 200:
    print('..ERROR Request:', res.text)
    if res.text.find('NeedsBrowser') != -1:
      print('\nAllow access to the Google account')
      access_url = 'https://accounts.google.com/b/0/DisplayUnlockCaptcha'
      print('Trying to open browser at \'{}\'...'.format(access_url))
      print('Press Enter after enabling access...\n')
      webbrowser.open(access_url, new=2)
      
      input()
      res = session.post(auth_url, data, headers={'User-Agent': useragent})
      if not res.status_code == 200:
        return
  
  res = parse_auth_response(res.text)
  print(res['Token'])
  print()
  psw1 = res['Token']
  
  # --- III - Google Keep connection
  app = 'com.google.android.keep'
  client_sig = '38918a453d07199354f8b19af05ec6562ced5788'
  service = 'oauth2:https://www.googleapis.com/auth/memento'
  
  data = {
    'accountType': 'HOSTED_OR_GOOGLE',
    'Email':   email,
    'has_permission':  1,
    'EncryptedPasswd': psw1,
    'service': service,
    'source':  'android',
    'androidId':   android_id,
    'app': app,
    'client_sig': client_sig,
    'device_country':  device_country,
    'operatorCountry': device_country,
    'lang':    lang,
    'sdk_version': sdk_version
  }
  
  session = requests.session()
  res = session.post(auth_url, data, headers={'User-Agent': useragent})
  if not res.status_code == 200:
    print('..ERROR Request [2]:', res.text)
    return
  res = parse_auth_response(res.text)
  auth_token = res['Auth']
  print(auth_token)
  
  # --- IV
  print('\nCalling API...')
  data = {
    'clientTimestamp': datetime.now().isoformat()+'Z',
    'requestHeader': {
      'clientSessionId': session_id,
      'clientPlatform': 'ANDROID',
      'clientVersion': {
        'major': '9',
        'minor': '9',
        'build': '9',
        'revision': '9'
      },
      'capabilities': [
        {'type': 'NC'}, # Color support (Send note color)
        {'type': 'PI'}, # Pinned support (Send note pinned)
        {'type': 'LB'}, # Labels support (Send note labels)
        {'type': 'AN'}, # Annotations support (Send annotations)
        {'type': 'SH'}, # Sharing support
        {'type': 'DR'}, # Drawing support
        {'type': 'TR'}, # Trash support (Stop setting the delete timestamp)
        {'type': 'IN'}, # Indentation support (Send listitem parent)

        {'type': 'SNB'}, # Allows modification of shared notes?
        {'type': 'MI'},  # Concise blob info?
        {'type': 'CO'},  # VSS_SUCCEEDED when off?
      ]
    },
  }
  
  session = requests.session()
  res = session.post(url=api_url, json=data, headers={'Authorization': 'OAuth ' + auth_token})
  if not res.status_code == 200:
    print('..ERROR Request [3]:', res.text)
    print()
    print(res)
    return
  res = res.json()
  if 'error' in res:
    print('Response with error:', res['error'])
    return
  
  if 'nodes' not in res:
    print('\'nodes\' key missing from JSON')
    return
  
  # --- V
  print('\nProcessing notes...')
  final_notes = {}
  nodes = res['nodes']
  for node in nodes:
    note_id = node['id']
    note_parent = node['parentId']
    
    # -- Node keys
    # kind id serverId parentId type timestamps title nodeSettings isArchived isPinned color sortValue annotationsGroup lastModifierEmail moved
    
    value = {}
    if note_parent == 'root':
      key = note_id
      if 'title' in node:
        value['title'] = node['title']
      if 'isArchived' in node:
        value['isArchived'] = node['isArchived']
      if 'isPinned' in node:
        value['isPinned'] = node['isPinned']
    else:
      key = note_parent
      if 'text' in node:
        value['text'] = node['text']
    
    if key not in final_notes:
      final_notes[key] = value
    else:
      final_notes[key].update(value)
    
  # --- VI
  print('\nWriting file...')
  notes_list = []
  for key in final_notes:
    notes_list.append(final_notes[key])
  
  notes_list.sort(key=lambda x: (x['isArchived'], not x['isPinned']))
  
  now = datetime.now()
  dt = '{:4}_{:2}_{:2}'.format(now.year, now.month, now.day)
  
  fn = 'keep_notes_{}.txt'.format(dt)
  f = codecs.open(fn, 'w', 'utf8')
  for note in notes_list:
    f.write('[' + note['title'] + ']')
    if note['isPinned']:
      f.write(' [PINNED]')
    if note['isArchived']:
      f.write(' [ARCHIVE]')
    f.write('\n')
    f.write('------------------------------------------\n')
    
    f.write(note['text'] + '\n')
    f.write('------------------------------------------\n\n\n')
  f.close()
  
  print('\n>>> File written: \'' + fn + '\'')
  
  
# ----
run()
# keep_api_test()
