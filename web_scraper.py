# A Web scraper template
# Gets HTML code from a series of pages 
# and finds elements using jQuery selectors

import os, re, codecs, subprocess, time, random
from datetime import datetime

import requests
from pyquery import PyQuery as pq

# pip install requests pyquery


def run():
  f = codecs.open('e:/links.txt', 'w', 'utf-8')
  
  base_url = 'https://abc.net/forum/viewforum.php?f=1780'
  max_req = 100
  start = 0
  
  for i in range(max_req):
    url_str = base_url + '&start=' + str(start)
    start += 50

    print('URL: ' + url_str)
    r = requests.get(url_str, headers = {'User-agent': 'your bot 0.1'})
    # content = r.content
    d = pq(r.text)
    
    links = d('a.topic')
    for j in range(links.length):
      link = links.eq(j)
      href = link.attr('href')
      text = link.text()
      text = text.replace('\n', ' ')
      f.write(text + '\n')
    
    time.sleep(0.1)
  # for
  
  f.close()
  
  
# ---
run()
