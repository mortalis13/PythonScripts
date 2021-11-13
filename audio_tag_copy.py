# Copies mp3 tags from files in one folder to the files with the same names in another folder
# pip install eyed3

import os
import eyed3

from modules.file_system_functions import *
from modules.general_functions import *


path_src = 'c:/original_files_path/'
path_dst = 'c:/new_files_path/'

path_src = os.path.normpath(path_src)
path_dst = os.path.normpath(path_dst)

src_files = get_filepaths_in_tree_ext(path_src, 'mp3')


def copy_tags(f0, f1):
  a0_file = eyed3.load(f0)
  a1_file = eyed3.load(f1)
  
  if not a0_file:
    print('[ERROR]: AudioFile None')
    return
  
  a1_file.tag = a0_file.tag
  if not a1_file.tag:
    a1_file.initTag()
  
  try:
    a1_file.tag.save()
  except UnicodeEncodeError as er:
    print('[ERROR]: files' + str(er))
  

done = 0
for f0 in src_files:
  f0_rel = f0.replace(path_src, '')
  f1 = path_dst + f0_rel
  if os.path.exists(f1):
    print(f1)
    copy_tags(f0, f1)
    done += 1

print(f'\nsource: {len(src_files)}, dest: {done}\n\n')
