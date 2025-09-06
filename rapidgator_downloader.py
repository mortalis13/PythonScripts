# Downloads a file from rapidgator.net using its API
# Accepts file ID or the full link that includes file ID

import sys
import re
import codecs
import requests

EMAIL = ''
PASS = ''

def format_size(byte_size, max_unit=''):
  byte_size = int(byte_size)
  for unit in ['B', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
    if abs(byte_size) < 1024.0 or unit == max_unit:
      fmt = '{:.2f} {}'
      if unit == 'B':
        fmt = '{:d} {}'
      res = fmt.format(byte_size, unit)
      return res
    byte_size /= 1024.0
  return '{:.2f} {}'.format(byte_size, 'Yi')


def login():
  print('login()')
  url = 'http://rapidgator.net/api/v2/user/login?login={}&password={}'.format(EMAIL, PASS)
  headers = {'User-Agent': "Magic Browser"}
  resp = requests.get(url, headers=headers)
  
  if resp.status_code == 200 and resp.json():
    jresp = resp.json()['response']
    if not jresp:
      print('[SKIP], not jresp, details: ' + str(resp.json()))
      return None
    token = jresp['token']
    print('token: "{}"'.format(token))
    return token
  else:
    print('[ERROR] Incorrect login')
  
  return None


def download_file(file_id, user_token):
  print(f'download_file() {file_id}')
  headers = {'User-Agent': "Magic Browser"}
  
  # -------- Connect
  url = 'http://rapidgator.net/api/v2/file/download?file_id={}&token={}'.format(file_id, user_token)
  
# ====== [REQ] ======
  print('[REQ] {}'.format(url))
  try:
    resp = requests.get(url, timeout=20, headers=headers)
  except Exception as ex:
    print(f'[SKIP] Request error: {ex}')
    return False
  
  if resp.status_code != 200:
    print('[SKIP], status_code: {}, text: {}'.format(resp.status_code, resp.text))
    return False
    
  jresp = resp.json()['response']
  if not jresp:
    print('[ERROR]: "' + resp.json()['details'] + '"')
    print(resp.json())
    return False
  
  
  # --------- Download
  url = jresp['download_url']
  print('== download_url: ' + url)

# ====== [REQ] ======
  print('\n[REQ] {}'.format(url))
  try:
    resp = requests.get(url, stream=True, headers=headers)
  except:
    print(f'[SKIP] Request error: {ex}')
    return False
  print(resp.headers)
  
  total_bytes = -1
  fp = file_id
  
  try:
    if resp.headers['Content-Type'] == 'application/json':
      print('[SKIP] error in download: ' + str(resp.json()))
      return False
    if resp.headers['Content-Disposition']:
      fp = re.findall('filename="(.+)"', resp.headers['Content-Disposition'])
      if len(fp):
        fp = fp[0]
    total_bytes = resp.headers['Content-Length']
  except:
    print('[ERROR]: Processing headers')
  
  print('\nWriting to "{}"'.format(fp))
  done = 0

  f = codecs.open(fp, 'wb')
  try:
    for chunk in resp.iter_content(512):
      done += f.write(chunk)
      print('[DONE] {} / {}     \r'.format(format_size(done), format_size(total_bytes)), end='')
    print()
  except Exception as e:
    print(f'\n[SKIP] Exception reading data: {e}')
    return False
  f.close()
  
  return True


def run():
  if len(sys.argv) < 2:
    print('Specify file id')
    return
  
  file_id = sys.argv[1]
  if file_id.startswith('https:'):
    file_id = re.findall('https://rapidgator.net/file/(\w+)', file_id)[0]
  user_token = login()
  
  if not user_token:
    print('\nError getting user token\n')
    return
  
  res = download_file(file_id, user_token)
  if res:
    print('Downloading finished')


# ------
run()
