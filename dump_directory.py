# Recursively scans a directory and writes its structure to a text file
# Set the 'from_path' and 'out_path' variables before running

import os
import traceback

from_path = 'd:/'
result = 'd:/dir_tree.txt'


def log(msg):
  try:
    print(msg)
  except:
    pass

def run():
  error_log_path = os.path.join(os.path.dirname(result), 'errors.log')
  
  log(f'Scanning "{from_path}" to "{result}"')
  
  # ----------------------
  if not os.path.exists(os.path.dirname(result)):
    os.makedirs(os.path.dirname(result))
  
  error_log = open(error_log_path, 'w', encoding='utf-8')
  out_file = open(result, 'w', encoding='utf-8')
  
  from_path = os.path.normpath(from_path)
  # ----------------------
  
  def scan(path, level=0):
    if level == 1:
      log(os.path.basename(path))
    if level == 2:
      log('-- ' + os.path.basename(path))
    
    try:
      items = list(os.scandir(os.path.normpath(path)))
    except:
      error_log.write(path)
      error_log.write(traceback.format_exc())
      error_log.write('\n')
      return
      
    num = len(items)
    
    indent = level * '\u2502  '  # drawing vertical bar
    
    i = 0
    for item in items:
      if item.is_dir():
        dir_path = item.path.replace('\\\\?\\', '')
        out_file.write(f'{indent}[{item.name}]\n')
        out_file.write(f'{indent}<{dir_path}>\n')
        scan(item.path, level+1)
      
      else:
        if i < num-1:
          out_file.write(f'{indent}{item.name}\n')
        else:
          out_file.write(f'{indent[:-3]}\\  {item.name}\n')
      
      i += 1
  
  scan('\\\\?\\' + from_path)
  
  error_log.close()
  out_file.close()


run()
