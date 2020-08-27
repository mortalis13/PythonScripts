# Extracts WAV audio data from a binary file
# Can be used with game resource files, 
# where WAV audio is packed directly into binary files
# (like in Overlord game .pvp files)

# The strcture of a WAV file is 'RIFF [header] data [data_size][audio_data (data_size bytes)]'
# The script finds the 'RIFF' header, then the 'data' string,
# [data_size] (4B) in little-endian
# and just copies the next [data_size] bytes to a new file

# Input data:
#   fps -> array of paths to binary files
#   out_dir -> path to the output folder
# Paths can be absolute (c:\folder...) or relative to the script location
# The output WAV files are named according to the pattern 'audio_001.wav'

# --- DATA
fps = [
  '_files/MinionVoiceData_ENGLISH.pvp'
]
out_dir = '_files/wavs'
# --------


import codecs, os

def write_wav(f, out_path):
  print('..write_wav(): {}'.format(out_path))
  
  fo = codecs.open(out_path, 'wb')
  fo.write(b'RIFF')
  
  finder = b'    '
  while True:
    b = f.read(1)
    fo.write(b)
    
    finder += b
    finder = finder[1:]
    if finder == b'data':
      size_b = f.read(4)
      fo.write(size_b)
      
      datasize = int.from_bytes(size_b, 'little')
      wav_data = f.read(datasize)
      fo.write(wav_data)
      break
  fo.close()
  
def extract_audio(fp, out_dir):
  print('..extract_audio(): {}\n'.format(fp))
  f = codecs.open(fp, 'rb')
  
  out_dir += '/' + os.path.splitext(os.path.basename(fp))[0] + '/'
  if not os.path.exists(out_dir):
    os.makedirs(out_dir)

  finder = b'    '
  i = 1

  while True:
    b = f.read(1)
    if not b:
      break
    
    finder += b
    finder = finder[1:]
    if finder == b'RIFF':
      out_path = out_dir + 'audio_' + '{:03}'.format(i) + '.wav'
      write_wav(f, out_path)
      i += 1
  f.close()


def run():
  for fp in fps:
    extract_audio(fp, out_dir)
  
# ---
run()
