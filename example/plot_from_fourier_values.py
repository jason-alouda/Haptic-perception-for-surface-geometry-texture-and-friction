#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 17:09:37 2019
This file simply plots grahs produced from a given set of frequencies and corresponding amplitudes

@author: jasonahchuen
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
from fourier2 import make_signal

fields = ['freq', 'dif']
signal = pd.read_csv("scans/fourier_dif.csv", skipinitialspace = True, usecols = fields).dropna()

freqs = signal.freq
amps = signal.dif

t, y = make_signal(freqs, amps, np.zeros(len(freqs)), 0, 16 ,100)
        
plt.plot(t, y, 'r--')
plt.show()