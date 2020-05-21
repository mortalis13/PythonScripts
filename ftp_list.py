
# Write list of files/folders in a FTP directory
# (directly in a folder or recursively get subtree)
# Tries to convert names with non-UTF russian characters


import os, re, codecs, subprocess
import shutil, stat, errno, sys, traceback

import ftplib
from ftplib import FTP
import encodings.idna

from modules.file_system_functions import *
from modules.general_functions import *


ftp = FTP('host', 'user', 'pass', timeout=60)

def get_ftp_list(dir_path):
  files_list = []
  
  try:
    # ftp.cwd(dir_path)
    files_list = ftp.nlst(dir_path)
  except ftplib.error_perm:
    pass
    
  return files_list


def writeItem(f, item, pad, line_num):
  try:
    item = item.encode('latin-1').decode('utf-8')
  except:
    print('Error converting latin-1 -> utf-8: [' + str(line_num) + '], Trying to convert cp1252 -> cp1251')
    try:
      item = item.encode('cp1252').decode('cp1251')
    except:
      print('Error converting cp1252 -> cp1251: [' + str(line_num) + ']')
  
  f.write(pad + item + '\n')
  f.flush()


# Recursion
def extract_ftp_dir(root_path, f, lev):
  # if lev == 3:
  #   return
  
  pad = '    '*lev
  
  print('Scanning ' + pad + '[' + str(lev) + ']')
  
  files_list = get_ftp_list(root_path)
  
  line_num = 0
  for item in files_list:
    line_num += 1
    writeItem(f, item, pad, line_num)
    extract_ftp_dir(root_path + '/' + item, f, lev+1)

    
def write_dir_list(dir_path, out_file):
  files_list = get_ftp_list(dir_path)
  enc = 'utf8'
  f = codecs.open(out_file, 'w', encoding=enc)
  for item in files_list:
    writeItem(f, item, '', 0)
  f.close()
  

def write_dir_tree():
  dirs = [
    'dir_1',
    'dir_2',
    'dir_3',
  ]
  
  for dir_name in dirs:
    root_path = '/' + dir_name
    dir_name = dir_name.replace('/', '-')
    
    enc = 'utf8'
    fp = 'e:/ftp_' + dir_name + '.txt'
    f = codecs.open(fp, 'w', encoding=enc)
    
    extract_ftp_dir(root_path, f, 0)
    
    f.close()
    
  ftp.quit()
  

# ---
# write_dir_tree()
write_dir_list('/', 'e:/ftp_list.txt')
