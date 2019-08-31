'''
Akram Sbaih, 08-06-2019, Stanford University
This file contains the class template for a robotic arm object,
use it to control and read from the arm as described below
'''
from CurrentReader import *
import os, ctypes, struct, datetime, sys


class arm:
	'''
	arm has the following attributes: dynamixel, reader
	'''
	def import_sdk(self, dynamixel_sdk_path):
		os.sys.path.append(dynamixel_sdk_path)  # append sdk to PATH
		os.sys.path.append('.')			 	# append '.' to PATH
		current_working_directory = os.getcwd()
		os.chdir(dynamixel_sdk_path) 			# change working dir
		import dynamixel_functions as dynamixel # imports Dynamixel SDK library
		self.dynamixel = dynamixel 				# saves the sdk into the object
		os.chdir(current_working_directory)		# return the working directory back here

	def configure_reader(self, config):
		self.reader = DynamixelReader(device_name=config['name'], baud_rate=config['baud'], m1id=config['ids'][0], m2id=config['ids'][1], m3id=config['ids'][2], m4id=config['ids'][3], proto_ver=config['protocol'], read_addr=config['reader_addr'], read_len=config['reader_len'])

	def set_current(self, motor, value):
		self.reader.Set_Value(motor, self.goal['add_cur'], self.goal['len_cur'], value)

	def set_pos(self, motor, value):
		self.reader.Set_Value(motor, self.goal['add_pos'], self.goal['len_pos'], value)


	# returns a dictionary representing the state of all the currents and positions and time of the arm
	def read_state(self):
		[timestamp, dxl1_current, dxl2_current, dxl3_current, dxl4_current] = self.reader.Read_Sync_Once()
		position1 = self.reader.Read_Value(self.reader.m1id, self.present['add_pos'], self.present['len_pos'])
		position2 = self.reader.Read_Value(self.reader.m2id, self.present['add_pos'], self.present['len_pos'])
		state = {'time': timestamp, 'c1': dxl1_current, 'c2': dxl2_current, 'c3': dxl3_current, 'c4': dxl4_current, 'p1': position1, 'p2': position2}
		return state

	# returns the id of the motor responsible for the joint and direction. Kills if it's inappropriate
	def what_motor(self, joint, direction):
		if joint == 1:
			if direction == 'l' or direction == 'r':
				return self.reader.m1id
			elif direction == 'u' or direction == 'd':
				return self.reader.m2id
		elif joint == 2:
			if direction == 'l' or direction == 'r':
				return self.reader.m3id
			elif direction == 'u' or direction == 'd':
				return self.reader.m4id
		print("Inappropriate motion direction. EXIT")
		sys.exit(0)

	def set_pro_params(self, present={'add_pos': 132, 'len_pos': 4, 'add_cur': 126, 'len_cur': 4}, goal={'add_pos': 116, 'len_pos': 4, 'add_cur': 102, 'len_cur': 4}):
		self.present = present
		self.goal = goal

	# moves the specified motor in the specified direction by the dpecified distance
	def move_motor(self, motor, direction, distance):
		initial_pos = self.init_state[{self.reader.m1id: 'p1',  self.reader.m2id: 'p2'}[motor]]
		if (direction == 'l' or direction == 'u'):
			self.set_pos(motor, initial_pos - distance)
		else:
			self.set_pos(motor, initial_pos + distance)
	# initializer for the arm addresses, default to the arm used in the lab
	def start(self, dynamixel_sdk_path= '../DynamixelSDK-master/python/dynamixel_functions_py', config= {'name': "/dev/tty.usbserial-FT2GXCCT".encode('utf-8'), 'baud': 115200, 'ids':[200, 201, 202, 203], 'protocol': 2, 'reader_addr': 126, 'reader_len': 2}):
		self.import_sdk(dynamixel_sdk_path)
		self.configure_reader(config)
		self.set_pro_params()
		self.init_state = self.read_state() # starting point 
