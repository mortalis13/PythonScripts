
# Retreives author and subject metadata from PDF files
# and renames files according to a pattern


import os, re, codecs, subprocess
import shutil, stat, errno, sys

from modules.file_system_functions import *
from modules.general_functions import *


def run():
  fs = [
    'e:/pdfs',
  ]
  
  for f in fs:
    files = get_filepaths_in_tree_ext(f, 'pdf')
  
    for file_path in files:
      subject = get_pdf_author_subject(file_path)
      if not subject:
        continue
      
      subject = subject.strip()
      
      to_name = normalize_filename(subject)
      dir_path = os.path.dirname(file_path)
      to_name = dir_path + '/' + to_name + '.pdf'
      
      try:
        if os.path.exists(to_name):
          to_name = to_name[:-4] + '_1' + '.pdf'
        os.rename(file_path, to_name)
      except:
        msg = "-- Rename file Exception:\n{0}\n{1}"
        msg = msg.format(sys.exc_info()[0], sys.exc_info()[1])
        print(msg)
  
  
def get_pdf_author_subject(file_path):
  fp = open(file_path, 'rb')
  parser = PDFParser(fp)
  doc = PDFDocument(parser)
  doc_info = doc.info
  
  enc = 'utf8'
  enc = 'cp1252'
  
  try:
    author = doc_info[0]['Author'].decode(enc)
    subject = doc_info[0]['Subject'].decode(enc)
  except:
    print('Exception getting info field: ' + file_path)
    return False
  
  res = author + ' - ' + subject
  
  fp.close()
  return res


# ---
run()
