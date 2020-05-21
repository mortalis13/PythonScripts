
# Writes file tree to a text file


import os, codecs


def get_tree_list(dir):
  exts = [
    'pdf',
    'chm',
    'djvu'
  ]
  
  res_file_path = 'c:/res_tree.txt'
  res_file = codecs.open(res_file_path, encoding='utf-8', mode='w')
  
  root_len = len(dir)
  
  for root, dirs, files in os.walk(dir):
    out_files = []
    
    for file in files:
      file_name, file_ext = os.path.splitext(file)
      if len(file_ext) != 0 and file_ext[1:].lower() in exts:
        out_files.append(file)

    if len(out_files) != 0:
      root = os.path.normpath(root)
      root = root[root_len:]
      res_file.write('\n' + root + '\n')
      
      for file in out_files:
        res_file.write('    ' + file + '\n')
      
  res_file.close()
  
  print('Finish')


# ---
f = 'g:/books'
get_tree_list(f)
