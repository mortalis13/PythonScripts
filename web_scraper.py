# A Web scraper template
# Gets HTML code from a series of pages 
# and finds elements using jQuery selectors

import os, re, codecs, subprocess, time, random
from datetime import datetime

import requests
from pyquery import PyQuery as pq

# pip install requests pyquery


def process_url(url_str, list_mode = False):
  r = requests.get(url_str, headers = {'User-agent': 'your bot 0.1'})
  # content = r.content
  d = pq(r.text)
  
  if list_mode:
    links = d('.course-list-item .content h4 a')
    text = ''
    for i in range(links.length):
      link = links.eq(i)
      text += link.html().strip() + ' :: ' + link.attr.href + '\n'
    return text
  
  link = d('a.item')
  link = link.eq(0)
  href = link.attr.href
  text = href
  
  return text

def run():
  f = codecs.open('e:/res_links.txt', 'w', 'utf-8')
  
  # use generated list of pages or a static urls list
  prefix = 'https://abc.net/forum?page='
  urls = [prefix+str(x) for x in range(1,101)]
  
  urls = [
    'http://url-1.net',
    'http://url-2.net',
  ]
  
  print('total:', len(urls))
  for url_str in urls:
    print('URL: ' + url_str)
    text = process_url(url_str)
    f.write(text + '\n')
    time.sleep(0.2)
  
  f.close()
  
  
# ---
run()
