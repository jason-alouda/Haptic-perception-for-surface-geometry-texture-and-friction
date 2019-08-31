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
                             m1id = 200, m2id = 201, m3id = 202, m4id = 203,
                             # protocol ver
                             proto_ver = 2,
                             # Motor Current Addr and Len
                             read_addr = 126, read_len = 2)
    fname = "test.csv"
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
        
    # Moving arm and reading current
        
    current_position = reader.Read_Value(motor, ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
    timestamp = 0
    for j in range(N_QUERIES):
        oldtimestamp = timestamp

        # read all current
        [timestamp, dxl1_current, dxl2_current, dxl3_current, dxl4_current] = reader.Read_Sync_Once()

        #filter


        #set goal position example

        if (direction == 'l' or direction == 'u'):
            reader.Set_Value(motor, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, current_position - int(j/10))
        else:
            reader.Set_Value(motor, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, current_position + int(j/10))

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
