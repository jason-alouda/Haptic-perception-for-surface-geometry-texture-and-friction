#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 16:32:11 2019

@author: jasonahchuen

Calculates standard deviations on all 4 joints.
Plots fourier graphs and logarithm graphs on joints 1 and 2.
Calculates frequency and amplitude of main harmonic on joint 1.

Loads KNN model and multinomial logistic regression model. 
Based on past train data, makes a prediction for present data.

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def run_analysis():

    # Ignore warnings due to division by zero
    np.seterr(divide='ignore') 
    
    # Now opening and reading scan to get fft values

    fields = ['Timestamp', 'Current1', 'Current2', 'Current3', 'Current4', 'Position1', 'Position2']
    signal = pd.read_csv("scan.csv", skipinitialspace = True, usecols = fields)
    
    #plotting original graph for current 1
    signal1 = signal.Current1
    sd1 = np.std(signal1)
    
    #plt.figure(1, figsize = [10,10], dpi=300)
    plt.figure(1)
    plt.title("Current 1 varying with time")
    plt.plot(signal1)
    
    #plotting fourier
    res = np.fft.fft(signal1)
    nsamples = 250
    sample_interval = 63995e-6
    xf = np.linspace(0.0, 1.0/(2.0*sample_interval), nsamples//2)
    #plt.figure(2, figsize = [10,10], dpi=300)
    plt.figure(2)
    plt.title("Fourier graph of current1")
    plt.ylabel("Amplitude")
    plt.xlabel("Frequency")
    plt.plot(xf, np.abs(res[0:nsamples//2]), 'bo')

    #plotting logarithm graph
    logarithm_signal = np.log2(np.abs(res[0:nsamples//2]))
    
    logarithm_x = np.log10(xf)
    #plt.figure(3)
    #plt.plot(xf, logarithm_signal)
    
    #plt.figure(4)
    #plt.plot(logarithm_x, logarithm_signal)
    
    #Finding frequency of main harmonic
    new_amp = list(np.abs(res[0:nsamples//2]))
    new_amp.remove(max(new_amp))
    amp_main = max(new_amp)
    f_main = xf[new_amp.index(amp_main) + 1]
    
    # Do NOT take the natural frequency and corresponding amplitude of system
    
    if (f_main < 0.07):
        new_amp.remove(amp_main)
        amp_main = max(new_amp)
        f_main = xf[new_amp.index(amp_main) + 2]
    
    print(amp_main)
    print(f_main)
    
    ################################################################
    
    #plotting original graph for current 3
    signal3 = signal['Current3']
    
    sd3 = np.std(signal3)
    
    #plt.figure(1, figsize = [10,10], dpi=300)
    #plt.figure(1)
    #plt.plot(signal3)
    
    #plotting fourier graph
    res3 = np.fft.fft(signal3)
    xf3 = np.linspace(0.0, 1.0/(2.0*sample_interval), nsamples//2)
    #plt.figure(2, figsize = [10,10], dpi=300)
    #plt.figure(3)
    #plt.plot(xf3, np.abs(res3[0:nsamples//2]), 'bo')
    
    
    
    #plotting logarithm graph
    logarithm_signal3 = np.log2(np.abs(res3[0:nsamples//2]))
    
    logarithm_x3 = np.log10(xf3)
    #plt.figure(3)
    #plt.plot(xf3, logarithm_signal3)
    
    #plt.figure(4)
    #plt.plot(logarithm_x3, logarithm_signal3)
    
    ###############################################################
    
    signal2 = signal['Current2']
    sd2 = np.std(signal2)
    
    signal4 = signal['Current4']
    sd4 = np.std(signal4)
    
    # Saving data as csv file
    df = pd.DataFrame({"Freq1" : xf, "Amplitude1" : np.abs(res[0:nsamples//2]), "Log freq1" : logarithm_x, "Log amplitude1" : logarithm_signal,
                       "Freq2" : xf3, "Amplitude2" : np.abs(res3[0:nsamples//2]), "Log freq2" : logarithm_x3, "Log amplitude2" : logarithm_signal3,
                       "s.d1" : sd1, "s.d2" : sd2, "s.d3" : sd3, "s.d4" : sd4, "f": f_main, "amp": amp_main})
    df.to_csv('data.csv')
    
    
    ##############  PREDICTION ##############
    from sklearn.externals import joblib

    # load the model from disk
    
    KNN_model = joblib.load('KNN_model.sav')
    
    # Predicting texture of object and whether it has a repeating geometry using machine learning
    KNN_predicted= KNN_model.predict([[sd1, sd2, sd3, amp_main, f_main]])
    print("Prediction by KNN: ", KNN_predicted)
    
    multinomial_model = joblib.load('multinomial_model.sav')
    multinomial_predicted= multinomial_model.predict(np.array([[sd1, sd2, sd3, amp_main, f_main]]))
    print("Prediction by multinomial logistic regression: ", multinomial_predicted)
    
    return KNN_predicted, multinomial_predicted, f_main