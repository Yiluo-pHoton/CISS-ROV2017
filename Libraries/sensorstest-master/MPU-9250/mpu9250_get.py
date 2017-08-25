#!/usr/bin/python

from mpu9250 import *
import time

mpu = MPU9250()
mpu.initialize()

compas = AK8963()
compas.initialize()

# Set calibration data
mpu.gyro_offs =  {'y': 136, 'x': -167, 'z': 59}
mpu.accel_offs =  {'y': -2, 'x': 7048, 'z': -3200}

compas.calibration_matrix = [  [1.560948, 0.001838, -0.011552],
                                        [0.001838, 1.521376, 0.047572],
                                        [-0.011552, 0.047572, 1.357251]]
compas.bias = [218.92, 115.072, -121.599]

while True:
	gyro_data = mpu.get_gyro()
	accel_data = mpu.get_accel()
	compas_data = compas.get_calibrated()
	
	print "GYROSCOPE: ", gyro_data
	print "ACCELEROMETER: ", accel_data
	print "TEMPERATURE: ",mpu.get_temp()
	print "MAGNETOMETER: ", compas_data, "\n\n"

	time.sleep(1)
