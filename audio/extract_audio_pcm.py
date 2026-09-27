# Extracts audio samples from a .wav file
# and writes them as a Python list

# pip install scipy matplotlib

import math

import scipy.io.wavfile as wavfile

audio_path = '../data/sine_440_hz.wav'
out_file = '440_hex.py'

def run():
  rate, data = wavfile.read(audio_path)

  with open(out_file, 'w', encoding='utf-8') as f:
    f.write('data = [\n')

    for i in data:
      val = '0x%04x'%i
      if i < 0:
        val = '%05x'%i
        val = val[1:]
        val = '-0x' + val
      f.write(val + ',\n')

    f.write(']\n')

run()
