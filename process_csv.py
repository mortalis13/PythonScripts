
# Reformat CSV files from a folder
# and create a new combined CSV


import os, re, codecs, subprocess

from modules.file_system_functions import *


def run():
  print('Start')
  
  dir_path = 'c:/all'
  res_file_path = 'c:/00_ALL.csv'
  uuid_path = 'c:/uuids.txt'
  
  res_file = codecs.open(res_file_path, encoding='utf-8', mode='w')
  uuid_file = codecs.open(uuid_path, encoding='utf-8', mode='w')
  
  files_list = get_filepaths(dir_path)
  res_file.write('path;uuid\n')
  
  total_lines = 0
  for fp in files_list:
    f = codecs.open(fp, encoding='utf-8', mode='r')
    for line in f:
      if line[0] != '\t':
        parts = line.split(';')
        
        num_lines = int((len(parts)-1) / 3)
        total_lines += num_lines
        
        doc_item = []
        for part in parts:
          if len(doc_item) == 3:
            doc_item[2] = doc_item[2].replace('/ROOT_PATH/', '')
            doc = doc_item[2] + '/' + doc_item[0] + ';' + doc_item[1] + '\n'
            res_file.write(doc)
            
            uuid_file.write(doc_item[1] + '\n')
            doc_item = []
        
          part = part.strip()
          if len(part) != 0:
            doc_item.append(part)
    
    f.close()
  
  res_file.close()
  
  print('Finish, Total lines: ' + str(total_lines))
  
  
run()
