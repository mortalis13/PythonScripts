# A Web scraper template
# Gets HTML code from a series of pages
# and finds elements using jQuery selectors

import os, re, codecs, subprocess, time, random
from datetime import datetime

import requests
from pyquery import PyQuery as pq

# pip install requests pyquery


def process_url(url):
  text = ''
  
  try:
    r = requests.get(url, headers={'User-agent':'Magic Browser'})
    # content = r.content
    d = pq(r.text)
    
    links = d('.course-list-item .content h4 a')
    for i in range(links.length):
      link = links.eq(i)
      text += link.html().strip() + ' :: ' + link.attr.href + '\n'
    
    # item_price = d('.product-price-box .price').eq(0).text()
  except Exception as ex:
    print('Error: ' + str(ex))
    text = str(ex)
  
  return text


def run():
  # use generated list of pages or a static urls list
  prefix = 'https://abc.net/forum?page='
  urls = [prefix+str(x) for x in range(1,101)]
  
  urls = [
    'http://url-1.net',
    'http://url-2.net',
  ]
  
  f = codecs.open('scrape_result.txt', 'w', 'utf-8')
  
  date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  f.write('[{}]\n'.format(date_str))
  
  print('total:', len(urls))
  for url in urls:
    print('URL: ' + url)
    text = process_url(url)
    f.write(text + '\n')
    time.sleep(0.2)
  
  f.close()
  
  
# ---
run()
