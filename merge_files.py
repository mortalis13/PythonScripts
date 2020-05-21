
# Combine text files in a folder into 1 file


import os, re, codecs, subprocess

from modules.file_system_functions import *


def merge_files(files_list, out_file):
  print('Start merging')
  
  outfile = codecs.open(out_file, encoding='utf-8', mode='w')
  
  for fname in files_list:
    infile = codecs.open(fname, encoding='utf-8', mode='r')
    for line in infile:
      line = line.strip()
      outfile.write(line + '\n')
    infile.close()
  
  outfile.close()
  
  print('End')
  
  
# ---
f_list = get_filepaths('e:/logs')
out_file = 'c:/_all.txt'

merge_files(f_list, out_file)
