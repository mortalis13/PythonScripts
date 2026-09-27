# Merges files into single PDF
# Input files are separate PDFs or images

# pip install fpdf pypdf2 Pillow

import os
import shutil

from modules.file_system_functions import *

from PyPDF2 import PdfFileWriter, PdfFileReader
from fpdf import FPDF
from PIL import Image

path = 'c:/book_pdfs'


def append_pdf(input,output):
  [output.addPage(input.getPage(page_num)) for page_num in range(input.numPages)]

def run():
  print(f'Merging files from "{path}"')
  files = get_filepaths_in_tree(path)

  result = 'result.pdf'

  parent_dir = os.path.dirname(path)
  out_pdf = os.path.join(parent_dir, result)

  name = files[0].lower()
  is_pdf = name.endswith('.pdf')
  is_img = name.endswith('.jpg') or name.endswith('.png')

  if is_pdf:
    output = PdfFileWriter()
    for file in files:
      append_pdf(PdfFileReader(open(file, "rb")), output)
    output.write(open(out_pdf, "wb"))

  elif is_img:
    tmp_dir = os.path.join(parent_dir, 'tmp')
    if not os.path.exists(tmp_dir):
      os.mkdir(tmp_dir)

    for file in files:
      img = Image.open(file)
      w, h = img.size
      xdpi, ydpi = img.info['dpi']
      print(xdpi, ydpi)

      w = w / xdpi
      h = h / ydpi

      pdf = FPDF('P', 'in', (w, h))
      pdf.add_page()
      pdf.image(file, 0, 0, w, h)

      page_pdf = os.path.join(tmp_dir, os.path.basename(file) + '.pdf')
      pdf.output(page_pdf, 'F')

    output = PdfFileWriter()
    files = get_filepaths_in_tree(tmp_dir)

    for file in files:
      append_pdf(PdfFileReader(file), output)
    output.write(open(out_pdf, "wb"))

    print(f'Merged into {result}')
    shutil.rmtree(tmp_dir)

run()
