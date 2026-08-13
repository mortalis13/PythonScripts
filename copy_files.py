import os
import shutil

copy_dest = 'c:/result'

source = [
  'c:/project1',
  'c:/project2',
  'c:/project3',
]

def copy_files(folder_src, folder_dest):
  ignore = shutil.ignore_patterns('.svn', 'target', '.metadata')
  shutil.copytree(folder_src, folder_dest, ignore=ignore)

def run():
  for src in source:
    dest = copy_dest + '/' + os.path.basename(src)
    
    src = os.path.normpath(src)
    dest = os.path.normpath(dest)
    
    dest = '\\\\?\\' + dest
    copy_files(src, dest)


run()
