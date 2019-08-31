
"""
Created on August 12

@author: Jason Ah Chuen

Arm explores the environment.

If a feature is found, it uses haptic exploration methods (e.g. stroking) to know more about it: surface roughness, geometry and friction coefficient.

TODO: run scan, make object detection more reliable

"""

from CurrentReader import *
import numpy as np
import time
import matplotlib.pyplot as plt
from surface_exploration2 import run_exploration

from arm import arm
from coord2 import *
import math




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
    
    # Setting speed of all 4 motors
    reader.Set_Value(reader.m1id, 112, LEN_PRO_GOAL_POSITION, 50)
    reader.Set_Value(reader.m2id, 112, LEN_PRO_GOAL_POSITION, 50)
    reader.Set_Value(reader.m3id, 112, LEN_PRO_GOAL_POSITION, 50)
    reader.Set_Value(reader.m4id, 112, LEN_PRO_GOAL_POSITION, 50)
    

    # Reading and setting initial positions for scanning
    
    position1 = reader.Read_Value(reader.m1id, ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
    position2 = reader.Read_Value(reader.m2id, ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
    position3 = reader.Read_Value(reader.m3id, ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
    position4 = reader.Read_Value(reader.m4id, ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
    #print("%f" % position1)
    #print("%f" % position2)
    #print("%f" % position3)
    #print("%f" % position4)
    

    
    
    #creating an instance of the arm
    a = arm()
    #move_to(148, 467, 20, a)
    move_to(340, 400, 10, a)
    
    reader.Set_Value(reader.m1id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 490)
    reader.Set_Value(reader.m2id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 2150)
    reader.Set_Value(reader.m3id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 420)
    reader.Set_Value(reader.m4id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 1255)
    time.sleep(1)
    
    # Array of readings initialized to 0
    #x = np.zeros((N_QUERIES,))
    ys = np.zeros((N_QUERIES,))
    
    #h = np.zeros((N_QUERIES, ))
    
    # Array for event detection
    e = np.zeros(15)
    
    # Number of consecutive events detected
    num_event = 0
    
    # Other parameters
    timestamp = 0
    j = 0
    #i = 0
    ys[j] = 0
    #h[i] = 0
    
    position1 = reader.Read_Value(reader.m1id, ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)

    starting = 25
    while 1:
        
        j = j+1
        
        oldtimestamp = timestamp

        # read all current
        [timestamp, dxl1_current, dxl2_current, dxl3_current, dxl4_current] = reader.Read_Sync_Once()

        ys[j] = dxl1_current
        
        if (j < starting):
            print("Not starting yet")
            continue
        
        # Event detection. Stop if event is detected. Keep moving arm if no event is detected     
        if (np.abs(ys[j]) > 75 and np.abs(ys[j-1]) > 75):
            print("Possible object detected")
            # To make sure that event is constant and not just a fluctuation
            if e[14] == 1:
                
                print("Object detected. Let's find1 it!")
                
                # move arm a bit backwards to x-coordinate
                position1 -= 10
                reader.Set_Value(reader.m1id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, position1)
                
                
                # Now that line is found on the plane, move arm to find x and y coordinates
                x, y, z = get_coordinates(a)
                x = -x
                y = -y
                z = -z
                
                print("%d, %d, %d" % (x, y, z))
                ix, iy, iz = x, y, z
                step_x = int(x/200)
                #print(step_x)
                step_y = int(y/200)
                #print(step_y)
                count = 0
                z -= 50
                c4s = [1, 1, 1, 1, 1, 1, 1, 1, 1]
                means=[1, 1, 1, 1, 1, 1, 1, 1, 1]
                number = 0
                while 1:
                    
                    x -= step_x 
                    y -= step_y 
                    move_to(x, y, z, a)
                    print("Moving towards object")
                    state = a.read_state()
                    print(state)
                    #if (state['p2'] < 1700):
                        #position2 = reader.Read_Value(reader.m2id, ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
                        #reader.Set_Value(reader.m2id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, position2 - 5)
                    c4s.append(math.fabs(state['c4']))
                    means.append(np.mean(c4s[-3:]) - np.mean(c4s[-8:]))
                    if(((np.mean(c4s[-3:]) - np.mean(c4s[-8:])) > 11) and number > 8): 
                        count += 1
                        print("yes")
                        if (count == 2):
                            # After y-coordinate is found, move onto surface and analyze it
                            print("Moving up onto surface")
                            move_to(x, y, z + 10, a)
                            x -= step_x * 5
                            y -= step_y * 5
                            move_to(x, y, z, a)
                            while (state['c2'] < 20):
                                z -= 2
                                move_to(x, y, z, a)
                                state = a.read_state()
                                print(state)
                            
                            
                            print("Now we run the exploration")
                            time.sleep(1)
                            run_exploration("scan.csv")
                            
                            print("Exploration complete!")
                            # Move arm beyond obstacle
                            print("We did it! Moving onto next target now...")
                            x -= step_x
                            y -= step_y
                            move_to(x, y, z, a)
                            
                    else:
                        count = 0
                    number += 1  
                    L = get_distance(a)
                    # keep scanning beyond obstacle if any, up to a certain point 170
                    if (L <= 200):
                        move_to(x, y, 50, a)
                        time.sleep(1)
                        move_to(ix,iy,iz, a)
                        starting = j + 50
                        number = 0
                        #plt.plot(c4s)
                        #plt.plot(means)
                        #plt.show()
                        break
                    else:
                        continue
                    
                
                # go back to original scanning position but on the same position1
                reader.Set_Value(reader.m2id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 2140)
                reader.Set_Value(reader.m3id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 420)
                reader.Set_Value(reader.m4id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 1300)
                
                # move position1 past obstacle
                position1 += 120
                reader.Set_Value(reader.m1id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, position1)
                time.sleep(2)
                
     
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
                 
        print("%09d,%f" % (timestamp, ys[j]))
        
        if (position1 == 1700): break
        
        
        
    del reader
