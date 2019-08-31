
"""
Created on August 12

@author: Jason Ah Chuen

Arm explores the environment.

If a feature is found, it uses haptic exploration methods (e.g. stroking) to know more about it: surface roughness, geometry and friction coefficient.

TODO: search process is incorrect rns

"""

from CurrentReader import *
import numpy as np
from surface_exploration import run_exploration
import time

from arm import arm
from coord2 import *




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
    
    # Setting initial positions for scanning
    reader.Set_Value(reader.m1id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 200)
    time.sleep(0.25)
    reader.Set_Value(reader.m2id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 2430)
    time.sleep(0.25)
    reader.Set_Value(reader.m3id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 427)
    time.sleep(0.25)
    reader.Set_Value(reader.m4id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 960)
    
    
    # Reading current position (position1) at start
    position1 = reader.Read_Value(reader.m1id, ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
    position2 = reader.Read_Value(reader.m2id, ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
    position4 = reader.Read_Value(reader.m4id, ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
    
    # Setting velocity for motor1
    reader.Set_Value(reader.m1id, ADDR_PRO_GOAL_VELOCITY, LEN_PRO_GOAL_VELOCITY, 10)
    
    arm = arm()
    
    
    # Array of readings initialized to 0
    x = np.zeros((N_QUERIES,))
    y = np.zeros((N_QUERIES,))
    
    #h = np.zeros((N_QUERIES, ))
    
    # Array for event detection
    e = np.zeros(15)
    
    # Number of consecutive events detected
    num_event = 0
    
    # Other parameters
    timestamp = 0
    j = 0
    #i = 0
    y[j] = 0
    #h[i] = 0
    
    while 1:
        
        j = j+1

        oldtimestamp = timestamp

        # read all current
        [timestamp, dxl1_current, dxl2_current, dxl3_current, dxl4_current] = reader.Read_Sync_Once()

        y[j] = dxl1_current
        
        
        # Event detection. Stop if event is detected. Keep moving arm if no event is detected     
        if (np.abs(y[j]) > 50 and np.abs(y[j-1]) > 50):
            print("Possible object detected")
            # To make sure that event is constant and not just a fluctuation
            if e[14] == 1:
                reader.Set_Value(reader.m1id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, position1 - 10)
                time.sleep(0.5)
                
                # Now that x coordinate is found on the plane, move arm to find y-coordinate
                while 1:
                    x, y, z = ang_to_xyz(reader,m2id, reader.m4id, reader.m1id)
                    y += 1
                    arm.move_to(x, y, z)
                    state = arm.read_state()
                    if (state['c2'] > 50):
                        
                        # After y-coordinate is found, move onto surface and analyze it
                        print("Moving up onto surface")
                        arm.move_to(x, y, z + 4)
                        arm.move_to(x + 5, y, z + 2)
                        #run_exploration()
                        
                        # Move arm beyond obstacle
                        arm.move_to(_, _, _)
                    
                    # keep scanning beyond obstacle if any, up to a certain point
                    if (z >= _):
                        arm.move_to(_,_,_)
     
            else:
                e[num_event] = 1
                num_event += 1
        else:
            # Reset array for event detection
            e = np.zeros(15)
            num_event = 0
        
        # Going in one direction
        position1 += 1
        reader.Set_Value(reader.m1id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, position1)
                 
        print("%09d,%f" % (timestamp, y[j]))
        
        
        
    del reader
