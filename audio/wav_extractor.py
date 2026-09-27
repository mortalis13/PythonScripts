# Extracts WAV audio data from a binary file
# Can be used with game resource files, 
# where WAV audio is packed directly into binary files
# (like in Overlord game .pvp files)

# The strcture of a WAV file is 'RIFF [header] data [data_size][audio_data (data_size bytes)]'
# The script finds the 'RIFF' header, then the 'data' string,
# [data_size] (4B) in little-endian
# and just copies the next [data_size] bytes to a new file

# Input data:
#   files -> array of paths to binary files
#   out_dir -> path to the output folder
# Paths can be absolute (c:\folder...) or relative to the script location
# The output WAV files are named according to the pattern 'audio_001.wav'

import os

files = [
  '../data/MinionVoiceData_ENGLISH.pvp',
]
out_dir = '../data/wavs'


def write_wav(source_file, out_path):
  print(os.path.basename(out_path))
  
  out_file = open(out_path, 'wb')
  out_file.write(b'RIFF')
  
  finder = b'    '
  while True:
    b = source_file.read(1)
    out_file.write(b)
    
    finder += b
    finder = finder[1:]
    if finder == b'data':
      size_b = source_file.read(4)
      out_file.write(size_b)
      
      datasize = int.from_bytes(size_b, 'little')
      wav_data = source_file.read(datasize)
      out_file.write(wav_data)
      break
  out_file.close()


def extract_audio(path, out_dir):
  print(f'Extracting audio from "{path}"\n')
  f = open(path, 'rb')
  
  out_dir += '/' + os.path.splitext(os.path.basename(path))[0] + '/'
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
  for file in files:
    extract_audio(file, out_dir)


run()
