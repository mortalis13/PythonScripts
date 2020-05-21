
# Download Fender FUSE presets with wget
# using a text file with direct links


import os, re, codecs, subprocess
from time import sleep

from modules.file_system_functions import *

# 
# wget --content-disposition --header "Cookie: fmic_session=[sessionkey]" https://fuse.fender.com/mustangv2/presets/doctorvito-1.-synth-of-legends/download/
# 

wget_path = 'c:/tools/wget.exe'

session_cookie = 'syKEjx1%2BVcEWnn4DF4pY7l6pIZzqqIVdyW1gRfDLBI7rlEpHLjusvln9p63ZztVCOYy7EK33GXZRhn5XxuA73ZGY8u6s8k7wMgufLs%2BNP1CHKXHSO8eCwzwxsoPBhrv5tGG50Z0Bi7G96YCCCRHWyOQ5BGNosaJzolypPgM4z9E8ffrOVB%2BgwSrYaaHPJOsAbh%2FV1dzdQy9beIcEzthCCDG70x5piHUQHigbq8zRF0Rx9u1d74wrBLwKO%2Fr0gThYQdhRfmAfKhMu9rgOCEDionAkjuzWmJznHKN7i5sb3EXoyX%2FaoKJk07XNP54IR3ySjGLZC5lsWzERsEDfOlTrNysDn%2F3MnDyWRpD7HveoxxxsS3DzOcH%2Bedo64azxrMs43253259c2fd9cb3ee4cf5688858f64afbf2c8bb8'

cookie_param = 'Cookie: fmic_session=' + session_cookie

def download_presets(urls_file_path):
  urls_file = codecs.open(urls_file_path, encoding='utf-8', mode='r')
  
  i = 1
  
  for url in urls_file:
    url = url.strip()
    if not len(url):
      continue
    
    url += 'download/'
    res = subprocess.run([wget_path, '--content-disposition', '--header', cookie_param, '-P', out_folder, url])
    
    print('\n\n""" ' + str(i) + ' [' + str(part_id) + ']\n\n')
    i += 1

  urls_file.close()


def run():
  fp = 'e:/links.txt'
  download_presets(fp)


run()
