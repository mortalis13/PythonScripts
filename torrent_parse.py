# Parses .torrent files and writes the structure to a text file

# pip install torrent_parser

import os
import sys

import torrent_parser

from modules.file_system_functions import *

files = [
  'c:/torrents/01.torrent',
  'c:/torrents/02.torrent',
  'c:/torrents/03.torrent',
]


def get_torrent_info(path):
  res = ''

  try:
    data = torrent_parser.parse_torrent_file(path)

    url = data['publisher-url']
    name = data['info']['name']
    files = data['info']['files']

    for file in files:
      tf_path = ''
      path_parts = file['path']
      for part in path_parts:
        tf_path += '/' + part

      res += tf_path + '\n'

    res = name + '\n' + url + '\n---------------\n' + res

  except:
    msg = '-- Parse Exception: {0}\n{1}\n{2}'.format('', sys.exc_info()[0], sys.exc_info()[1])
    print('\n' + msg + '\n')

  return res


def run():
  for file in files:
    info = get_torrent_info(file)
    path = os.path.splitext(file)[0] + '.txt'

    with open(path, 'w', encoding='utf8') as f:
      f.write(str(info))


run()
