# Batch downloader for guitar tabs from ultimate-guitar.com
# Needs text files with direct tabs urls generated in a separate script
# Performs downloads by parts

import os, re, codecs, subprocess
import time, random
import shutil, stat, errno, sys, http

from modules.file_system_functions import *
from modules.general_functions import *

import urllib.request
import requests

# attachment; filename="Falkenbach - As Long As Winds Will Blow (guitar pro).gp5"; filename*=utf-8''Falkenbach%20-%20As%20Long%20As%20Winds%20Will%20Blow%20%28guitar%20pro%29.gp5


# -----------------------------------------------------

http_addr = '103.8.235.94:80'
https_addr = '52.174.252.85:8080'

proxies = {
  "http": "http://" + http_addr,
  "https": "https://" + https_addr
}

headers = {
  'User-Agent': "Magic Browser",
  'Cookie': 'new_ug_exp=25; lang=en'
}

part_ids = [1, 2, 3, 4, 5]

# -----------------------------------------------------

def run_default():
  print('Start downloading ...')
  
  base_path = 'e:/Documents/tabs_info'
  save_path_base = base_path + '/tabs_res'
  
  url_prefix = 'https://tabs.ultimate-guitar.com/tab/download?id='
  
  for part_id in part_ids:
    part_id = str(part_id)
    
    print('\nStarting part ' + part_id + ' [' + time.strftime("%H:%M:%S", time.gmtime()) + ']\n-----------')
    
    fp = base_path + '/tab_ids_' + part_id + '.txt'
    f = codecs.open(fp, 'r', 'utf-8')
    lines = f.readlines()
    f.close()
    
    fp_log = base_path + '/logs/log_' + part_id + '.txt'
    fp_error_log = base_path + '/logs/error_log_' + part_id + '.txt'
    
    if os.path.exists(fp_error_log) and os.stat(fp_error_log).st_size != 0:
      f_error_log = codecs.open(fp_error_log, 'r', 'utf-8')
      lines = f_error_log.readlines()
      f_error_log.close()
      print('Processing unfinished downloads for the part, total [' + str(len(lines)) + ']')
    
    f_log = codecs.open(fp_log, 'w', 'utf-8')
    f_error_log = codecs.open(fp_error_log, 'w', 'utf-8')
    
    save_path = save_path_base + '/' + 'tabs_' + part_id
    if not os.path.exists(save_path):
      os.mkdir(save_path)
    
    i = 1
    total = len(lines)
    
    for id in lines:
      id = id.strip()
      if not len(id):
        continue
        
      url = url_prefix + id
      
      try:
        req = requests.get(url, headers=headers)
          
        req_headers = req.headers
        content = req.content
        
        fn_search = 'filename='
        res_filename = ''
        
        content_disposition = req_headers['Content-Disposition']
        if len(content_disposition):
          parts = content_disposition.split('; ')
          for part in parts:
            if part.find(fn_search) != -1:
              res_filename = part[len(fn_search):]
              break
        res_filename = res_filename.replace('"', '')
        res_filename = normalize_filename(res_filename)
        
        if len(res_filename):
          fp = save_path + '/' + res_filename
          fp = generate_next_filename(fp)
          f = codecs.open(fp, 'wb')
          f.write(content)
          f.close()
          
        f_log.write(str(id) + ' :: ' + res_filename + '\n')
        f_log.flush()
        
        time.sleep(random.uniform(0.5,1))
      except:
        msg = "-- Save Exception: {0}\n{1}\n{2}"
        msg = msg.format(str(id), sys.exc_info()[0], sys.exc_info()[1])
        print('\n' + msg + '\n')
        f_error_log.write(str(id) + '\n')
        f_error_log.flush()
        
      if i == 1:
        print('1 processed')
      if i%50 == 0:
        print(str(i) + ' processed')
      i += 1
    
    print('----------\nEnd part ' + part_id + ' [' + time.strftime("%H:%M:%S", time.gmtime()) + ']')
    
    f_log.close()
    f_error_log.close()
  # // for part_id
    
  print('End downloading ...')
  
  
# ---
run_default()
