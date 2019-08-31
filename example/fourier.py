#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 16:27:43 2019

@author: jasonahchuen
"""

import matplotlib.pyplot as plt
import math
import pandas as pd
import numpy as np
from scipy.signal import butter, lfilter, freqz

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

if __name__ == '__main__':
    
    #logarithm = lambda t: math.log(t, 2)
    #logarithm_func = np.vectorize(logarithm)
    
    
    
    # Sample rate and desired cutoff frequencies (in Hz).
    #fs = 5000.0
    #lowcut = 1000
    #highcut = 2000
    fields = ['Current1', 'Current2', 'Current3', 'Current4']
    signal = pd.read_csv("test5.csv", skipinitialspace = True, usecols = fields)
    
    
    #plotting original graph for current 1
    signal1 = signal.Current1
    sd1 = np.std(signal1)
    
    #plt.figure(1, figsize = [10,10], dpi=300)
    plt.figure(1)
    plt.plot(signal1)
    
    #plotting fourier graph
    res = np.fft.fft(signal1)
    nsamples = 250
    sample_interval = 63995e-6
    xf = np.linspace(0.0, 1.0/(2.0*sample_interval), nsamples//2)
    #plt.figure(2, figsize = [10,10], dpi=300)
    plt.figure(2)
    plt.plot(xf, np.abs(res[0:nsamples//2]), 'bo')
    
    #from scipy.fftpack import fft
    #N = 1000
    #T = 1.0/2000
    #x = np.linspace(0.0, N*T, N)
    #y = signal1
    #res = fft(y)
    #xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
    #import matplotlib.pyplot as plt
    #plt.plot(xf, 2.0/N * np.abs(res[0:N//2]))
    #plt.grid()
    #plt.show()
    
    
    #plotting logarithm graph
    logarithm_signal = np.log2(np.abs(res[0:nsamples//2]))
    
    logarithm_x = np.log10(xf)
    plt.figure(3)
    plt.plot(xf, logarithm_signal)
    
    plt.figure(4)
    plt.plot(logarithm_x, logarithm_signal)
    
    #Finding frequency of main harmonic
    new_amp = list(np.abs(res[0:nsamples//2]))
    new_amp.remove(max(new_amp))
    amp_main = max(new_amp)
    print(amp_main)
    f_main = xf[new_amp.index(amp_main) + 1]
    print(f_main)
    
    ################################################################
    
    #plotting original graph for current 3
    signal3 = signal['Current3']
    
    sd3 = np.std(signal3)
    
    #plt.figure(1, figsize = [10,10], dpi=300)
    plt.figure(1)
    plt.plot(signal3)
    
    #plotting fourier graph
    res3 = np.fft.fft(signal3)
    xf3 = np.linspace(0.0, 1.0/(2.0*sample_interval), nsamples//2)
    #plt.figure(2, figsize = [10,10], dpi=300)
    plt.figure(2)
    plt.plot(xf3, np.abs(res3[0:nsamples//2]), 'bo')
    
    
    
    #plotting logarithm graph
    logarithm_signal3 = np.log2(np.abs(res3[0:nsamples//2]))
    
    logarithm_x3 = np.log10(xf3)
    plt.figure(3)
    plt.plot(xf3, logarithm_signal3)
    
    plt.figure(4)
    plt.plot(logarithm_x3, logarithm_signal3)
    
    ###############################################################
    
    signal2 = signal['Current2']
    sd2 = np.std(signal2)
    
    signal4 = signal['Current4']
    sd4 = np.std(signal4)
    
    # Saving data as csv file
    df = pd.DataFrame({"Freq1" : xf, "Amplitude1" : np.abs(res[0:nsamples//2]), "Log freq1" : logarithm_x, "Log amplitude1" : logarithm_signal,
                       "Freq2" : xf3, "Amplitude2" : np.abs(res3[0:nsamples//2]), "Log freq2" : logarithm_x3, "Log amplitude2" : logarithm_signal3,
                       "s.d1" : sd1, "s.d2" : sd2, "s.d3" : sd3, "s.d4" : sd4, "f": f_main, "amp": amp_main})
    df.to_csv('test.csv')