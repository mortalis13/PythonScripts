# Plots a waveform of an audio .wav file

# pip install scipy matplotlib

import matplotlib.pyplot as plt
from scipy.io import wavfile

fp = '../data/kick.wav'

rate, data = wavfile.read(fp)

plt.plot(data)
plt.show()
