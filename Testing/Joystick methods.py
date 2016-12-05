import pygame
import time


pygame.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()

#data = joystick.get_numaxes()
#print data

def joystickParse():
    while True:
        data = joystick.get_axis(0)
        data2 = joystick.get_axis(1)
        data3 = joystick.get_axis(2)
        data4 = joystick.get_axis(3)    
        data5 = joystick.get_axis(4)
        data6 = joystick.get_axis(5)
        data = round(data, 2)
        data2 = round(data2, 2)
        data3 = round(data3, 2)
        data4 = round(data4, 2)
        data5 = round(data5, 2)
        data6 = round(data6, 2)
        msg = str(data) + " " + str(data2) + " " + str(data3) + " " + str(data4) + " " + str(data5) + " " + str(data6)
        print msg
        return msg
        pygame.event.pump()
        time.sleep(0.05)
joystickParse()
