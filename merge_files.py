# Combines text files from a folder

import codecs

from modules.file_system_functions import *

path = 'c:/logs'
result = 'c:/merged.txt'

def merge_files(files_list, out_file):
  outfile = codecs.open(out_file, encoding='utf-8', mode='w')

  for file in files_list:
    f = codecs.open(file, encoding='utf-8', mode='r')
    outfile.write(f.read())
    f.close()

  outfile.close()

def run():
    files = get_filepaths(path)
    merge_files(files, result)

run()
