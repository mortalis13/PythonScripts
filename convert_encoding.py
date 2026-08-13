# Converts encodings in files inside a directory

import codecs

from modules.file_system_functions import *

root = 'c:/files'

def convert(path, from_enc, to_enc):
  f = codecs.open(path, encoding=from_enc, mode='r')
  text = f.read()
  f.close()
  
  res = text.encode(from_enc).decode(to_enc)
  
  f = codecs.open(path, encoding='utf8', mode='w')
  f.write(res)
  f.close()

def run():
  files = get_filepaths_in_tree(root)
  
  for fp in files:
    convert(fp, 'cp850', 'cp1251')


run()
