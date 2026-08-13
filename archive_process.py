# Process zip, zip-like, rar archives:
# Filter zip files containing a file name
# Unpack a RAR archive

# pip install rarfile

import codecs, os
import zipfile
import rarfile

from modules.file_system_functions import *

def find_file(file_name, folder):
  out_file = 'output.txt'
  f = codecs.open(out_file, 'w', 'utf8')
  
  zip_files = get_filepaths(folder)
  
  for zip_file in zip_files:
    try:
      zip = zipfile.ZipFile(zip_file)
    except zipfile.BadZipFile:
      continue
      
    print(zip_file)
    files = zip.namelist()
    
    if file_name in files:
      f.write(zip_file + '\n')
      f.flush()
      
  f.close()


def unpack_rar(path):
  print(f'Extracting "{path}"...\n')
  
  target_dir = os.getcwd()
  
  with rarfile.RarFile(path) as rar:
    rar.extractall(target_dir)
    extracted_files = rar.namelist()
  
  [print(x) for x in extracted_files]
  

def run():
  find_file('AndroidManifest.xml', 'c:/archives')
  unpack_rar('c:/archives/sample.rar')

run()
