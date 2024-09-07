# Recursively scans a directory write to a text file the tree structure
# Set the 'from_path' and 'out_path' variables before running

import os
import codecs
import traceback


def log(msg):
  try:
    print(msg)
  except:
    pass


def run():
  from_path = 'd:/'
  out_path = 'd:/dir_tree.txt'
  error_log_path = 'd:/dir_errors.log'
  
  log(f'Scanning "{from_path}" to "{out_path}"')
  
  # ----------------------
  if not os.path.exists(os.path.dirname(out_path)):
    os.makedirs(os.path.dirname(out_path))
  
  error_log = codecs.open(error_log_path, encoding='utf-8', mode='w')
  out = codecs.open(out_path, encoding='utf-8', mode='w')
  
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
        out.write(f'{indent}[{item.name}]\n')
        out.write(f'{indent}<{dir_path}>\n')
        scan(item.path, level+1)
      
      else:
        if i < num-1:
          out.write(f'{indent}{item.name}\n')
        else:
          out.write(f'{indent[:-3]}\\  {item.name}\n')
      
      i += 1
  
  scan('\\\\?\\' + from_path)
  
  error_log.close()
  out.close()


# ---
run()
