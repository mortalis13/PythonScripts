# Extracts WAV audio data from binary resource files from the Overlord game
# Uses the same code as the 'wav_extractor.py' but also finds output file names
# in the .pvp files which are placed before the 'RIFF' header for each WAV block

# See the 'wav_extractor.py' for the info about the input data

# --- DATA
fps = [
  '_files/MinionVoiceData_ENGLISH.pvp'
]
out_dir = '_files/wavs'
# --------


import codecs, os

def extract_audio(fp, out_dir):
  print('..extract_audio(): {}\n'.format(fp))
  f = codecs.open(fp, 'rb')
  
  out_dir += '/' + os.path.splitext(os.path.basename(fp))[0] + '/'
  
  rifflen = 4
  finder = b'    '
  c = 0
  pos = 0
  
  # -- get RIFF positions
  riff_list = []
  while True:
    b = f.read(1)
    if not b:
      break
    
    pos += 1
    finder += b
    finder = finder[1:]
    if finder == b'RIFF':
      riff_list.append(pos-rifflen)
  
  print('items:', len(riff_list))
  
  if len(riff_list) and not os.path.exists(out_dir):
    os.makedirs(out_dir)
  
  # ---
  extracted_count = 0
  for item_pos in riff_list:
    # -- get file name
    f.seek(item_pos)
    f.read(1)
    
    wav_name = b''
    finder = b'    '
    ext_found = False
    
    while True:
      f.seek(-2, 1)
      b = f.read(1)
      
      if ext_found:
        if b == b'\x00':
          break
        wav_name = b + wav_name
      else:
        finder = b + finder
        finder = finder[:-1]
        if finder.lower() == b'.wav':
          ext_found = True
          wav_name = finder
    
    print('{}  ::  [{}]'.format(wav_name, hex(item_pos)))
    
    # -- write wav data
    if wav_name.lower().find(b'.wav') != -1:
      fo = codecs.open(out_dir + wav_name.decode(), 'wb')
      f.seek(item_pos)
      
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
      
      extracted_count += 1
      fo.close()
    else:
      print('not a WAV name')
  
  if extracted_count == len(riff_list):
    print('\n== [{}] -> All WAVs extracted: {}\n\n'.format(out_dir, extracted_count))
  else:
    print('\n== [{}] -> Missing some WAVs: extracted {} of {}\n\n'.format(extracted_count, len(riff_list)))
  
  # ---
  f.close()


def run():
  for fp in fps:
    extract_audio(fp, out_dir)
  
# ---
run()
