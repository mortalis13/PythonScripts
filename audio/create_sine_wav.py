# Write sine wave to a wav file

# pip install numpy scipy

import numpy as np
from scipy.io import wavfile


frequency = 440
gain = 0.5
sampleRate = 44100
length = 1


def write_wav_float():
  t = np.linspace(0, length, sampleRate * length)
  data = gain * np.sin(2 * np.pi * frequency * t)
  wavfile.write(f'sine_{frequency}_float.wav', sampleRate, data)


def write_wav_16bit():
  amplitude = gain * np.iinfo(np.int16).max
  t = np.linspace(start=0, stop=length, num=sampleRate * length)
  data = amplitude * np.sin(2 * np.pi * frequency * t)
  data = data.astype(np.int16)
  wavfile.write(f'sine_{frequency}_16bit.wav', sampleRate, data)


write_wav_float()
write_wav_16bit()
