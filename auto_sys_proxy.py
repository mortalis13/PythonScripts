# Searches a list of proxies,
# checks active IPs and sets system proxy via Windows Registry
# This reflects the 'Proxy server' section in the 
# 'Control Panel -> Internet Options -> Connections -> LAN Settings'

import time, os, codecs
import requests

from winreg import *
from pyquery import PyQuery as pq

# pip install pyquery

print('== Proxy Change ==')

def get_proxy_list(https_only=True):
  res = []
  url = 'https://free-proxy-list.net'
  
  print('==[REQ]: {}\n'.format(url))
  r = requests.get(url, headers={'User-agent':'Magic Browser'})
  d = pq(r.text)
  
  rows = d('#proxylisttable tr')
  if rows.length:
    header = rows.eq(0)
    cells = header.find('th')
    print('==Table Headers==')
    for c in range(cells.length):
      print('{}:\'{}\'  '.format(c, cells.eq(c).html().strip()), end='')
    print('\n')
  
  for i in range(rows.length):
    row = rows.eq(i)
    cells = row.find('td')
    if not cells or not cells.length:
      continue
    
    # Columns
    ip = cells.eq(0).html().strip()
    port = cells.eq(1).html().strip()
    https = cells.eq(6).html().strip()
    
    if not https_only or https == 'yes':
      res.append('{}:{}'.format(ip, port))
  
  return res
  

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
  

def set_system_proxy(p=''):
  print('set_system_proxy(): ' + p)
  
  disable_proxy = p == ''
  status = 1
  if disable_proxy:
    status = 0
  
  if status:
    print('Enabling System Proxy...')
  else:
    print('Disabling System Proxy...')
  
  keyVal = 'Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings'
  key = OpenKey(HKEY_CURRENT_USER, keyVal, 0, KEY_ALL_ACCESS)
  SetValueEx(key, "ProxyServer", 0, REG_SZ, p)
  SetValueEx(key, "ProxyEnable", 0, REG_DWORD, status)
  CloseKey(key)
  

def get_system_proxy():
  print('get_system_proxy()')
  keyVal = 'Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings'
  key = OpenKey(HKEY_CURRENT_USER, keyVal, 0, KEY_ALL_ACCESS)
  try:
    val = QueryValueEx(key, "ProxyServer")
    val = val[0]
  except:
    val = None
  CloseKey(key)
  
  return val
  

def run(plist=[]):
  fp = 'used_proxies.txt'
  # os.remove(fp)
  if not os.path.exists(fp):
    f = open(fp, 'w'); f.close()
  
  f = codecs.open(fp, 'r+')
  used_proxies = f.readlines()
  used_proxies = [x.strip() for x in used_proxies]
  
  proxy_changed = False
  new_proxy = ''
  
  if not plist:
    plist = get_proxy_list()
  total = len(plist)
  
  print('Checking proxies')
  for i in range(0, total):
    p = plist[i]
    valid_proxy = True
    print('[{}/{}] {}'.format(i, total, p))
    
    current_proxy = get_system_proxy()
    if current_proxy and current_proxy == p:
      print('[SKIP] Currently in use')
      valid_proxy = False
    if valid_proxy:
      for up in used_proxies:
        if up == p:
          print('[SKIP] Already used')
          valid_proxy = False
          break
    
    if valid_proxy:
      res = check_proxy(p, True, 3)
      if res and not proxy_changed:
        print('=== [OK: \'{}\']'.format(p))
        set_system_proxy(p)
        new_proxy = p
        proxy_changed = True
        f.write(p + '\n')
        break
    print('-------------------------------------------')
    
  if proxy_changed:
    print('\n\n======== System proxy changed to: \'{}\' ========'.format(new_proxy))
  else:
    set_system_proxy('')
  
  f.close()


# ----------------
plist = []
run(plist)

# -- Reset system proxy
# set_system_proxy('')
