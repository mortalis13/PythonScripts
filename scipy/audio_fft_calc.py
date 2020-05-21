
# Calculates Fast Fourier Transform (FFT) of an audio data
# determining frequency/magnitude distribution 
# Shows graphs for linear an log frequency scales with frequency peaks in Hz
# Uses static audio data from sine_440_hex.py which is a sine wave samples at 440 Hz
# or can read a .wav file


import scipy.io.wavfile as wavfile
import scipy
import scipy.fftpack
from scipy.signal.windows import *
import numpy as np
from matplotlib import pyplot as plt

import math, codecs

from imp.sine_440_hex import *


def whamm(M):
    res = []
    for n in range(0, M):
      val = 0.54 - 0.46 * np.cos(2*np.pi * n / (M-1))
      res.append(val)
      
    return np.array(res)

def whann(M):
    res = []
    for n in range(0, M):
      val = 0.5 - 0.5 * np.cos(2*np.pi * n / (M-1))
      res.append(val)
      
    return np.array(res)


def to_file(fp, arr, N = 0, fmt = '{}'):
  if N == 0: N = len(arr)
  
  f = codecs.open(fp, encoding='utf-8', mode='w')
  for i in range(0, N):
    f.write(fmt.format(arr[i]) + '\n')
  f.close()


# --- MAIN ---
def run():
  ZERO_PAD = False
  LOAD_440_WAVE = True
  
  LIN_FREQ_FROM = 280
  LIN_FREQ_TO = 360
  
  FS = 44100
  MAXS = 32768
  
  FN0 = 2048
  FN0 = 4096
  
  # FN = 1024
  # FN = 4096
  FN = 2**15
  
  FREQ_N = FN//2
  FREQ_STEP = FS/FN
  MN = 20
  
  if LOAD_440_WAVE:
    data = data_440
  else:
    fp = 'data/kick.wav'
    fs_rate, data = wavfile.read(fp)
  
  
  # -------- FFT Calc --------
  
  ndata = np.array(data)
  ndata = ndata / MAXS
  
  if ZERO_PAD:
    w = np.ones(FN0)
    w = whamm(FN0)
    y0 = ndata[FN0:FN0*2] * w
    y = np.array([0.0]*FN)
    y[:FN0] = np.array(y0)
  else:
    w = np.ones(FN)
    # w = blackman(FN)
    # w = hann(FN)
    w = whamm(FN)
    y = ndata[:FN] * w
  
  freqs = scipy.fftpack.fftfreq(FN, 1/FS)
  mags = abs(scipy.fft(y))
  
  
  # -------- log scale frequencies --------
  pst = 24
  pen = 90
  pstep = 2
  PN = (pen - pst) // pstep
  
  mags_log = []
  freqs_pitch = [0]*PN
  ks = []
  
  p = pst
  while p <= pen:
    ktemp = []
    mag_sum = 0
    
    fr_cut_left = 440 * 2**((p-pstep/2-69)/12)
    fr_cut_right = 440 * 2**((p+pstep/2-69)/12)
    
    k_left = math.floor(fr_cut_left * FN / FS)
    k_right = math.ceil(fr_cut_right * FN / FS)
    
    for k in range(k_left, k_right+1):
      fr_k = k * FS / FN
      if fr_cut_left <= fr_k and fr_k < fr_cut_right:
        ktemp.append(k)
        val = mags[k]**2
        mag_sum += val
    ks.append(ktemp)
    
    mags_log.append(mag_sum)
    p += pstep
  
  
  # -------- print pitch-frequency table --------
  for i in range(0, PN):
    p = pst + i*pstep
    fr = 440 * 2**((p-69)/12)
    freqs_pitch[i] = fr
  
  print()
  print('Pitch -- Frequency -- Magnitude')
  for i in range(0, PN):
    p = pst + i*pstep
    text = '{:3d}  -  {:9.3f}  -  {:.3f}'.format(p, freqs_pitch[i], mags_log[i]).rstrip('0').rstrip('.')
    print(text)
  print()
  
  
  # -------- plot --------
  fr_res = np.linspace(0, PN, PN+1)
  bars_pos = np.arange(0, PN, 1)
  db_res = np.array(mags_log)
  bars_labels = []
  
  db_res = np.sqrt(db_res)
  dbfs = 20 * np.log10(db_res * 2 / np.sum(w))
  db_res = dbfs
  
  for i in range(0, PN):
    p = pst + i*pstep
    fr = 440 * 2**((p-69)/12)
    bars_labels.append(round(fr, 1))
  
    
  dbfs0 = 20 * np.log10(mags * 2 / np.sum(w))
  fr_res0 = freqs[LIN_FREQ_FROM:LIN_FREQ_TO]
  db_res0 = dbfs0[LIN_FREQ_FROM:LIN_FREQ_TO]
  
  bars_pos0 = np.arange(0, 30, 1)
  bars_labels0 = fr_res0
  
  ax1 = plt.subplot(211)
  plt.bar(fr_res0, db_res0)
  plt.grid(True)
  locs, labels = plt.xticks()
  plt.setp(labels, rotation=40)
  plt.xlabel('Frequency [Hz]')
  plt.ylabel('Amplitude [dB]')
  
  ax2 = plt.subplot(212)
  plt.bar(fr_res, db_res)
  plt.grid(True)
  locs, labels = plt.xticks()
  plt.setp(labels, rotation=40)
  plt.xlabel('Frequency [Hz]')
  plt.ylabel('Amplitude [dB]')
  ax2.set_xticks(bars_pos)
  ax2.set_xticklabels(bars_labels)
  
  mng = plt.get_current_fig_manager()
  mng.window.state('zoomed')
  plt.show()
  

# ---
run()
