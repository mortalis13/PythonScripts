# Retreives author and subject metadata from PDF files
# and renames files according to a pattern

# pip install pdfminer

import os
import sys

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

from modules.file_system_functions import *

path = 'c:/pdfs/'


def get_pdf_author_subject(path):
  f = open(path, 'rb')
  parser = PDFParser(f)
  doc = PDFDocument(parser)
  doc_info = doc.info

  enc = 'utf8'

  try:
    author = doc_info[0]['Author'].decode(enc)
    subject = doc_info[0]['Subject'].decode(enc)
  except:
    print('Exception getting info field: ' + path)
    return False

  res = author + ' - ' + subject

  f.close()
  return res


def run():
  files = get_filepaths_in_tree_ext(path, 'pdf')

  for file in files:
    subject = get_pdf_author_subject(file)
    if not subject:
      continue

    subject = subject.strip()

    to_name = normalize_filename(subject)
    dir_path = os.path.dirname(file)
    to_name = dir_path + '/' + to_name + '.pdf'

    try:
      if os.path.exists(to_name):
        to_name = to_name[:-4] + '_1' + '.pdf'
      os.rename(file, to_name)

    except:
      msg = "Rename error:\n{0}\n{1}"
      msg = msg.format(sys.exc_info()[0], sys.exc_info()[1])
      print(msg)


run()
