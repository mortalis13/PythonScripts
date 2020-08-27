# Parses .torrent files and writes its structure to a text file

# -- pip install torrent_parser

import os, re, codecs, subprocess
import shutil, stat, errno, sys

from modules.file_system_functions import *

import torrent_parser as tp


def write_file(file_path, text):
  fout = open(file_path, "w", encoding='utf8')
  fout.write(str(text))
  fout.close()


# --------------------------------------------------------------------------

def get_torrent_info(file_path):
  res = ''
  
  try:
    data = tp.parse_torrent_file(file_path)
    
    url = data['publisher-url']
    name = data['info']['name']
    files = data['info']['files']
    
    for f in files:
      tf_path = ''
      path_parts = f['path']
      for part in path_parts:
        tf_path += '/' + part
        
      res += tf_path + '\n'
      
    res = name + '\n' + url + '\n---------------\n' + res
  except:
    msg = "-- Parse Exception: {0}\n{1}\n{2}"
    msg = msg.format('', sys.exc_info()[0], sys.exc_info()[1])
    print('\n' + msg + '\n')
    
  return res


def parse_list(file_paths):
  for file_path in file_paths:
    info = get_torrent_info(file_path)
    info_fp = os.path.splitext(file_path)[0] + '.txt'
    write_file(info_fp, info)

# --------------------------------------------------------------------------

def run():
  file_paths = [
    'e:/torrents/tor_01.torrent',
    'e:/torrents/tor_02.torrent',
    'e:/torrents/tor_03.torrent',
  ]
  
  parse_list(file_paths)


# ---
run()
