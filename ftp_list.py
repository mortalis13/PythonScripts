# Writes list of files/folders in a FTP directory
# Tries to convert names with non-UTF cyrillic characters

import ftplib

HOST = ''
USER = ''
PASS = ''


ftp = ftplib.FTP(HOST, USER, PASS, timeout=60)

def get_ftp_list(dir_path):
  files_list = []
  
  try:
    files_list = ftp.nlst(dir_path)
  except ftplib.error_perm:
    pass
    
  return files_list


def writeItem(f, item, pad, line_num):
  try:
    item = item.encode('latin-1').decode('utf-8')
  except:
    print('Error converting latin-1 -> utf-8: [' + str(line_num) + '], Trying to convert cp1252 -> cp1251')
    try:
      item = item.encode('cp1252').decode('cp1251')
    except:
      print('Error converting cp1252 -> cp1251: [' + str(line_num) + ']')
  
  f.write(pad + item + '\n')
  f.flush()


# Recursion
def extract_ftp_dir(root_path, f, lev):
  pad = '    '*lev
  print('Scanning ' + pad + '[' + str(lev) + ']')
  
  files_list = get_ftp_list(root_path)
  
  line_num = 0
  for item in files_list:
    line_num += 1
    writeItem(f, item, pad, line_num)
    extract_ftp_dir(root_path + '/' + item, f, lev+1)

    
def write_file_tree(*paths):
  result_folder = paths[-1]
  dirs = paths[:-1]
  
  for dir_name in dirs:
    root_path = '/' + dir_name

    dir_name = 'root' if dir_name == '/' else dir_name.replace('/', '--')
    file = os.path.join(result_folder, 'ftp_' + dir_name + '.txt')
    
    with open(file, 'w', encoding='utf-8') as f:
      extract_ftp_dir(root_path, f, 0)
    
  ftp.quit()


def write_file_list(dir_path, result_folder):
  files_list = get_ftp_list(dir_path)
  
  file = os.path.basename(dir_path) or 'root'
  file = os.path.join(result_folder, 'ftp_' + file + '.txt')
  
  with open(file, 'w', encoding='utf-8') as f:
    for item in files_list:
      writeItem(f, item, '', 0)
  

def run():
  result_folder = 'c:/'
  
  write_file_tree('/', result_folder)
  write_file_tree('dir1', 'dir2', result_folder)
  
  write_file_list('/', result_folder)


run()
