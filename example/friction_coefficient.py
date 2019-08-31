#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 11:27:26 2019

@author: jasonahchuen


Plotting graph of current 1 against time

Find the peaks on the graphs. Take only peaks where slipping just occurs, hence friction coefficient can be found by dividing the
horizontal force by the normal foce on the arm

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

normal_force = 30

scan = pd.read_csv('scan.csv', skipinitialspace = True)
scan = scan.sort_values(['p1'])
 

normalized = pd.DataFrame(columns=['p1', 'c1'])
last_x = 0

for _, row in scan.iterrows():
  if(row.loc['p1'] == last_x):
    continue
  last_x = row.loc['p1']
  normalized = normalized.append({'p1': row.loc['p1'], 'c1': scan.loc[scan['p1'] == row.loc['p1'], 'c1'].mean()}, ignore_index=True)

from scipy.signal import find_peaks

w = normalized['c1']
plt.plot(w)
peaks, properties = find_peaks(w, height=0)
plt.ylabel("Horizontal torque (mA)")
plt.xlabel("Horizontal position")
plt.plot(peaks, w[peaks], "x")
plt.savefig("friction.png")

#print(properties['peak_heights'])
horizontal_force = np.average(properties['peak_heights'])

#print(horizontal_force)

friction_coefficient = horizontal_force/normal_force


print("Approximate friction coefficient is %f" % friction_coefficient)
