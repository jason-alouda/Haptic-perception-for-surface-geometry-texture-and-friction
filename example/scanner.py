#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 10:11:40 2019

@author: Jason Ah Chuen

Moves arm in the direction and by the amount specified by the user.
For the first scan, current readings on all 4 joints are recorded.
For the second scan, x-position (joint 1) and y-position (joint 2)  are recorded.

TODO: Find friction coefficient from first scan

"""
import arm as robot
import pandas as pd

'''
# Decide which joint to move
joint = int(input("Enter 1 for joint 1. Enter 2 for joint 2: "))
# Decide which direction to move
direction = str(input("Enter l for left direction, r for right direction, u for up direction, d for down direction: "))
# Decide number of steps/readinga
n_steps = int(input("Enter number of steps/readings: "))
'''


'''
This function performs a lateral scan on a sample with the provided parameters.
@param topo: True to trace the surface vertically; False to not change vertical position
'''
def scan(joint=1, direction='r', n_steps=250, filename="scan.csv", topo=False):
	# initialize an object for the robotic arm
	arm = robot.arm()
	arm.start()
	# This dataframe will store the time, current, and position readings of the scan
	df = pd.DataFrame(columns=['time', 'c1', 'c2', 'c3', 'c4', 'p1', 'p2'])
	# Setting current of motor2
	arm.set_current(motor=arm.reader.m2id, value=30)
	# gets the motor responsible for the requested motion
	motor = arm.what_motor(joint=joint, direction=direction)
	# move the arm step by step while recording the states of currents and position
	for step in range(n_steps):
		# read all current
		state = arm.read_state()
		# append the record to the dataframe
		df = df.append(other=state, ignore_index=True)
		# move the arm by a step
		arm.move_motor(motor=motor, direction=direction, distance=step//2)
		# if this is a topo scan, adapt the pressure of the arm to follow the surface
		if topo: adapt_topo(arm, state)

	df.to_csv(filename)
	
# this function uses the force measurements to change the vertical position of the arm to trace the surface
def adapt_topo(arm, state, sensitivity=2):
		if (state['c1'] < -20):
			arm.set_pos(arm.reader.m2id, state['p2'] - 6)
		if (state['c1'] > -3 and state['c2'] < -4) :
			arm.set_pos(arm.reader.m2id, state['p2'] + 6)

if __name__=="__main__":
	scan(joint=1, direction='r', n_steps=250)
