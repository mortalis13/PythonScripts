
# Reads a list of Unicode codepoint ranges from a file
# and writes the corresponding characters to another file


import os, re, codecs, subprocess
import time, random, requests
import shutil, stat, errno, sys, http


def run():
  ranges = []
  
  # -- read --
  fp = 'data/uchars-hex-ranges.txt'
  f = codecs.open(fp, 'r', 'utf8')
  
  for line in f:
    if len(line.strip()):
      lims = line.split(' ')
      ranges.append([int(lims[0], 16), int(lims[1], 16)])
      
  f.close()
  
  
  # -- write --
  fp = 'data/uchars.txt'
  f = codecs.open(fp, 'w', 'utf8')
  
  for r in ranges:
    for val in range(r[0], r[1]+1):
      c = chr(val)
      f.write(c + '\n')
      
  f.close()


# ---
run()
