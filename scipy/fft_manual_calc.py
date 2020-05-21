
# Manual calculation of FFT using basic formulas
# Prints frequency bands (bins) and corresponding magnitudes
# as well as the calculated magnitude for the selected frequency value (FR)


import scipy.io.wavfile as wavfile
import scipy
import scipy.fftpack
from scipy.signal.windows import *
import numpy as np
from matplotlib import pyplot as plt

import math, codecs
import cmath

from imp.sine_440_hex import *


def run():
  MAXS = 32768
  FS = 44100
  
  FR = 440.0
  N = 1024
  
  M = N
  M = 20
  
  ndata = np.array(data_440)
  ndata = ndata / MAXS
  ndata = ndata[:N]
  
  
  # Magnitude for exact frequency (FR) in Hz
  # Formula: SUM[x(n) * exp(-2pi*i*w*n)], where w - the frequency, i - imaginary unit
  # the SUM argument is complex number in polar coodinates (z = r*exp(-i*f))
  # w = k/N
  # formula for frequency in Hz: FR = k*FS/N
  # having a frequency FR get the k index (the 'band' index that corresponds to the sought frequency)
  # (in this calculation it will be a fraction in most of cases, so it's situated between discrete bands limits)
  
  k = FR * N / FS         # for 440, 1024, 44100: k = 10.2167 (between bands 10 and 11)
  dsum = complex(0, 0)
  for n in range(0, N):
    val = cmath.rect(ndata[n], -2*math.pi * n * k/N)
    dsum += val
  
  print('--%.2f Hz--'%FR)
  print(dsum)
  print(abs(dsum))
  print()

  
  # Get magnitudes for first M bands (each FS/N Hz wide)
  # The same formula but for discrete 'k' values
  fft_data = []
  for k in range(0, M):
    dsum = complex(0, 0)
    for n in range(0, N):
      val = cmath.rect(ndata[n], -2*math.pi * n * k/N)
      dsum += val
    fft_data.append(abs(dsum))
  
  freq_width = FS/N
  freq = 0
  for d in fft_data:
    print('%.2f Hz - %f'%(freq, d))
    freq += freq_width
  

# ---
run()
