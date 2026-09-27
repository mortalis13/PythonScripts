# Direct file downloader
# Uses a text file with list of URLs

# pip install requests

import requests, os

from modules.file_system_functions import *
from modules.general_functions import *

path = 'c:/urls.txt'
output = 'c:/output/'

def run():
  with open(path, 'r') as f:
    urls = f.readlines()
  
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
    
    file = os.path.join(output, file_name)
    with open(file, 'wb') as f:
      f.write(content)
    
    i += 1

run()
