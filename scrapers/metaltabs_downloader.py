# Downloads tabs from metaltabs.org
# Goes through bands by alphabet, their albums, 
# takes all available tabs links and adds /dl to them, 
# those which are downloadable will be saved (gpx, gp, gp#, ptb), 
# some text tabs can be downloaded, some not.
# Set PARSE_LETTERS to a list of band letters to process

import os, re

import requests
from pyquery import PyQuery as pq

PARSE_LETTERS = ['A']

# 0-9 -> 16
# A -> 453
# B -> 266
# C -> 229
# D -> 328
# E -> 174
# F -> 127
# G -> 151
# H -> 150
# I -> 135
# J -> 45
# K -> 112
# L -> 133
# M -> 222
# N -> 150
# O -> 111
# P -> 164
# Q -> 6
# R -> 144
# S -> 413
# T -> 332
# U -> 44
# V -> 125
# W -> 143
# X -> 14
# Y -> 9
# Z -> 20

class ConnectionRetriesOverflow(Exception): pass

def normalize_filename(val):
  remove_symbols = [':', '\"', '?', '*', '¿', '¡']
  dash_symbols = ['<', '>', '/', '\\', '|']
  
  for sym in remove_symbols:
    val = val.replace(sym, '')
  for sym in dash_symbols:
    val = val.replace(sym, '-')
  
  val = val.rstrip('.')
  return val


def _request(url):
  tries = 1
  while True:
    try:
      return requests.get(url, headers={'User-agent': 'your bot 0.1'})

    except (
      requests.exceptions.ConnectionError,
      requests.exceptions.ChunkedEncodingError
    ):
      print(f'\n== Connection error. Retrying {tries}...')
      if tries == 5:
        raise ConnectionRetriesOverflow()
      tries += 1


def download(url, folder):
  print(url, end='')
  r = _request(url)
  
  if r.status_code != 200:
    print(f' >> [{r.status_code}]')
    if r.status_code != 404:
      print(r.text)
    return
  
  print()
  if not os.path.exists(folder):
    os.makedirs(folder)
  
  name = re.findall('filename=(.+)', r.headers['Content-Disposition'])[0]
  path = folder + '/' + name
  
  if os.path.exists(path):
    print(f'== WARN file exists: {path}')
  
  with open(path, 'wb') as f:
    f.write(r.content)


def get_links(url):
  r = _request(url)
  d = pq(r.text)
  links = d('a')
  return links


def run():
  TRIGGER_URL = ''
  trigger_found = False
  
  url = 'https://metaltabs.org/band/index'
  letter_prefix = 'https://metaltabs.org/band/letter/'
  band_prefix = 'https://metaltabs.org/bands/'
  tab_prefix = 'https://metaltabs.org/tab/'
  
  links = get_links(url)
  
  letters = [link for link in links.items() if letter_prefix in link.attr.href]
  for letter_link in letters:
    url = letter_link.attr.href
    letter = url.replace(letter_prefix, '')
    if letter.upper() not in PARSE_LETTERS:
      continue
    
    print('>> ' + url)
    links = get_links(url)
    bands = [link for link in links.items() if band_prefix in link.attr.href]
    
    bands.sort(key=lambda item: item.attr.href)
    
    num_bands = len(bands)
    print(f'>> {num_bands} bands')
    i = 0
    
    for band_link in bands:
      i += 1
      url = band_link.attr.href
      
      if TRIGGER_URL:
        if not trigger_found and url != TRIGGER_URL:
          continue
        else:
          trigger_found = True
      
      band = band_link.text().strip()
      band_id = url.replace(band_prefix, '')
      
      letter_folder = '0-9' if band[0].isdigit() else band[0].lower()
      band_folder = 'dist/' + letter_folder + '/' + normalize_filename(band)
      
      print(f'>> [{band}] [{i}/{num_bands}] {url}')
      links = get_links(url)
      albums = [link for link in links.items() if band_prefix + band_id in link.attr.href]
      
      tabs_links = []
      for album_link in albums:
        url = album_link.attr.href
        links = get_links(url)
        tabs = [link.attr.href for link in links.items() if tab_prefix in link.attr.href]
        
        for tab_url in tabs:
          tabs_links.append(tab_url.replace(tab_prefix, tab_prefix + 'dl/'))
      
      tabs_links.sort()
      for url in tabs_links:
        try:
          download(url, band_folder)
        except ConnectionRetriesOverflow:
          return
      
      print()
  
# ---
run()
