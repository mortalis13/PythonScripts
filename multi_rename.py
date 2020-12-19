# Renamed multiple files using a naming map

import os

rename_map = {
  "from_path_1": "to_path_1",
  "from_path_2": "to_path_2",
}

def run():
  print('== multi_rename ==')
  
  for k in rename_map:
    fin = k
    fout = rename_map[k]
    if os.path.exists(fin):
      print('"{}" => \n"{}"\n'.format(fin, fout))
      os.rename(fin, fout)
    
run()