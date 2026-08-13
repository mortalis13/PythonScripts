# Extracts a list of Java 'import' statements
# from all .java files in a folder and its subfolders

# pip install chardet

import re, codecs, traceback
import chardet

from modules.file_system_functions import *


input_folder = 'c:/projects'
result = 'data/java_imports.txt'

def run():
  fout = codecs.open(result, 'w', 'utf8')
  fs = get_filepaths_in_tree_ext(input_folder, 'java')
  
  re_pat_import = 'import (.+)?;'
  
  for file in fs:
    try:
      file = '\\\\?\\' + file
      
      opts = chardet.detect(open(file, "rb").read())
      enc = opts['encoding']
      
      f = codecs.open(file, 'r', enc)
      text = f.read()
      f.close()
      
      imports_list = re.findall(re_pat_import, text)
      imports = ''
      for import_item in imports_list:
        imports += import_item + '\n'
      
      fout.write(imports + '\n\n')
      fout.flush()
    
    except:
      print('\n-- Read Exception: ' + file + '\n')
      traceback.print_exc()
    
  fout.close()
  
run()
