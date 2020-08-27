# Write names of zip files containing 'manifest.json' file
# Used for XPI files (which are zip-like archives and Firefox addon files)

import re, codecs, os
import zipfile

from modules.file_system_functions import *
from modules.general_functions import *

  
def run():
  manifest_file = 'manifest.json'
  
  fp = 'e:/webext-android.txt'
  f = codecs.open(fp, 'w', 'utf8')
  
  dp = 'e:/XPI/_all/android'
  zip_files = get_filepaths(dp)
  
  for zip_file in zip_files:
    print(zip_file)
    zip = zipfile.ZipFile(zip_file)
    files = zip.namelist()
    
    if manifest_file in files:
      f.write(zip_file + '\n')
      f.flush()
      
  f.close()
  
  
run()
