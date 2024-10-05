
import os, re, codecs, subprocess
import shutil, stat, errno, sys, operator

from modules.general_functions import *


def get_filenames(root_dir):
  for root, dirs, files in os.walk(root_dir):
    return files

def get_dirnames(root_dir):
  for root, dirs, files in os.walk(root_dir):
    return dirs
    
def get_dirpaths(root_dir):
  res_list = []
  
  for root, dirs, files in os.walk(root_dir):
    for dirr in dirs:
      res_list.append(os.path.normpath(os.path.join(root, dirr)))
      
    return res_list
    
def get_filepaths(root_dir, group_by=None):
  files_list = []
  
  for root, dirs, files in os.walk(root_dir):
    for file in files:
      files_list.append(os.path.normpath(os.path.join(root, file)))
    
    if group_by == 'ext':
      files_list_dict = {}
      for file_item in files_list:
        name,ext = os.path.splitext(file_item)
        if not ext in files_list_dict:
          files_list_dict[ext] = []
        else:
          files_list_dict[ext].append(file_item)
      
      return files_list_dict
    
    return files_list
    
def get_filenames_ext(root_dir, ext):
  res = []
  
  for root, dirs, files in os.walk(root_dir):
    for file in files:
      file_name, file_ext = os.path.splitext(file)
      if len(file_ext) != 0 and file_ext[1:].lower() == ext:
        res.append(file)
    return res

def get_filenames_in_tree_ext(root_dir, ext):
  res = []
  
  for root, dirs, files in os.walk(root_dir):
    for file in files:
      file_name, file_ext = os.path.splitext(file)
      if len(file_ext) != 0 and file_ext[1:].lower() == ext:
        res.append(file)
        
  return res

def get_filenames_in_tree(root_dir):
  files_list = []
  
  for root, dirs, files in os.walk(root_dir):
    for file in files:
      files_list.append(file)

  return files_list

def get_full_tree(root_dir):
  files_list = []
  dirs_list = []
  
  for root, dirs, files in os.walk(root_dir):
    for file in files:
      files_list.append(os.path.normpath(os.path.join(root, file)))
    for root_dir in dirs:
      dirs_list.append(os.path.normpath(os.path.join(root, root_dir)))

  return (files_list, dirs_list)

def get_filepaths_in_tree(root_dir):
  files_list = []
  
  for root, dirs, files in os.walk(root_dir):
    for file in files:
      files_list.append(os.path.normpath(os.path.join(root, file)))

  return files_list
  
def get_filepaths_in_tree_ext(root_dir, ext):
  files_list = []
  
  for root, dirs, files in os.walk(root_dir):
    for file in files:
      file_name, file_ext = os.path.splitext(file)
      if len(file_ext) != 0 and file_ext[1:].lower() == ext:
        files_list.append(os.path.normpath(os.path.join(root, file)))

  return files_list
  
def get_filepaths_in_tree_filter_dirs(root_dir, exclude_dirs):
  files_list = []
  
  for root, dirs, files in os.walk(root_dir):
    search_in_dir = True
    for exclude_dir in exclude_dirs:
      if(os.path.basename(root) == exclude_dir):
        search_in_dir = False
    
    if not search_in_dir:
      continue
      
    for file in files:
      files_list.append(os.path.normpath(os.path.join(root, file)))

  return files_list

def get_filepaths_in_tree_ext_filter_dirs(root_dir, ext, exclude_dirs):
  files_list = []
  
  for root, dirs, files in os.walk(root_dir):
    search_in_dir = True
    for exclude_dir in exclude_dirs:
      if(os.path.basename(root) == exclude_dir):
        search_in_dir = False
    
    if not search_in_dir:
      continue
      
    for file in files:
      file_name, file_ext = os.path.splitext(file)
      if len(file_ext) != 0 and file_ext[1:].lower() == ext:
        files_list.append(os.path.normpath(os.path.join(root, file)))

  return files_list

def get_extensions_in_tree(root_dir):
  ext_list = {}
  
  for root, dirs, files in os.walk(root_dir):
    for file in files:
      ext = os.path.splitext(file)[1]
      
      if ext in ext_list:
        ext_list[ext] += 1
      else:
        ext_list[ext] = 1

  return ext_list


def remove_files(folder, remove_root):
  print('Starting to remove files in folder: ' + folder)
  
  remove_success = True
  
  for root, dirs, files in os.walk(folder, topdown=False):
    if os.path.dirname(root) == folder:
      print('Removing directory: ' + root)
    
    dir_path = ''
    
    path_sep = '\\'
    # path_sep = '/'
    
    try:
      root = os.path.normpath(root)
      root = '\\\\?\\' + root
      
      for file in files:
        file_path = root + path_sep + file
        os.chmod(file_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        os.remove(file_path)
        
      for dirr in dirs:
        dir_path = root + path_sep + dirr
        os.rmdir(dir_path)
    except:
      remove_success = False
      
      temp_files_list, temp_dirs_list = get_full_tree(dir_path)
      print()
      print(sys.exc_info()[0])
      print(sys.exc_info()[1])
      print('root:', dir_path)
      print('files:', temp_files_list)
      print('dirs:', temp_dirs_list)
      print()
      continue
  
  if remove_root and remove_success:
    if os.path.exists(folder):
      os.rmdir(folder)
  
  print('Finish Removing')
  
  return remove_success


def remove_files_from_list(files_list):
  print('Starting to remove files from list')
  
  remove_success = True
  
  count = 0
  total = len(files_list)
  
  try:
    for file_path in files_list:
      file_path = file_path.strip()
      if os.path.exists(file_path):
        os.chmod(file_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        os.remove(file_path)
        count += 1
        
      if count%100 == 0:
        print('Removed ' + str(count))
  except:
    remove_success = False
    
    print()
    print(sys.exc_info()[0])
    print(sys.exc_info()[1])
    print()
  
  print('Finish Removing, removed: ' + str(count) + '/' + str(total))
  
  return remove_success


def get_tree_list(root_dir, exts):
  root_len = len(root_dir)
  
  for root, dirs, files in os.walk(root_dir):
    out_files = []
    
    for file in files:
      file_name, file_ext = os.path.splitext(file)
      if len(file_ext) != 0 and file_ext[1:].lower() in exts:
        out_files.append(file)

    if len(out_files) != 0:
      root = os.path.normpath(root)
      root = root[root_len:]
      
      res_tree[root] = []
      
      for file in out_files:
        res_tree[root].append(file)
      
  
def write_tree_list(root_dir, exts, res_filepath):
  res_file = codecs.open(res_filepath, encoding='utf-8', mode='w')
  root_len = len(root_dir)
  
  for root, dirs, files in os.walk(root_dir):
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


def generate_next_filename(filepath, pat=None):
  if pat:
    file_dir = os.path.dirname(filepath)
    file_name = os.path.basename(filepath)
    name,ext = os.path.splitext(file_name)
    
    name_check = regex_search(name, '^(.+?)' + pat + '\d+$', 1)
    if name_check:
      filepath = file_dir + '/' + name_check + ext
  
  res_filepath = filepath
  file_exists = os.path.exists(filepath)

  counter = 2
  
  while file_exists:
    file_dir = os.path.dirname(filepath)
    file_name = os.path.basename(filepath)
    name,ext = os.path.splitext(file_name)
    file_name = name + '_' + str(counter) + ext
    counter += 1
    
    res_filepath = file_dir + '/' + file_name
    file_exists = os.path.exists(res_filepath)

  return res_filepath


def create_folder(folder_path):
  if not os.path.exists(folder_path):
    os.makedirs(folder_path)
