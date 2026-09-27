# Combines text files from a folder

from modules.file_system_functions import *

path = 'c:/logs'
result = 'c:/merged.txt'

def merge_files(files_list, out_file):
  with open(out_file, 'w', encoding='utf-8') as outfile:
    for file in files_list:
      with open(file, 'r', encoding='utf-8') as f:
        outfile.write(f.read())

def run():
  files = get_filepaths(path)
  merge_files(files, result)

run()
