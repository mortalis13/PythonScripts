# Merges files into 1 PDF
# 'd' - directory with files
# Input files are separate PDFs or images

# -- pip install fpdf
# -- pip install pypdf2
# -- pip install Pillow


import os, re, codecs, subprocess
import shutil, stat, errno, sys
from io import StringIO
from io import BytesIO

from modules.file_system_functions import *
from modules.general_functions import *

from PyPDF2 import PdfFileWriter, PdfFileReader

from fpdf import FPDF

from PIL import Image


def append_pdf(input,output):
  [output.addPage(input.getPage(page_num)) for page_num in range(input.numPages)]

    
def run():
  d = 'e:/Documents/Book_PDF'
  files = get_filepaths_in_tree(d)
  
  parent_dir = os.path.dirname(d) + '/'
  out_pdf = parent_dir + 'res.pdf'
  
  fname = files[0].lower()
  is_pdf = fname.endswith('.pdf')
  is_img = fname.endswith('.jpg') or fname.endswith('.png')
  
  if is_pdf:
    output = PdfFileWriter()
    for f in files:
      append_pdf(PdfFileReader(open(f, "rb")), output)
    output.write(open(out_pdf, "wb"))
  elif is_img:
    tmp_dir = parent_dir + 'tmp/'
    if not os.path.exists(tmp_dir):
      os.mkdir(tmp_dir)
    
    for f in files:
      img = Image.open(f)
      w, h = img.size
      xdpi, ydpi = img.info['dpi']
      print(xdpi, ydpi)
      w = w/xdpi
      h = h/ydpi
      
      pdf = FPDF('P', 'in', (w, h))
      pdf.add_page()
      pdf.image(f,0,0,w,h)
      
      page_pdf = tmp_dir + os.path.basename(f) + '.pdf'
      pdf.output(page_pdf, 'F')
    
    
    output = PdfFileWriter()
    files = get_filepaths_in_tree(tmp_dir)
    for f in files:
      append_pdf(PdfFileReader(f), output)
    output.write(open(out_pdf, "wb"))
    
    shutil.rmtree(tmp_dir)
    

# ---
run()
