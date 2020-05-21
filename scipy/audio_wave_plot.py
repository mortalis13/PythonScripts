
# Plots a waveform of an audio .wav file

import matplotlib.pyplot as plt
from scipy.io import wavfile as wav


fp = 'data/kick.wav'

rate, data = wav.read(fp)

plt.plot(data)
plt.show()
