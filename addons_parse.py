# Parses Firefox addons pages and extracts direct download links for .xpi files
# Used in the 'addons_download.py' script

import os, re, codecs, subprocess
import shutil, stat, errno, sys, http

from modules.file_system_functions import *
from modules.general_functions import *

from pyquery import PyQuery as pq
from lxml import etree
import requests


headers = {
  'User-Agent': "Magic Browser",
  'Cookie': 'new_ug_exp=25; lang=en'
}

addon_urls_fp = 'e:/Documents/addons.txt'
addon_install_urls = 'e:/Documents/addons-download.txt'
pages_count = 72


def get_addon_urls():
  url_tmpl = 'https://addons.mozilla.org/en-US/android/search/?category=user-interface&page={0}&sort=updated&type=extension'
  base_url = 'https://addons.mozilla.org'
  
  f = codecs.open(addon_urls_fp, 'a', 'utf8')
  
  for i in range(1, pages_count):
    url = url_tmpl.format(i)
  
    req = requests.get(url)
    d = pq(req.text)
    
    links = d('.SearchResult-link')
    for j in range(0, links.length):
      link = links.eq(j)
      link = link.attr('href')
      link = base_url + link
      f.write(link + '\n')
      f.flush()
    
  f.close()
  
  
def get_addon_downloads():
  f_urls = codecs.open(addon_urls_fp, 'r', 'utf8')
  lines_urls = f_urls.readlines()
  f_urls.close()
  
  f = codecs.open(addon_install_urls, 'w', 'utf8')
  
  i = 0
  for url in lines_urls:
    try:
      url = url.strip()
      if not len(url):
        continue
      
      req = requests.get(url)
      d = pq(req.text)
      
      links = d('.InstallButton-button')
      link = links.eq(0)
      link = link.attr('href')
      f.write(link + '\n')
      f.flush()
    
      i += 1
      if i%100 == 0:
        print('--processed ' + str(i))
    except:
      print('Exception-' + url)
    
  f.close()


# ---
get_addon_urls()
# get_addon_downloads()
