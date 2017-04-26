import sys
import socket
import select
import pygame
import time
import pyfirmata

########Below is superfluous code necessary only for receiving and sending controller input
# pygame.init()

# joystick = pygame.joystick.Joystick(0)
# joystick.init()


# def print_data():
# 	data = joystick.get_axis(0)
# 	data2 = joystick.get_axis(1)
# 	data3 = joystick.get_axis(2)
# 	data4 = joystick.get_axis(3)    
# 	data5 = joystick.get_axis(4)
# 	data6 = joystick.get_axis(5)
# 	data = round(data, 2)
# 	data2 = round(data2, 2)
# 	data3 = round(data3, 2)
# 	data4 = round(data4, 2)
# 	data5 = round(data5, 2)
# 	data6 = round(data6, 2)
# 	mesg = str(data) + " " + str(data2) + " " + str(data3) + " " + str(data4) + " " + str(data5) + " " + str(data6)
# 	# print msg
# 	pygame.event.pump()
# 	time.sleep(0.05)
        
# 	return mesg
        


#setup pyFirmata
# board =  pyfirmata.Arduino('/dev/cu.usbmodem1411')

# #setup an iterator for safety
# iter8 = pyfirmata.util.Iterator(board)
# iter8.start()

# #locate pins
# pin9 = board.get_pin('d:9:s') #motor 1
# # pin8 = board.get_pin('d:8:s') #motor 2

# def move1(a):
#     pin9.write(a)

# def move2(a):
#     pin8.write(a)

########Multiple clients connect to a server than send and receive data to all clients
def chat_client():
    if(len(sys.argv) < 3) :
        print 'Usage : python chat_client.py hostname port'
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()
     
    print 'Connected to remote host. You can start sending messages'
    sys.stdout.write('[Me] '); sys.stdout.flush()
     
    while 1:
        socket_list = [sys.stdin, s]
         
        # Get the list sockets which are readable
        ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
         
        for sock in ready_to_read:             
            if sock == s:
                # incoming message from remote server, s
                data = sock.recv(4096)
                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :
                    #print data
                    sys.stdout.write("data received")
                    sys.stdout.write("\n")
                    datalist = data.split()
                    motor1val = int(float(datalist[3])*80+90) if (float(datalist[3]) > 0.1 or float(datalist[3]) < -0.1) else 90
                    # move1(motor1val)
                    print motor1val
                    sys.stdout.write('[Me] '); sys.stdout.flush()     
            
            else :
                # user entered a message
                msg = "\n"
                s.send('\n')
                time.sleep(0.1)
                sys.stdout.write('[Me] \n'); sys.stdout.flush() 
                
                
if __name__ == "__main__":

    sys.exit(chat_client())
