# Gets dictionary headwords from a list of DSL dictionary files
# Headwords are not indented with tabs/spaces (as article bodies are)

import codecs

files = [
  'data/EsEn_Vox_School.dsl',
]

def run():
  result = codecs.open('data/dsl_headwords.txt', 'w', 'utf8')
  
  for path in files:
    print('Reading: ' + path)
    file = codecs.open(path, 'r', 'utf_16_le')
    
    for line in file:
      if line[0] != ' ' and line[0] != '\t' and line[0] != '#' and not '#NAME' in line and len(line.strip()):
        result.write(line)
        
    file.close()
  
  result.close()


run()
