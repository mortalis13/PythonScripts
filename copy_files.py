# Copies files from multiple folders to single folder

import os
import shutil

source = [
  'c:/project1',
  'c:/project2',
  'c:/project3',
]

output = 'c:/result'

def copy_files(folder_src, folder_dest):
  ignore = shutil.ignore_patterns('.svn', 'target', '.metadata')
  shutil.copytree(folder_src, folder_dest, ignore=ignore)

def run():
  for src in source:
    dest = os.path.join(output, os.path.basename(src))
    
    src = os.path.normpath(src)
    dest = os.path.normpath(dest)
    
    dest = '\\\\?\\' + dest
    copy_files(src, dest)

run()
