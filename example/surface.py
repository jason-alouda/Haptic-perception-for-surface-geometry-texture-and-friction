#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 10:11:40 2019

@author: Jason Ah Chuen, Ante Qu

Moves arm in the direction and by the amount specified by the user.
Records current readings all along.

"""
from CurrentReader import *
import os, ctypes, struct
import math
import time
import numpy as np

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

# todo Ante: Set this
os.sys.path.append('../DynamixelSDK-master/python/dynamixel_functions_py')             # Path setting
os.sys.path.append('.')             # Path setting
cwd=os.getcwd()
os.chdir('../DynamixelSDK-master/python/dynamixel_functions_py')
import dynamixel_functions as dynamixel                     # Uses Dynamixel SDK library
os.chdir(cwd)
import datetime


COMM_SUCCESS                = 0                             # Communication Success result value
COMM_TX_FAIL                = -1001                         # Communication Tx Failed

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
    fname = "out4_markerslides.csv"
    fout = open(fname, "w")

    print("Format:")
    print("Timestamp, Current1, Current2, Current3, Current4, dt (msec)")
    print("Timestamp, Current1, Current2, Current3, Current4", file=fout)
    ADDR_PRO_GOAL_POSITION = 116  # address of the goal position and present position
    ADDR_PRO_PRESENT_POSITION = 132
    LEN_PRO_GOAL_POSITION = 4  # length of size of goal and present position
    LEN_PRO_PRESENT_POSITION = 4
    
    # Decide which joint to move
    joint = int(input("Enter 1 for joint 1. Enter 2 for joint 2: "))
    
    # Decide which direction to move
    direction = str(input("Enter l for left direction, r for right direction, u for up direction, d for down direction: "))

    # Decide number of steps/readinga
    N_QUERIES = int(input("Enter number of steps/readings: "))
    
    x1 = np.zeros((2 * N_QUERIES + 360,))
    x2 = np.zeros((2 * N_QUERIES + 360,))
    x3 = np.zeros((2 * N_QUERIES + 360,))
    
    if joint == 1:
        if direction == 'l' or direction == 'r':
            motor = reader.m1id
        elif direction == 'u' or direction == 'd':
            motor = reader.m2id
    elif joint == 2:
        if direction == 'l' or direction == 'r':
            motor = reader.m3id
        elif direction == 'u' or direction == 'd':
            motor = reader.m4id
    else:
        print("Inappropriate input. EXIT")
        del reader
        fout.close()
        sys.exit(0)
        
    # Moving arm forward to get current readings
        
    current_position = reader.Read_Value(motor, ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
    timestamp = 0
    print("Moving forwards")
    for j in range(N_QUERIES):
        oldtimestamp = timestamp

        # read all current
        [timestamp, dxl1_current, dxl2_current, dxl3_current, dxl4_current] = reader.Read_Sync_Once()
        x1[j] = dxl1_current
        x2[j] = dxl2_current
        x3[j] = dxl3_current

        skip = 10
        if j % skip == 0:
            if (direction == 'l' or direction == 'u'):
                reader.Set_Value(motor, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, current_position - int(j/2))
            else:
                reader.Set_Value(motor, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, current_position + int(j/2))

        difft = timestamp - oldtimestamp
        
        print(
            "%09d,%05d,%05d,%05d,%05d, %d" % (timestamp, dxl1_current, dxl2_current, dxl3_current, dxl4_current, difft))
        print("%09d,%05d,%05d,%05d,%05d" % (timestamp, dxl1_current, dxl2_current, dxl3_current, dxl4_current),
              file=fout)
    
    # Moving arm backward to get current readings
    print("Moving backwards")
    for j in range(N_QUERIES):
        oldtimestamp = timestamp

        # read all current
        [timestamp, dxl1_current, dxl2_current, dxl3_current, dxl4_current] = reader.Read_Sync_Once()
        
        x1[j + N_QUERIES] = dxl1_current
        x2[j + N_QUERIES] = dxl2_current
        x3[j + N_QUERIES] = dxl3_current

        skip = 10
        if j % skip == 0:
            if (direction == 'l' or direction == 'u'):
                reader.Set_Value(motor, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, current_position + int(j/2))
            else:
                reader.Set_Value(motor, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, current_position - int(j/2))

        difft = timestamp - oldtimestamp
        
        print(
            "%09d,%05d,%05d,%05d,%05d, %d" % (timestamp, dxl1_current, dxl2_current, dxl3_current, dxl4_current, difft))
        print("%09d,%05d,%05d,%05d,%05d" % (timestamp, dxl1_current, dxl2_current, dxl3_current, dxl4_current),
              file=fout)
        
    
    # Moving arm in a circle
    print("Moving in a circle")
    radius = 1
    angle = 0
    increment = 1
    
    motor3_current_position = reader.Read_Value(reader.m3id, ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
    motor4_current_position = reader.Read_Value(reader.m4id, ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION) - 40
    reader.Set_Value(reader.m4id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, motor4_current_position)
    time.sleep(1)
    
    for j in range(360):

        oldtimestamp = timestamp
        [timestamp, dxl1_current, dxl2_current, dxl3_current, dxl4_current] = reader.Read_Sync_Once()
        
        angle += increment
        motor4_current_position += round(radius * math.sin(math.radians(angle)))
        motor3_current_position += round(radius * math.cos(math.radians(angle)))
        
        reader.Set_Value(reader.m3id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, motor3_current_position)
        reader.Set_Value(reader.m4id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, motor4_current_position)
        
        difft = timestamp - oldtimestamp
        
        print(
          "%09d,%05d,%05d,%05d,%05d, %d" % (timestamp, dxl1_current, dxl2_current, dxl3_current, dxl4_current, difft))
        print("%09d,%05d,%05d,%05d,%05d" % (timestamp, dxl1_current, dxl2_current, dxl3_current, dxl4_current),
             file=fout)       
    
    del reader
    fout.close()

#miscellaneous
# Control table address
ADDR_PRO_TORQUE_ENABLE = 64  # Control table address is different in Dynamixel model
ADDR_PRO_GOAL_POSITION = 116
ADDR_PRO_REALTIME_TICK = 120
ADDR_PRO_PRESENT_POSITION = 132
ADDR_PRO_LED_RED = 65
ADDR_PRO_CURRENT = 126

# Data Byte Length
LEN_PRO_GOAL_POSITION = 4
LEN_PRO_PRESENT_POSITION = 4
LEN_PRO_REALTIME_TICK = 2
LEN_PRO_LED_RED = 1
LEN_PRO_CURRENT = 2

# Protocol version
PROTOCOL_VERSION = 2  # See which protocol version is used in the Dynamixel

# Default setting
DXL1_ID = 100  # Dynamixel ID: 1
DXL2_ID = 101  # Dynamixel ID: 2
DXL3_ID = 102  # Dynamixel ID: 3
DXL4_ID = 103  # Dynamixel ID: 4
BAUDRATE = 1000000
DEVICENAME = "COM5".encode('utf-8')  # Check which port is being used on your controller