#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 10:11:40 2019

@author: Jason Ah Chuen, Ante Qu

Moves arm in the direction and by the amount specified by the user.

"""

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



class DynamixelReader:
    def __init__(self,
                 # Check which port is being used on your controller
                 device_name = "COM5".encode('utf-8'),
                 # baud rate
                 baud_rate = 1000000,
                 # motor ids
                 m1id = 100,                                # Joint 1 moves horizontally
                 m2id = 101,                                # Joint 1 moves vertically
                 m3id = 102,                                # Joint 2 moves horizontally
                 m4id = 103,                                # Joint 2 moves vertically
                 #protocol ver
                 proto_ver = 2,
                 #SyncRead Addr
                 read_addr = 126,
                 #SyncRead Len
                 read_len = 2):
        self.baud_rate = baud_rate
        self.device_name = device_name
        self.m1id = m1id
        self.m2id = m2id
        self.m3id = m3id
        self.m4id = m4id
        self.proto_ver = proto_ver
        self.read_addr = read_addr
        self.read_len = read_len

        # Initialize PortHandler Structs
        # Set the port path
        # Get methods and members of PortHandlerLinux or PortHandlerWindows
        self.port_num = dynamixel.portHandler(device_name)
        dynamixel.setPacketTimeoutMSec(1)
        # Initialize PacketHandler Structs
        dynamixel.packetHandler()
        # Initialize Groupsyncread Structs for Current
        self.groupread_num = dynamixel.groupSyncRead(self.port_num, proto_ver, read_addr,read_len) #0, 148
        dt = datetime.datetime.now()
        self.timestamp0 = dt.minute * 60000000 + dt.second * 1000000 + dt.microsecond
        self.Init_Port_And_Motors()
        self.Init_Param_Storage()

    def __del__(self):
        self.Disable_Torque_Close_Port()

    def Init_Port_And_Motors(self):
        # Open port
        if dynamixel.openPort(self.port_num):
            print("Successfully opened the port!")
        else:
            print("Failed to open the port!")
            print("Press any key to terminate...")
            getch()
            quit()
        # Set port baudrate
        if dynamixel.setBaudRate(self.port_num, self.baud_rate):
            print("Successfully set the baudrate!")
        else:
            print("Failed to change the baudrate!")
            print("Press any key to terminate...")
            getch()
            quit()
        ADDR_PRO_TORQUE_ENABLE = 64
        TORQUE_ENABLE = 1
        dxl_comm_result = COMM_TX_FAIL
        # Enable Dynamixel#1 Torque
        dynamixel.write1ByteTxRx(self.port_num, self.proto_ver, self.m1id, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
        dxl_comm_result = dynamixel.getLastTxRxResult(self.port_num, self.proto_ver)
        dxl_error = dynamixel.getLastRxPacketError(self.port_num, self.proto_ver)
        if dxl_comm_result != COMM_SUCCESS:
            print(dynamixel.getTxRxResult(self.proto_ver, dxl_comm_result))
        elif dxl_error != 0:
            print(dynamixel.getRxPacketError(self.proto_ver, dxl_error))
        else:
            print("Dynamixel#1 has been successfully connected")
        # Enable Dynamixel#2 Torque
        dynamixel.write1ByteTxRx(self.port_num, self.proto_ver, self.m2id, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
        dxl_comm_result = dynamixel.getLastTxRxResult(self.port_num, self.proto_ver)
        dxl_error = dynamixel.getLastRxPacketError(self.port_num, self.proto_ver)
        if dxl_comm_result != COMM_SUCCESS:
            print(dynamixel.getTxRxResult(self.proto_ver, dxl_comm_result))
        elif dxl_error != 0:
            print(dynamixel.getRxPacketError(self.proto_ver, dxl_error))
        else:
            print("Dynamixel#2 has been successfully connected")
        # Enable Dynamixel#3 Torque
        dynamixel.write1ByteTxRx(self.port_num, self.proto_ver, self.m3id, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
        dxl_comm_result = dynamixel.getLastTxRxResult(self.port_num, self.proto_ver)
        dxl_error = dynamixel.getLastRxPacketError(self.port_num, self.proto_ver)
        if dxl_comm_result != COMM_SUCCESS:
            print(dynamixel.getTxRxResult(self.proto_ver, dxl_comm_result))
        elif dxl_error != 0:
            print(dynamixel.getRxPacketError(self.proto_ver, dxl_error))
        else:
            print("Dynamixel#3 has been successfully connected")
        # Enable Dynamixel#4 Torque
        dynamixel.write1ByteTxRx(self.port_num, self.proto_ver, self.m4id, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
        dxl_comm_result = dynamixel.getLastTxRxResult(self.port_num, self.proto_ver)
        dxl_error = dynamixel.getLastRxPacketError(self.port_num, self.proto_ver)
        if dxl_comm_result != COMM_SUCCESS:
            print(dynamixel.getTxRxResult(self.proto_ver, dxl_comm_result))
        elif dxl_error != 0:
            print(dynamixel.getRxPacketError(self.proto_ver, dxl_error))
        else:
            print("Dynamixel#4 has been successfully connected")

    def Init_Param_Storage(self):
        groupread_num = self.groupread_num
        # Add parameter storage for Dynamixel#1 current
        dxl_addparam_result = ctypes.c_ubyte(dynamixel.groupSyncReadAddParam(groupread_num, self.m1id)).value
        if dxl_addparam_result != 1:
            print("[ID:%03d] groupSyncRead addparam failed" % (self.m1id))
            quit()

        # Add parameter storage for Dynamixel#2 current
        dxl_addparam_result = ctypes.c_ubyte(dynamixel.groupSyncReadAddParam(groupread_num, self.m2id)).value
        if dxl_addparam_result != 1:
            print("[ID:%03d] groupSyncRead addparam failed" % (self.m2id))
            quit()

        # Add parameter storage for Dynamixel#2 current
        dxl_addparam_result = ctypes.c_ubyte(dynamixel.groupSyncReadAddParam(groupread_num, self.m3id)).value
        if dxl_addparam_result != 1:
            print("[ID:%03d] groupSyncRead addparam failed" % (self.m3id))
            quit()

        # Add parameter storage for Dynamixel#4 current
        dxl_addparam_result = ctypes.c_ubyte(dynamixel.groupSyncReadAddParam(groupread_num, self.m4id)).value
        if dxl_addparam_result != 1:
            print("[ID:%03d] groupSyncRead addparam failed" % (self.m4id))
            quit()

    def Set_Value(self, motorId, set_addr, set_len, value):
        if(set_len == 4):
            dynamixel.write4ByteTxRx(self.port_num, self.proto_ver, motorId, set_addr, value)
        elif(set_len == 2):
            dynamixel.write2ByteTxRx(self.port_num, self.proto_ver, motorId, set_addr, value)
        elif(set_len == 1):
            dynamixel.write1ByteTxRx(self.port_num, self.proto_ver, motorId, set_addr, value)
        else:
            print('[ID:%03d]: invalid set length %d' %(motorId, set_len))
            return
        dxl_comm_result = dynamixel.getLastTxRxResult(self.port_num, self.proto_ver)
        dxl_error = dynamixel.getLastRxPacketError(self.port_num, self.proto_ver)
        if dxl_comm_result != COMM_SUCCESS:
            print(dynamixel.getTxRxResult(self.proto_ver, dxl_comm_result))
        elif dxl_error != 0:
            print(dynamixel.getRxPacketError(self.proto_ver, dxl_error))

    def Read_Value(self, motorId, read_addr, read_len):
        # Read value
        dxl_result = -1
        if(read_len == 4):
            dxl_result = dynamixel.read4ByteTxRx(self.port_num, self.proto_ver, motorId, read_addr)
        elif(read_len == 2):
            dxl_result = dynamixel.read2ByteTxRx(self.port_num, self.proto_ver, motorId, read_addr)
        elif(read_len == 1):
            dxl_result = dynamixel.read1ByteTxRx(self.port_num, self.proto_ver, motorId, read_addr)
        else:
            print('[ID:%03d]: invalid read length %d' %(motorId, read_len))
            return dxl_result
        dxl_comm_result = dynamixel.getLastTxRxResult(self.port_num, self.proto_ver)
        dxl_error = dynamixel.getLastRxPacketError(self.port_num, self.proto_ver)
        if dxl_comm_result != COMM_SUCCESS:
            print(dynamixel.getTxRxResult(self.proto_ver, dxl_comm_result))
        elif dxl_error != 0:
            print(dynamixel.getRxPacketError(self.proto_ver, dxl_error))
        return dxl_result


    def Disable_Torque_Close_Port(self):
        ADDR_PRO_TORQUE_ENABLE = 64
        TORQUE_DISABLE = 0
        dxl_comm_result = COMM_TX_FAIL
        # Enable Dynamixel#1 Torque
        dynamixel.write1ByteTxRx(self.port_num, self.proto_ver, self.m1id, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)
        dxl_comm_result = dynamixel.getLastTxRxResult(self.port_num, self.proto_ver)
        dxl_error = dynamixel.getLastRxPacketError(self.port_num, self.proto_ver)
        if dxl_comm_result != COMM_SUCCESS:
            print(dynamixel.getTxRxResult(self.proto_ver, dxl_comm_result))
        elif dxl_error != 0:
            print(dynamixel.getRxPacketError(self.proto_ver, dxl_error))
        else:
            print("Dynamixel#1 has been successfully freed")
        # Enable Dynamixel#2 Torque
        dynamixel.write1ByteTxRx(self.port_num, self.proto_ver, self.m2id, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)
        dxl_comm_result = dynamixel.getLastTxRxResult(self.port_num, self.proto_ver)
        dxl_error = dynamixel.getLastRxPacketError(self.port_num, self.proto_ver)
        if dxl_comm_result != COMM_SUCCESS:
            print(dynamixel.getTxRxResult(self.proto_ver, dxl_comm_result))
        elif dxl_error != 0:
            print(dynamixel.getRxPacketError(self.proto_ver, dxl_error))
        else:
            print("Dynamixel#2 has been successfully freed")
        # Enable Dynamixel#3 Torque
        dynamixel.write1ByteTxRx(self.port_num, self.proto_ver, self.m3id, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)
        dxl_comm_result = dynamixel.getLastTxRxResult(self.port_num, self.proto_ver)
        dxl_error = dynamixel.getLastRxPacketError(self.port_num, self.proto_ver)
        if dxl_comm_result != COMM_SUCCESS:
            print(dynamixel.getTxRxResult(self.proto_ver, dxl_comm_result))
        elif dxl_error != 0:
            print(dynamixel.getRxPacketError(self.proto_ver, dxl_error))
        else:
            print("Dynamixel#3 has been successfully freed")
        # Enable Dynamixel#4 Torque
        dynamixel.write1ByteTxRx(self.port_num, self.proto_ver, self.m4id, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)
        dxl_comm_result = dynamixel.getLastTxRxResult(self.port_num, self.proto_ver)
        dxl_error = dynamixel.getLastRxPacketError(self.port_num, self.proto_ver)
        if dxl_comm_result != COMM_SUCCESS:
            print(dynamixel.getTxRxResult(self.proto_ver, dxl_comm_result))
        elif dxl_error != 0:
            print(dynamixel.getRxPacketError(self.proto_ver, dxl_error))
        else:
            print("Dynamixel#4 has been successfully freed")

        #close port
        dynamixel.closePort(self.port_num)

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
    
    # Decide which joint to move
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
        sys.exit(0)
        
        
    # Moving arm
    
    current_position = reader.Read_Value(motor, ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
    timestamp = 0
    for j in range(N_QUERIES):

        #set goal position example
        skip = 10
        if j % skip == 0:
            if (direction == 'l' or direction == 'u'):
                reader.Set_Value(motor, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, current_position - int(j/10))
            else:
                reader.Set_Value(motor, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, current_position + int(j/10))



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
