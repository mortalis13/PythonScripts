# Edits mp3 tags for multiple files
# pip install eyed3

import eyed3

files = """
c:/file1.mp3
c:/file2.mp3
"""
titles = """
title1
title2
"""
artist = """
artist1
"""

files = list(filter(None, files.split('\n')))
titles = list(filter(None, titles.split('\n')))
artist = artist.strip()

def set_titles(artist):
  if len(files) != len(titles):
    print('files and titles have different size')
    return
  
  saved = 0
  for a in range(len(files)):
    f_path = files[a]
    title = titles[a]
    print(f_path)
    print('    => '+title)
    
    a_file = eyed3.load(f_path)
    if not a_file.tag:
      a_file.initTag()
    
    a_file.tag.title = title
    if artist:
      a_file.tag.artist = artist
    
    try:
      a_file.tag.save()
      saved += 1
    except UnicodeEncodeError as er:
      print(f'>>>>>>>>>>>[ERROR]: {er}<<<<<<<<<<<<')
    print()
  print(f'>>> saved: {saved}/{len(files)}')
  
    
def set_artist(artist):
  saved = 0
  for a in range(len(files)):
    f_path = files[a]
    print(f_path)
    
    a_file = eyed3.load(f_path)
    if not a_file.tag:
      a_file.initTag()
    
    a_file.tag.artist = artist
    
    try:
      a_file.tag.save()
      saved += 1
    except UnicodeEncodeError as er:
      print(f'>>>>>>>>>>>[ERROR]: {er}<<<<<<<<<<<<')
    print()
  print(f'>>> saved: {saved}/{len(files)}')

# set_artist(artist)
set_titles(artist)
print('-------------')
