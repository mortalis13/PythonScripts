# Batch downloader for Firefox addons
# Put direct URLs to a text file ('addons_1.txt') and run
# Download links are generated with 'addons_parse.py'

import requests, re, codecs, os

from modules.file_system_functions import *
from modules.general_functions import *


def run():
  files = [
    'data/addons_1.txt'
  ]
  
  fp = files[0]
  print('Prosessing ' + fp)
  
  f = codecs.open(fp, 'r', 'utf8')
  urls = f.readlines()
  f.close()
  
  addon_folder = os.path.splitext(os.path.basename(fp))[0]
  base_dir = 'e:/_addons-download/' + addon_folder + '/'
  if not os.path.exists(base_dir):
    os.mkdir(base_dir)
  
  for url in urls:
    url = url.strip()
    if len(url) == 0:
      continue
    
    file_name = regex_search(url, '([^/]+xpi)$', 1)
    print(file_name)
    
    req = requests.get(url)
    content = req.content
    
    fpout = base_dir + file_name
    f = codecs.open(fpout, 'wb')
    f.write(content)
    f.close()


run()
