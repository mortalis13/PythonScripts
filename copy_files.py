
# Copy Eclipse project folders from source list to a dest directory
# Ignore some folders to copy only core data


import os, re, codecs, subprocess
import shutil, stat, errno, sys

  
def copy_files(folder_src, folder_dest):
  ignore = shutil.ignore_patterns('.svn', 'target', '.metadata')
  shutil.copytree(folder_src, folder_dest, ignore=ignore)


def run():
  fsrc_list = [
    'C:/eclipse/project1',
    'C:/eclipse/project2',
    'C:/eclipse/project3',
  ]
  
  fdest_root = 'c:/eclipse-copy'
  
  for fsrc in fsrc_list:
    dest_folder_name = os.path.basename(fsrc)
    fdest = fdest_root + '/' + dest_folder_name
    
    fsrc = os.path.normpath(fsrc)
    fdest = os.path.normpath(fdest)
    
    fdest = '\\\\?\\' + fdest
  
    copy_files(fsrc, fdest)
  
  
# -------------------------

run()
