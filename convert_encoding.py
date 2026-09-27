# Converts encodings in files inside a directory

from modules.file_system_functions import *

root = 'c:/files'
src_enc = 'cp850'
dest_enc = 'cp1251'

def convert(path, from_enc, to_enc):
  with open(path, 'r', encoding=from_enc) as f:
    text = f.read()
  
  res = text.encode(from_enc).decode(to_enc)
  
  with open(path, 'w', encoding='utf8') as f:
    f.write(res)

def run():
  files = get_filepaths_in_tree(root)
  
  for file in files:
    convert(file, src_enc, dest_enc)

run()
