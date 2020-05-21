
# Extracts audio samples from a .wav file
# and writes them as a Python list


import scipy.io.wavfile as wavfile
import math, codecs


audio_path = 'data/sine_440_hz.wav'
out_file = 'data/440_hex.py'

fs_rate, data = wavfile.read(audio_path)

f = codecs.open(out_file, encoding='utf-8', mode='w')
f.write('data = [\n')

for i in data:
  val = '0x%04x'%i
  if i < 0:
    val = '%05x'%i
    val = val[1:]
    val = '-0x' + val
  f.write(val + ',\n')

f.write(']\n')
f.close()
