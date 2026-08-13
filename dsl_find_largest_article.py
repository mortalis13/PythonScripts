# Finds artcle with max body size in a DSL dictionary

import codecs

def run():
  fp = 'data/EsEn_Vox_School.dsl'
  f = codecs.open(fp, 'r', 'utf16')
  
  i = 1
  maxLine = 0
  maxLen = 0
  
  limitLine = 3006
  
  chars_count = 0
  wordLine = i
  
  for line in f:
    if i == limitLine:
      break
    if line[0] != '\t' and line[0] != ' ':
      if chars_count > maxLen:
        maxLen = chars_count
        maxLine = wordLine
      
      chars_count = 0
      wordLine = i
    else:
      chars_count += len(line)
    i += 1
    
  f.close()
  print(maxLine)


run()
