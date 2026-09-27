# Renames files in a folder by detecting full name from partial text
# For example, a file like "critical-thinking-education-students"
# would be matched to "Critical Thinking for Education Students: How to Argue, Analyse and Reflect" from a provided mapping list

# pip install rapidfuzz

import os
import re

import rapidfuzz

root = 'c:/files'
mapping_file = 'c:/map'


def normalize_filename(text):
  symbols = r'[:\"?\*¿¡<>/\\|]'
  text = re.sub(symbols, '.', text)
  
  quotes_pattern = r'[‘’‚‛“”„‟«»‹›]'
  text = re.sub(quotes_pattern, "'", text)
  
  return text

def match_file_name(file, names):
  def _normalize(text):
    text = os.path.splitext(text)[0]
    text = text.replace('-', ' ').replace('_', ' ').lower()
    text = re.sub(r'[^a-z0-9 ]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text
  
  base = _normalize(file)
  base_names = [_normalize(item) for item in names]
  
  _, score, idx = rapidfuzz.process.extractOne(base, base_names, scorer=rapidfuzz.fuzz.token_set_ratio)
  if score < 90:
    return os.path.splitext(file)[0]
  
  return names[idx]


def rename(path, full_names):
  print(f'Rename "{path}"')
  
  # Fuzzy match the file name to the list of full names
  name = os.path.basename(path)
  full_name = match_file_name(name, full_names)
  
  print(f'Full name: {full_name}')
  
  _, ext = os.path.splitext(name)
  
  new_name = normalize_filename(full_name) + ext
  new_path = os.path.join(os.path.dirname(path), new_name)
  
  if not os.path.exists(new_path):
    os.rename(path, new_path)


def run():
  with open(mapping_file, 'r', encoding='utf-8') as f:
    full_names = [line.strip() for line in f.readlines()]
  
  for file in os.listdir(root):
    rename(os.path.normpath(os.path.join(root, file)), full_names)

run()
