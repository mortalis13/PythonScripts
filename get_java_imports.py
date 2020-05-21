
# Extract a list of Java 'import' statements
# from all .java files in a folder and its subfolders


import os, re, codecs, subprocess, time, random
import shutil, stat, errno, sys, ssl, traceback

from modules.file_system_functions import *
from modules.general_functions import *

import chardet


def run():
  fpout = 'e:/Documents/java_imports.txt'
  fout = codecs.open(fpout, 'w', 'utf8')
  
  d = 'e:/Documents/code/projects'
  fs = get_filepaths_in_tree_ext(d, 'java')
  
  re_pat_import = 'import (.+)?;'
  
  for fp in fs:
    try:
      fp = '\\\\?\\' + fp
      
      enc = 'utf8'
      opts = chardet.detect(open(fp, "rb").read())
      enc = opts['encoding']
      
      f = codecs.open(fp, 'r', enc)
      text = f.read()
      f.close()
      
      imports_list = re.findall(re_pat_import, text)
      imports = ''
      for import_item in imports_list:
        imports += import_item + '\n'
      
      fout.write(imports + '\n\n')
      fout.flush()
    except:
      print('\n-- Read Exception: ' + fp + '\n')
      traceback.print_exc()
    
  fout.close()
  
  
run()
