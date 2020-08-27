# Direct file downloader
# Uses a text file with list of URLs

import requests, re, codecs, os

from modules.file_system_functions import *
from modules.general_functions import *


def run():
  fp = 'e:/Documents/urls.txt'
  base_dir = 'e:/output/'
  print('Prosessing ' + fp)
  
  f = codecs.open(fp, 'r', 'utf8')
  urls = f.readlines()
  f.close()
  
  i = 1
  
  for url in urls:
    url = url.strip()
    if len(url) == 0:
      continue
    
    file_name = '%03d'%i + '_' + os.path.basename(url)
    print(file_name)
    
    req = requests.get(url)
    content = req.content
    headers = req.headers
    
    fpout = base_dir + file_name
    f = codecs.open(fpout, 'wb')
    f.write(content)
    f.close()
    
    i += 1


run()
