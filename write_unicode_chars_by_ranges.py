# Reads a list of Unicode codepoint ranges from a file
# and writes the corresponding characters to another file

def run():
  ranges = []
  
  # -- Read --
  fp = 'data/uchars-hex-ranges.txt'
  with open(fp, 'r', encoding='utf8') as f:
    for line in f:
      if len(line.strip()):
        lims = line.split(' ')
        ranges.append([int(lims[0], 16), int(lims[1], 16)])
  
  # -- Write --
  fp = 'data/uchars.txt'
  with open(fp, 'w', encoding='utf8') as f:
    for r in ranges:
      for val in range(r[0], r[1]+1):
        c = chr(val)
        f.write(c + '\n')

run()
