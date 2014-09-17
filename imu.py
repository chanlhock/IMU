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

#### include external libraries ####
import socket
import traceback
import csv
import struct
import sys, time, string, pygame
from pygame.locals import *

from ponycube import *
from MadgwickAHRS import *
import os

#### assign local variables ####
host = ''
port = 5555
csvf = 'accelerometer.csv'

#### do UDP stuff (communicate with mobile phone's WiFi) ####
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host, port))

gameOver=False

#### do CSV stuff ####
with open(csvf, 'w', newline='', encoding='ascii') as csv_handle:
    csv_writer = csv.writer(csv_handle, delimiter=',')

    position = 20, 50
    os.environ['SDL_VIDEO_WINDOW_POS'] = str(position[0]) + "," + str(position[1])

    f = open("log.txt", "w")  # open a log text file

    pygame.init()
    screen = Screen(780,700,scale=1.5)  # original was 480, 400

    cube = Cube(60,120,10)   # original was 30,60,10
    caption = 'Platform for study of IMU features and functionality'
    pygame.display.set_caption(caption, 'Spine Runtime')
  

    q = Quaternion(1,0,0,0)
    cube.erase(screen)

    cube.draw(screen,q)


    pygame.display.flip()

    previous_timestamp = 0  # store previous value of timestamp

    while not gameOver:   # endless loop until user press Ctrl-Break key
        try:
            for e in pygame.event.get():
                if e.type==QUIT:
                    gameOver=True
                if e.type==KEYDOWN:
                    if e.key==K_ESCAPE:
                        gameOver=True

            #event = pygame.event.poll()

            # TODO: Allow exit via keystroke.

            #if event.type == pygame.QUIT:

            #   viewer.close()
            #   break


            message, address = s.recvfrom(8192)
            #print(message)                     # display data received from UDP on screen for debugging purpose
            csv_writer.writerow(message)        # write data to CSV file

            #print('Length of message', len(message))
            my_array = message.split(b',')
            #print(message)
            #print("gx: "+my_array[6]+"gy: "+my_array[7])
            print(my_array[6])
            print(my_array[7])

            print('Length of array', len(my_array))
            f.write("\nLength of array: ")
            length = len(my_array)
            f.write(str(length))

            if len(my_array) >= 13:  # if received data packet length is < 13 then data is thrown away as incomplete
                ax = float(my_array[2])
                ay = float(my_array[3])
                az = float(my_array[4])
                gx = float(my_array[6])
                gy = float(my_array[7])
                gz = float(my_array[8])
                mx = float(my_array[10])
                my = float(my_array[11])
                mz = float(my_array[12])

                if previous_timestamp <= 0:  
                    previous_timestamp = float(my_array[0])
                    time_diff = float(0)
                else:
                    time_diff = float(my_array[0]) - previous_timestamp
                    previous_timestamp = float(my_array[0])

                print('Time taken:', time_diff, 'secs')
                
                # Implementation of Madgwick's IMU and AHRS algorithms.
                # Uses the New Orientation Filter instead of conventional Kalman filter
                quaternion_list = MadgwickAHRSupdate(gx, gy, gz, ax, ay, az, mx, my, mz)     # c code module to be called by Python  
                
                print(">>>> Quaternion output qx, qy, qz, qw")
                f.write("\n>>>> Quaternion output qx, qy, qz, qw\n")
                print(quaternion_list)
                #print("qx=%f qy=%f qz=%f qw=%f", quaternion_list[0], quaternion_list[1], quaternion_list[2], quaternion_list[3])

                # assigned returned output to the quaternion local variables
                qx = float(quaternion_list[0])
                qy = float(quaternion_list[1])
                qz = float(quaternion_list[2])
                qw = float(quaternion_list[3])

                f.write(str(qx))
                f.write(" ")
                f.write(str(qy))
                f.write(" ")
                f.write(str(qz))
                f.write(" ")
                f.write(str(qw))

                q.w = qw
                q.x = -qz    # changing the direction to accomodate S3  - chanlhock 04/09/14
                q.y = -qy    # changing the direction to accomodate S3  - chanlhock 04/09/14
                q.z = qx
                cube.erase(screen)

                cube.draw(screen,q)

                pygame.display.flip()

            print("  ")  # leave an empty row for ease of readability
            # TODO: If system load is too high, increase this sleep time.

            pygame.time.delay(0)

        # Non Python 3.4 old method of raise exception format
        #     except(KeyboardInterrupt, SystemExit):
        #         raise
        #     except:
        #         traceback.print_exc()

        except Exception:
            traceback.print_exc()
    f.close()
