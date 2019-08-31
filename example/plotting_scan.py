#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 17:17:54 2019

@author: jasonahchuen

This file is used to find the geometry of a surface, if it has been found to have a repeating geometry.
It uses first and second derivatives to find max/min points, if any, to tell whether the surface is wavy, is a crest or is a trough.

TODO: Be able to distinguish between other shapes e.g. triangles

"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def run_geometry():
    
    scan = pd.read_csv('position_scan.csv', skipinitialspace = True)
    scan = scan.sort_values(['x'])
    
    
    normalized = pd.DataFrame(columns=['x', 'y'])
    last_x = 0
    
    for _, row in scan.iterrows():
      if(row.loc['x'] == last_x):
        continue
      last_x = row.loc['x']
      normalized = normalized.append({'x': row.loc['x'], 'y': scan.loc[scan['x'] == row.loc['x'], 'y'].mean()}, ignore_index=True)
          
    normalized = normalized.dropna()
    
    from scipy import signal
    xn = normalized['y']
    t = normalized['x']
    b, a = signal.butter(3, 0.05) 
    y = signal.filtfilt(b, a, xn)
    
    #Finding first derivative of smooth signal
    first_der = np.gradient(y, normalized['x'])
    
    #x-value: x, y-value: first derivative
    turning_pts = pd.DataFrame(columns=['x', 'y'])
    
    #x-value: x, y-value: y
    real_turning_pts = pd.DataFrame(columns=['x', 'y'])
    
    for i in range(len(first_der)-1):
      if ((first_der[i] > - 0.01) and (first_der[i] < 0.01)):
        turning_pts = turning_pts.append({'x': normalized['x'][i], 'y':first_der[i]}, ignore_index=True)
        real_turning_pts = real_turning_pts.append({'x': normalized['x'][i], 'y':normalized['y'][i]}, ignore_index=True)
    
    second_der = np.gradient(turning_pts['y'], turning_pts['x']) #Finding the second derivatives at each turning pt
    
    maxima = pd.DataFrame(columns=['x', 'y'])
    minima = pd.DataFrame(columns=['x', 'y'])
    inflection = pd.DataFrame(columns=['x', 'y'])
    
    for i in range(len(second_der)-1):
      if (second_der[i] > 0):
        minima = minima.append({'x': real_turning_pts['x'][i], 'y':real_turning_pts['y'][i]}, ignore_index=True)
      elif (second_der[i] < 0):
        maxima = maxima.append({'x': real_turning_pts['x'][i], 'y':real_turning_pts['y'][i]}, ignore_index=True)
      else:
        inflection = inflection.append({'x': real_turning_pts['x'][i], 'y':real_turning_pts['y'][i]}, ignore_index=True)      
    
    
    # Plotting the graphs
    plt.figure(3)
    plt.plot(normalized['x'], normalized['y'], 'r')
    plt.plot(t, y, 'k')
    plt.plot(minima['x'], minima['y'], 'g^')
    plt.plot(maxima['x'], maxima['y'], 'r^')
    plt.plot(inflection['x'], inflection['y'], 'x')
    plt.legend(('noisy signal', 'smooth signal'), loc='best')
    plt.grid(True)
    plt.show()
    
    der_sign = pd.DataFrame(columns=['x', 'y'])
    for i1 in range(len(first_der)-1):
      if(first_der[i1] > 0):
        plt.axvspan(normalized['x'][i1], normalized['x'][i1+1], color='green', alpha=0.1)
    #     der_sign = der_sign.append({'x': normalized['x'][i1], 'y':2069}, ignore_index=True)
      else:
        plt.axvspan(normalized['x'][i1], normalized['x'][i1+1], color='red', alpha=0.1)    
    
    # Trying to guess the geometry of the surface
    
    # If the peak heights are different and the peaks spaced unevenly
    
    
        # If the peak heights are small, it is flat and rough, else it has an unven shape
    
    
    
    if (minima.count == 0):
      if (maxima.count == 0):
        print("This surface is not wavy")
      else:
        print("There is a crest on the surface")
    else:
      if (maxima.count == 0):
        print("There is a trough on the surface")
      else:
        print("This is a wavy surface")