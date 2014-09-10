##################################################################################################################
# Platform for study of IMU features and functionality (using Samsung S3 internal phone IMU) 
# Demo program (imu.py)
#
# Copyright (c) 2014 Bernard Chan 
# chanlhock@gmail.com
#
# Date			Author          Notes
# 04/09/2014	     Bernard Chan   Initial release
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 2.1 of the License, or (at your
# option) any later version.
##################################################################################################################
# This program is tested to run on Windows based Python 3.4.1 and Pygame 1.9.2
# Pygame 1.9.2 installation (pygame‑1.9.2a0.win32‑py3.4.exe) for Windows can be found at:
# http://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame

# Code included leveraged from open source with thanks :-) are:
#    Python code:
#       ponycube.py, euclid.py
#    C code to be compiled into modules to be called from Python:
#       MadgwickAHRS.c & MadgwickAHRS.h compiled by gcc to MadgwickAHRS.pyd 
#       gcc -shared -IC:\Python34\include -LC:\Python34\libs MadgwickAHRS.c -lpython34 -o MadgwickAHRS.pyd 

# IMU+GPS-Stream apps (install to mobile phone through Google PlayStore)
# - sends the measurements from your phone inertial sensors via UDP as CSV (Comma-Separated Values) 
#   to a computer in your network.
# This turns your phone into a wireless inertial measurement unit (IMU).
# The following sensors are supported:
# - Accelerometer
# - Gyroscope
# - Magnetometer
# If your phone has not all these sensors, only the available sensor data is transmitted.
# Example UDP packet:
# 890.71558, 3, 0.076, 9.809, 0.565, 4, -0.559, 0.032, -0.134, 5, -21.660,-36.960,-28.140
# Timestamp [sec], sensorid, x, y, z, sensorid, x, y, z, sensorid, x, y, z
# Sensor id:
# 3 - Accelerometer (m/s^2)
# 4 - Gyroscope (rad/s)
# 5 - Magnetometer (micro-Tesla uT)
##################################################################################################################
