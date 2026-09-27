# Replaces a string in all files in a folder

from modules.file_system_functions import *

path = 'c:/project'

src_str = "org.apache.commons.logging.Log"
dest_str = "org.slf4j.Logger"

exclude_dirs = [
  '.svn',
  'target'
]

def replace_in_file(file_path, src_str, dest_str):
  with open(file_path, 'r', encoding='utf-8') as file:
    doc = file.read()
  
  res = doc.replace(src_str, dest_str)

  with open(file_path, 'w', encoding='utf-8') as file:
    file.write(res)

  return True

def run():
  files = get_filepaths_in_tree_filter_dirs(path, exclude_dirs)

  replaced = 0
  for file in files:
    if replace_in_file(file, src_str, dest_str):
      replaced += 1

  total = len(files)

  print('\nFinish. Replaced ' + str(replaced) + '/' + str(total))

run()
