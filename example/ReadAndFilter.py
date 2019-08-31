#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Ante Qu

#
# *********     Dynamixel Arm Current Readings      *********
#
#
# Available Dynamixel model on this example : All models using Protocol 2.0
# This example is designed for using two Dynamixel PRO 54-200, and an USB2DYNAMIXEL.
# To use another Dynamixel model, such as X series, see their details in E-Manual(support.robotis.com) and edit below variables yourself.
# Be sure that Dynamixel PRO properties are already set as %% ID : 1 / Baudnum : 1 (Baudrate : 57600)
#

from CurrentReader import *
import numpy as np
from scipy.signal import butter, lfilter, freqz


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def run_filter(data, b, a):
    y = lfilter(b, a, data)
    return y

if __name__ == '__main__':

    reader = DynamixelReader(device_name = "/dev/tty.usbserial-FT2N0DM5".encode('utf-8'),
                             # baud rate
                             baud_rate = 115200,
                             # motor ids
                             m1id = 100, m2id = 101, m3id = 102, m4id = 103,
                             # protocol ver
                             proto_ver = 2,
                             # Motor Current Addr and Len
                             read_addr = 126, read_len = 2)
    fname = "out4_filtered.csv"
    fout = open(fname, "w")
    N_QUERIES = 4000
    print("Format:")
    print("Timestamp, filtered")
    print("Timestamp, filtered", file=fout)
    ADDR_PRO_GOAL_POSITION = 116
    ADDR_PRO_PRESENT_POSITION = 132
    LEN_PRO_GOAL_POSITION = 4
    LEN_PRO_PRESENT_POSITION = 4

    current_position = reader.Read_Value(reader.m4id, ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
    x = np.zeros((N_QUERIES,))
    y = np.zeros((N_QUERIES,))
    timestamp = 0
    fs = 240.
    low = 5.
    hi = 100.
    b,a = butter_bandpass(low,hi,fs, order=4)
    M=b.size
    N=a.size
    for j in range(N_QUERIES):
        oldtimestamp = timestamp

        # read all current
        [timestamp, dxl1_current, dxl2_current, dxl3_current, dxl4_current] = reader.Read_Sync_Once()

        # compute norm
        x[j] = np.sqrt(dxl1_current**2 + dxl2_current**2 + dxl3_current**2 + dxl4_current**2)
        #filter
        if (j < 20):
            if (j>= 10):
                # filter everything using lfilter
                y[0:j+1]= lfilter(b, a, x[0:j+1])
            else:
                # don't filter first ten
                y[j] = x[j]
        else:
            y[j] = 1./a[0] *( b.dot(x[j:j-M:-1]) - a[1:N].dot(y[j-1:j-N:-1]))
        if (np.abs(y[j]) > 1. and np.abs(y[j-1]) > 1.):
            print( " EVENT ")
        #set goal position example
       # skip = 20
       # if j % skip == 0:
       #     reader.Set_Value(reader.m4id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, current_position - int(j/10))

        difft = timestamp - oldtimestamp
        print(
            "%09d,%f" % (timestamp, y[j] ))
        print("%09d,%f" % (timestamp, y[j]),
              file=fout)
        print(y[j])
        print(x[j])
    del reader
    fout.close()
