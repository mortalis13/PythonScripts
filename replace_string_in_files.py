
# Replaces a string in all files in a folder

import os, re, codecs

from modules.file_system_functions import *


def run():
  src_dir = "e:/Documents/src"
  ext = ''
  src_str = "org.apache.commons.logging.Log"
  dest_str = "org.slf4j.Logger"
  
  exclude_dirs = [
    '.svn',
    'target'
  ]
  
  replaced = 0
  
  if len(ext) == 0:
    flist = get_filepaths_in_tree_filter_dirs(src_dir, exclude_dirs)
  else:
    flist = get_filepaths_in_tree_ext_filter_dirs(src_dir, ext, exclude_dirs)
  
  for file_path in flist:
    res = replace_in_file(file_path, src_str, dest_str)
    if res:
      replaced += 1
  
  total = len(flist)
  
  print('\nFinish. Replaced ' + str(replaced) + '/' + str(total))


def replace_in_file(file_path, src_str, dest_str):
  file = codecs.open(file_path, encoding='utf-8', mode='r')
  doc = file.read()
  res = doc.replace(src_str, dest_str)
  file.close()
  
  file = codecs.open(file_path, encoding='utf-8', mode='w')
  file.write(res)
  file.close()
  
  return True


# ---
run()
