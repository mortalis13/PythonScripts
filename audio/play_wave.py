# Plays sine wave

# pip install numpy pyaudio

import time
import numpy as np
import pyaudio

f = 50
duration = 1.0
volume = 0.5
fs = 44100

print(f'Playing {duration} s on {f}Hz')

samples = np.sin(2 * np.pi * np.arange(fs * duration) * f / fs)
samples = volume * samples.astype(np.float32)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=fs, output=True)

stream.write(samples.tobytes())
stream.stop_stream()
stream.close()

p.terminate()
