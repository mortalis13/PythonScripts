# Writes flat file tree to a text file

import os

from_path = 'd:/'
result = 'd:/flat_tree.txt'

ext_filter = [
  'pdf',
  'chm',
  'djvu'
]

def run():
  out_file = open(result, 'w', encoding='utf-8')
  root_len = len(from_path)
  
  for root, dirs, files in os.walk(from_path):
    out_files = []
    
    for file in files:
      file_name, file_ext = os.path.splitext(file)
      if len(file_ext) != 0 and file_ext[1:].lower() in ext_filter:
        out_files.append(file)

    if len(out_files) != 0:
      root = os.path.normpath(root)
      root = root[root_len:]
      out_file.write('\n' + root + '\n')
      
      for file in out_files:
        out_file.write('    ' + file + '\n')
      
  out_file.close()

run()
