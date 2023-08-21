# Generates a sine wave or extracts signal from a wav file
# and plots the waveform and spectrum after applying FFT from NumPy

# pip install numpy scipy matplotlib

import numpy as np
from scipy.io import wavfile

import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter


def plot_audio(wave_x, wave_y, fft_x, fft_y, max_freq = 0, freq_log_scale = False):
  _, (ax1, ax2) = plt.subplots(2)

  ax1.plot(wave_x, wave_y)
  ax1.set_xlabel('Time s')
  ax1.set_ylabel(f'Amplitude')
  ax1.grid(True)

  ax2.plot(fft_x, fft_y)
  ax2.set_xlabel('Frequency Hz')
  ax2.set_ylabel('Amplitude')
  
  if max_freq > 0:
    ax2.set_xlim(0, max_freq)
  
  if freq_log_scale == 1:
    ax2.set_xscale('log')
    ax2.xaxis.set_major_formatter(ScalarFormatter())
    ax2.set_xlim(None, None)
  
  plt.show()


def sine_wave(freq):
  sample_rate = 44100
  time = 0.1
  
  print(f'Sine wave and frequency plot for {freq} Hz, sample rate {sample_rate} and time {time:.2f} s')

  sample_period = 1 / sample_rate
  total_samples = int(sample_rate * time)

  x = np.arange(total_samples) * sample_period  # 1 sample each 1/sample_rate seconds
  y = np.sin(2 * np.pi * freq * x)

  xf = np.fft.fftfreq(total_samples, sample_period)  # frequencies for N samples spaced in time (1 sample each 1/sample_rate seconds)
  yf = np.abs(np.fft.fft(y))

  xf = xf[:total_samples//2]
  yf = yf[:total_samples//2]
  
  plot_audio(x, y, xf, yf, max_freq=freq * 2)


def wav_file(file):
  sample_rate, data = wavfile.read(file)
  
  channels = 1 if len(data.shape) == 1 else data.shape[1]
  total_samples = data.shape[0]
  time = total_samples / sample_rate
  sample_period = 1 / sample_rate
  sample_type = type(data[0]).__name__
  
  print(f'File {file}, sample rate: {sample_rate}, channels: {channels}, time: {time:.2f} s, total_samples: {total_samples}, sample type: {sample_type}')
  
  x = np.arange(total_samples) * sample_period
  y = data
  
  xf = np.fft.fftfreq(total_samples, sample_period)
  yf = np.abs(np.fft.fft(y))

  xf = xf[:total_samples//2]
  yf = yf[:total_samples//2]
  
  plot_audio(x, y, xf, yf)


# sine_wave(220)
wav_file('../data/kick.wav')
