# Duplicates directory structure without copying files physically
# Adds files size to the their names
# Set the 'from_path' and 'out_path' variables before running

import os, re, codecs, subprocess
import shutil, stat, errno, sys, traceback

from modules.file_system_functions import *
from modules.general_functions import *


def format_size(byte_size):
  for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
    if abs(byte_size) < 1024.0:
      return "%d%s" % (byte_size, unit)
    byte_size /= 1024.0
  return "%d%s" % (byte_size, 'Yi')


def log(msg):
  try:
    print(msg)
  except:
    pass


def run():
  from_path = 'c:/'
  out_path_root = 'd:/_dir_struct'
  error_log_path = 'd:/_dir_struct/_dir_struct_dump_errors.log'
  
  # ----------------------
  out_dir = os.path.basename(from_path)
  if not out_dir.strip():
    out_dir = os.path.dirname(from_path).replace(':', '')
    
  out_path = out_path_root + '/' + out_dir
  if not os.path.exists(out_path):
    os.makedirs(out_path)
  
  error_log = codecs.open(error_log_path, encoding='utf-8', mode='w')
  
  from_path = os.path.normpath(from_path)
  out_path_root = os.path.normpath(out_path_root)
  out_path = os.path.normpath(out_path)
  # ----------------------
  
  for root, dirs, files in os.walk(from_path):
    # if out path is inside the from path, prevent infinite-recursive walk 
    if root == out_path_root:
      dirs[:] = []
      files[:] = []
      continue
    
    if os.path.dirname(root) == from_path:
      log('-- ' + os.path.basename(root))
    if os.path.dirname(os.path.dirname(root)) == from_path:
      log('---- ' + os.path.basename(root))
    
    item_root_path = root.replace(from_path, '')
    
    for subdir in dirs:
      try:
        # prevent dest folder creation, if out path is inside the from path
        if os.path.normpath(from_path + '/' + subdir) == out_path_root:
          continue
        
        item_out_path = out_path + '/' + item_root_path + '/' + subdir
        item_out_path = os.path.normpath(item_out_path)
        
        if len(item_out_path) > 200:
          item_out_path = '\\\\?\\' + item_out_path
        
        if not os.path.exists(item_out_path):
          os.mkdir(item_out_path)
      except:
        error_log.write(root+'/'+subdir)
        error_log.write(traceback.format_exc())
        error_log.write('\n')
      
    for file in files:
      try:
        fpath = root + '/' + file
        fsize = os.stat(fpath).st_size
        size_str = format_size(fsize)
        
        fn, ext = os.path.splitext(file)
        fp = fn + '_' + size_str + ext
        
        item_out_path = out_path + '/' + item_root_path + '/' + fp
        item_out_path = os.path.normpath(item_out_path)
        
        if len(item_out_path) > 200:
          item_out_path = '\\\\?\\' + item_out_path
        
        f = open(item_out_path, 'w')
        f.close()
      except:
        error_log.write(root+'/'+file)
        error_log.write(traceback.format_exc())
        error_log.write('\n')
    
  error_log.close()
  
# ---
run()
