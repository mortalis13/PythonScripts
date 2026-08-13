# Gets a random album from a folder and copies it to another folder

import random, shutil

from modules.file_system_functions import *

path = 'c:/music'
dest = 'c:/playlist'

def run():
  all_albums = []

  bands = get_dirpaths(path)
  for band in bands:
    albums = get_dirpaths(band)

    for album in albums:
      album_files = get_filepaths_in_tree_ext(album, 'mp3')
      if len(album_files):
        all_albums.append(album)

  album_id = random.randint(0, len(all_albums) - 1)

  album_path = all_albums[album_id]
  album_name = os.path.basename(album_path)

  shutil.copytree(album_path, os.path.join(dest, album_name))

run()
