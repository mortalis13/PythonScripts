# HTML pages parser
# Loads page URLs from a list
# As a test loads GuitarPro tab ids from ultimate-guitar.com
# and writes the to a text file

from pyquery import PyQuery as pq
from lxml import etree
import urllib

import http.client, json

import os, re, codecs, subprocess
import shutil, stat, errno, sys, http

from modules.file_system_functions import *
from modules.general_functions import *


def get_ids_gp_tabs():
  fp = 'E:/Documents/tab-pages.txt'
  fp_res = 'E:/Documents/tab_ids.txt'
  
  f = codecs.open(fp, 'r', 'utf-8')
  f_res = codecs.open(fp_res, 'w', 'utf8')
  
  i = 1
  lines = f.readlines()
  f.close()
  total = len(lines)
  
  for url in lines:
    url = url.strip()
    if not len(url):
      continue
    
    print('Reading ' + str(i) + '/' + str(total) + ' [' + url + ']')
    i += 1
    
    headers = {
      'User-Agent': "Magic Browser",
      'Cookie': 'new_ug_exp=25; lang=en'
    }
    
    req = urllib.request.Request(url, headers=headers)
    resp = urllib.request.urlopen(req)
    content = resp.read()
    content = content.decode(resp.info().get_param('charset') or 'utf-8')
    content = content[1:-1]
    content = json.loads(content)
    content = content['info']['tabs']
    
    d = pq(content)
    rows = d('.b-table--body .tr')
    for j in range(0, rows.length):
      row = rows.eq(j)
      band_name = row.find('.td').eq(0).text()
      btn = row.find('.block-btns button:first-child')
      id = btn.attr('data-id')
      song_name = btn.attr('data-song-name')
      
      line = band_name + ' - ' + song_name + ' :: ' + id
      f_res.write(line + '\n')
      
  f_res.close()


# ---
get_ids_gp_tabs()
