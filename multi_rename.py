# Renames multiple files using a naming map

import os

rename_map = {
  "from_path_1": "to_path_1",
  "from_path_2": "to_path_2",
}

def run():
  for src in rename_map:
    dest = rename_map[src]

    if os.path.exists(src):
      print('"{}" => \n"{}"\n'.format(src, dest))
      os.rename(src, dest)

run()
