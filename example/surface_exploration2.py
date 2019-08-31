#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 10:39:26 2019

@author: jasonahchuen
"""

from scanner import scan
from plotter import *
from fourier2 import run_fourier
from data_analysis import run_analysis


def run_exploration(filename, geometry = False):
    
    # current readings scan
    scan(filename=filename, reposition = False)
    l1 = [filename]
    #position_current_plot(l1)
    
    # geometry scan
    if (geometry == True):
        scan("geometry.csv", reposition = True)
        l2 = ["geometry.csv"]
        
        
    run_fourier()
    
    KNN_predicted, multinomial_predicted, freq = run_analysis()
    
    # If object has a repeating geometry, predict geometry of surface using its first and second derivatives
        
    if (KNN_predicted == 1 or multinomial_predicted == 'FS'):
        print("No repeating geometry found. This is likely to be a flat, smooth surface")
    elif (KNN_predicted == 0 or multinomial_predicted == 'FR'):
        print("No repeating geometry found. This is likely to be a flat, rough surface")
        
    
    if (KNN_predicted == 2 or multinomial_predicted == 'WS'):
        print("This is likely to be a wavy, smooth surface")
        g = input("Would you like to see the geometry scan?")
        if (g == 'y'):
            position_only_plot("geometry.csv")
    elif (KNN_predicted == 3 or multinomial_predicted == 'WR'):
        print("This is likely to be a wavy, rough surface") 
        g = input("Would you like to see the geometry scan?")
        if (g == 'y'):
            position_only_plot(l2)
    
    
    
    
    

if __name__ == '__main__':
    run_exploration(filename = 'scan.csv')