
# Gets dictionary headwords from a list of DSL files
# Headwords are not indented with tabs/spaces (as article bodies are)


import os, re, codecs, subprocess
import time, random, requests
import shutil, stat, errno, sys, http

from modules.file_system_functions import *
from modules.general_functions import *


def run():
  fl = [
    'data/EsEn_Vox_School.dsl',
  ]
  
  f = codecs.open('data/dsl_headwords.txt', 'w', 'utf8')
  
  for i in fl:
    print('reading: ' + i)
    fr = codecs.open(i, 'r', 'utf_16_le')
    # lines = fr.readlines()
    
    for line in fr:
      if line[0] != ' ' and line[0] != '\t' and line[0] != '#' and not '#NAME' in line and len(line.strip()):
        f.write(line)
        
    fr.close()
  
  f.close()


# ---
run()
