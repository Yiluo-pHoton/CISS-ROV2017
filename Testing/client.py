import sys
import socket
import select
import pygame
import time
import pyfirmata

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputing the
# information.
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def printf(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height
        
    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15
        
    def indent(self):
        self.x += 10
        
    def unindent(self):
        self.x -= 10

########Below is superfluous code necessary only for receiving and sending controller input
pygame.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()


def print_data(joystickTemp):
    dataList = []
    for i in range(6):
        dataList.append(round(joystickTemp.get_axis(i), 2))
    for i in range(5):
        dataList.append(round(joystickTemp.getbutton(i), 2))
        
    mesg = " ".join(dataList)
    pygame.event.pump()
    time.sleep(0.05)
    print mesg
    return mesg 
        

#setup pyFirmata
board =  pyfirmata.Arduino('/dev/cu.usbmodem1421')

#setup an iterator for safety
iter8 = pyfirmata.util.Iterator(board)
iter8.start()

#locate pins
pin9 = board.get_pin('d:9:s') #motor 1
pin8 = board.get_pin('d:8:s') #motor 2

def move1(a):
    pin9.write(a)

def move2(a):
    pin8.write(a)

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
     
    while True:
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
                    sys.stdout.write(data)
                    sys.stdout.write('[Me] '); sys.stdout.flush()     
            
            else :
                # user entered a message
                msg = print_data()
                s.send(msg)
                sys.stdout.write(msg + '\n[Me]'); sys.stdout.flush() 

if __name__ == "__main__":
    sys.exit(chat_client())
