
"""
Created on August 6

@author: Jason Ah Chuen

Arm explores the environment.

If a feature is found, it uses haptic exploration methods (e.g. stroking) to know more about it: surface roughness, geometry and friction coefficient.

TODO: search process is incorrect rns

"""

from CurrentReader import *
import numpy as np
from surface_exploration import run_exploration
import time


if __name__ == '__main__':

    reader = DynamixelReader(device_name = "/dev/tty.usbserial-FT2GXCCT".encode('utf-8'),
                             # baud rate
                             baud_rate = 115200,
                             # motor ids
                             m1id = 200, m2id = 201, m3id = 202, m4id = 203,
                             # protocol ver
                             proto_ver = 2,
                             # Motor Current Addr and Len
                             read_addr = 126, read_len = 2)

    ADDR_PRO_GOAL_POSITION = 116
    ADDR_PRO_PRESENT_POSITION = 132
    LEN_PRO_GOAL_POSITION = 4
    LEN_PRO_PRESENT_POSITION = 4
    
    ADDR_PRO_GOAL_VELOCITY = 104
    LEN_PRO_GOAL_VELOCITY = 4
    
    
    N_QUERIES = 10000
    
    
    # Reading current position (position1) at start
    position1 = reader.Read_Value(reader.m1id, ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
    position2 = reader.Read_Value(reader.m2id, ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
    position4 = reader.Read_Value(reader.m4id, ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
    
    # Setting velocity for motor1
    reader.Set_Value(reader.m1id, ADDR_PRO_GOAL_VELOCITY, LEN_PRO_GOAL_VELOCITY, 10)
    
    
    initial_position2 = position2
    
    # Array of readings initialized to 0
    x = np.zeros((N_QUERIES,))
    y = np.zeros((N_QUERIES,))
    
    # Array for event detection
    e = np.zeros(15)
    
    # Number of consecutive events detected
    num_event = 0
    
    # Other parameters
    timestamp = 0
    j = 0;
    flag = 1
    y[j] = 0
    
    while 1:
        
        j = j+1

        oldtimestamp = timestamp

        # read all current
        [timestamp, dxl1_current, dxl2_current, dxl3_current, dxl4_current] = reader.Read_Sync_Once()

        y[j] = dxl1_current
        
        
        # Event detection. Stop if event is detected. Keep moving arm if no event is detected     
        if (np.abs(y[j]) > 50 and np.abs(y[j-1]) > 50):
            print("Here")
            # To make sure that event is constant and not just a fluctuation
            if e[14] == 1:
                reader.Set_Value(reader.m1id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, position1 - 10)
                time.sleep(0.5)
                # Go onto surface and analyze it
                while (np.abs(dxl1_current) > 20):
                    print("Moving up onto surface")
                    
                    # read all current
                    [timestamp, dxl1_current, dxl2_current, dxl3_current, dxl4_current] = reader.Read_Sync_Once()
                    print(dxl1_current)
                    
                    position2 -= 2
                    reader.Set_Value(reader.m2id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, position2)
                    time.sleep(0.5)
                    
                run_exploration()
                reader.Set_Value(reader.m2id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, initial_position2)
                j += 250
            else:
                e[num_event] = 1
                num_event += 1
        else:
            # Reset array for event detection
            e = np.zeros(15)
            num_event = 0
        
        # Going in one direction for 2000 readings
        if (flag == 1):
            position1 += 1
            reader.Set_Value(reader.m1id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, position1)
        else:
            position1 -= 1
            reader.Set_Value(reader.m1id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, position1)
            
        
        print("%09d,%f" % (timestamp, y[j]))
        
        # Changing radius pf path along which arm is rotating if 2000 readings reached along current path
        if ((j % 2000) == 0):
            position4 += 10
            reader.Set_Value(reader.m4id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, position4)
            flag = -flag
        
    del reader