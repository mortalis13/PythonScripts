# Get random album from a folder (also scans subfolders)
# and copy it to another directory

import random, subprocess, shutil

from modules.file_system_functions import *


rd = 'j:/Music/Metal'
copy_to = 'e:/Documents/audio'

# CHCP 65001

def run():
  print('start')
  
  all_albums = []
  
  dirs = get_dirpaths(rd)
  for d in dirs:
    albums = get_dirpaths(d)
    for album_path in albums:
      album_files = get_filepaths_in_tree_ext(album_path, 'mp3')
      if len(album_files):
        all_albums.append(album_path)

  album_id = random.randint(0, len(all_albums)-1)
  
  album_path = all_albums[album_id]
  album_name = os.path.basename(album_path)
  
  # open in explorer
  # subprocess.Popen(r'explorer /select,"' + album_path + '"')
  
  # copy album
  album_name = 'Album_' + str(album_id)
  folder_src = album_path
  folder_dest = copy_to + '/' + album_name
  shutil.copytree(folder_src, folder_dest)

run()
