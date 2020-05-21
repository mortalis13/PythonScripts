
import os, re


def regex_search(text, pat, group=False, match_case=False):
  match = re.search(pat, text)
  if not match_case:
    match = re.search(pat, text, re.I)
    
  if match:
    res = match.group(group)
    return res

def regex_search_all_groups(text, pat, match_case=False):
  match = re.search(pat, text)
  if not match_case:
    match = re.search(pat, text, re.I)
    
  res = ''
  if match:
    for group in match.groups():
      res += group
    return res

def regex_match(text, pat, group=False, match_case=False):
  match = re.search(pat, text)
  if not match_case:
    match = re.search(pat, text, re.I)
    
  if match:
    return True
        
  return False

def regex_replace(text, pat, re_repl_func):
  res = re.sub(pat, re_repl_func, text)
  return res
  
def re_camel_func(match):
  return match.group(1).upper()

def title_lowercase_first(text):
  return text[0].lower() + text[1:]
  
def title_uppercase_first(text):
  return text[0].upper() + text[1:]

def swap_case_first_letter(txt):
  return txt[0].swapcase() + txt[1:]

def normalize_filename(val):
  remove_symbols = [':', '\"', '?', '*', '¿', '¡']
  dash_symbols = ['<', '>', '/', '\\', '|']
  
  for sym in remove_symbols:
    val = val.replace(sym, '')
  for sym in dash_symbols:
    val = val.replace(sym, '-')
    
  return val
  