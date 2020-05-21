
# Convert russian encodings in files inside a diectory 'd'

import os, re, codecs, subprocess
import shutil, stat, errno, sys

from modules.file_system_functions import *
from modules.general_functions import *


def run():
  d = 'c:/tools/rtr-vst'
  
  files = get_filepaths_in_tree(d)
  
  for fp in files:
    f = codecs.open(fp, encoding='cp1252', mode='r')
    text = f.read()
    f.close()
    
    # res=str.encode('cp850').decode('cp866')
    res=text.encode('cp1252').decode('cp1251')
    
    f = codecs.open(fp, encoding='utf8', mode='w')
    f.write(res)
    f.close()


run()
