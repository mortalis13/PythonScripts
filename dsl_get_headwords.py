# Gets dictionary headwords from a list of DSL dictionary files
# Headwords are not indented with tabs/spaces (as article bodies are)

files = [
  'data/EsEn_Vox_School.dsl',
]

output = 'data/dsl_headwords.txt'

def run():
  result_file = open(output, 'w', encoding='utf8')
  
  for file in files:
    print('Reading: ' + file)
    with open(file, 'r', encoding='utf_16_le') as f:
      for line in f:
        if line[0] != ' ' and line[0] != '\t' and line[0] != '#' and not '#NAME' in line and len(line.strip()):
          result_file.write(line)
  
  result_file.close()

run()
