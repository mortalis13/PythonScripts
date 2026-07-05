# Downloads a file with direct connection 
# or using a proxy from a proxy list

import time, os, codecs, re
import requests

plist = ['1.1.1.1:1234']

print('== Proxy Downloader ==')

def check_proxy(p, https=True, timeout=5):
  res = True
  proxies = {"http":"http://"+p, "https":"https://"+p}
  
  try:
    print('[http]...', end='')
    resp = requests.get('http://ip-api.com/json', proxies=proxies, timeout=timeout)
    json = resp.json()
    # print(json)
    print('OK')
    
    if https and res:
      print('[https]...', end='')
      resp = requests.get('https://cat-fact.herokuapp.com/facts/', proxies=proxies, timeout=timeout)
      json = resp.json()
      # print(json)
      print('OK')
  except:
    print('ERROR')
    res = False
  
  return res

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


def download_file(url, proxies=None):
  headers = {'User-Agent':"Magic Browser"}
  
# ====== [REQ] ======
  print('\n[REQ] {}'.format(url))
  try:
    resp = requests.get(url, stream=True, headers=headers, proxies=proxies)
  except:
    print('[SKIP] Request error')
    return False
  print(resp.headers)
  
  total_bytes = -1
  fp = 'a_file'
  
  try:
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
  except:
    print('\n[SKIP] Exception reading data')
    return False
  f.close()
  
  return True


def run(plist=[]):
  url = 'https://...'
  
  print('\n================\n  Downloading with the direct connection\n================')
  res = download_file(url)
  if res:
    print('Downloading finished')
    return
  
  
  print('\n\n================\n  Downloading with a proxy list\n================')
  total = len(plist)
  for i in range(0, total):
    p = plist[i]
    print('\n-------------------------------------------')
    print('Proxy: [{}/{}] {}'.format(i, total, p))

    res = check_proxy(p, False, 3)
    if not res:
      continue
    
    proxies = {"http":"http://"+p, "https":"https://"+p}
    res = download_file(_file_id, _user_token, proxies)
    if res:
      print('\nDownloading finished')
      return

# ----------------
run(plist)
