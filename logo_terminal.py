#!/usr/bin/python

import serial
import time
import asyncio
import pygame
pygame.init()
import math
import threading
import tkinter
import tkinter.ttk as ttk
from tkinter import *
gui = Tk()
gui.title("UART Interface")
# define the RGB value for white,
#  green, blue colour .
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0,0,0)
 
# assigning values to X and Y variable
X = 1024
Y = 768
 
# create the display surface object
# of specific dimension..e(X, Y).
#display_surface = pygame.display.set_mode((X, Y))
 
# set the pygame window name
#pygame.display.set_caption('Show Text')
 
# create a font object.
# 1st parameter is the font file
# which is present in pygame.
# 2nd parameter is size of the font

 
# create a text surface object,
# on which text is drawn on it.

# create a rectangular object for the
# text surface object

 
# set the center of the rectangular object.

 


#initialization and open the port

#possible timeout values:
#    1. None: wait forever, block call
#    2. 0: non-blocking mode, return immediately
#    3. x, x is bigger than 0, float allowed, timeout block call

ser = serial.Serial()
#ser.port = "/dev/ttyUSB0"
ser.port = "COM5"
#ser.port = "/dev/ttyS2"
ser.baudrate = 9600
ser.bytesize = serial.EIGHTBITS #number of bits per bytes
ser.parity = serial.PARITY_NONE #set parity check: no parity
ser.stopbits = serial.STOPBITS_ONE #number of stop bits
#ser.timeout = None          #block read
ser.timeout = 1            #non-block read
#ser.timeout = 2              #timeout block read
ser.xonxoff = True     #disable software flow control
ser.rtscts = False     #disable hardware (RTS/CTS) flow control
ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
ser.writeTimeout = 2     #timeout for write
lines = ['te',' te',' tes',' te',' test','']
 
import turtle
screen = turtle.Screen()
screen.screensize(800, 600)
tortue = turtle.Turtle()
screen.tracer(100,0)

def print_cube(ser,pygame,lines):
    while(True):
        
        response = ser.readline().decode()
        if response != '':
            print(response)
            command_processor(response.strip())
            #lines.append(response)
            #screen(pygame,lines)
            #text = ""
            #try:
                #for i in range(5,1,-1):
                    #text += '\n' + lines[len(lines)-i]
            #except Exception as e:
                #pass
            #display_surface.fill(pygame.Color('black')) 
            #font = pygame.font.Font('freesansbold.ttf', 32)    
            #blit_text(display_surface, text, (20, 20), font)
            #pygame.display.update()   
commands = ['to','fd','bk','rt','lt','forward','back','right','left','setxy','shiftxy','catalog','help','stop','scale','home','seth','setheading','towards','penup','pendown','pu','pd','readpict','repeat','xcor','ycor','clear','end']
commands_novalue = ['penup','pendown','pu','pd','home','catalog','help','xcor','ycor','clear','stop','end']
modifier = 0.1
def command_processor(command):
    command = command.replace("?","")
    if command != '':
        #pygame.event.get()
        command = command.lower()
        sum_command = command.split(" ")[0]
        if sum_command in commands:    
            if 'repeat' in command:
                #repeat_word_count = command.count('repeat')
                repeat_array = command.split("repeat ")
                for preitem in repeat_array:
                    if str(preitem) != '':
                        times = int(preitem.split('[')[0].strip())
                        item = preitem.split('[')[1]
                        subcommands = []
                        buffer = ''
                        new_command = ''
                        for char in item:
                            if char == ' ' or char == ']':
                                is_integer = True
                                try:
                                    if int(buffer) == buffer:
                                        is_integer = True
                                except Exception as e:
                                    is_integer = False
                                if is_integer == False:
                                    if buffer == ']' or buffer in commands_novalue:
                                        if buffer in commands_novalue:
                                            new_command = buffer
                                        subcommands.append(new_command)
                                        new_command = ''
                                        buffer = ''
                                        if char == ']': break
                                    elif buffer in cat:
                                        new_command = buffer
                                        subcommands.append(new_command)
                                        buffer = ''
                                    else:
                                        new_command = buffer + ' '
                                        buffer = ''
                                else:
                                    new_command += str(buffer)
                                    subcommands.append(new_command)
                                    new_command = ''
                                    buffer = ''
                                    if char == ']': break
                            else:
                                buffer += char
                        for i in range(times):
                            for cmd in subcommands:
                                command_processor(cmd)
            elif 'setxy' in command or 'goto' in command:
                coords = command.replace(')','').split('(')[1].replace('(','').replace(' ','').strip()
                x = int(coords.split(',')[0])
                y = int(coords.split(',')[1])
                tortue.goto(x,y)
                tortue.screen.update()
        
                tortue.screen.listen()
            elif 'shiftxy' in command:
                coords = command.replace(')','').split('(')[1].replace('(','').replace(' ','').strip()
                x = int(coords.split(',')[0]) #* modifier
                y = int(coords.split(',')[1])#* modifier
                if x == 0 and y == 0:
                        pass
                else:
                    targetx = tortue.xcor() + x
                    targety = tortue.ycor() + y
                    angle = calculate_angle(tortue.xcor(),tortue.ycor(),targetx,targety)
                    # opposite_angle = (angle + 180) % 360
                    # angle_diff = abs(self.bearing - angle)
                    # oangle_diff = (self.bearing - opposite_angle)
                    # if oangle_diff < angle_diff: flipped = True
                    distance = calculate_distance(tortue.xcor(),tortue.ycor(),targetx,targety)
              
                    tortue.seth(angle)
                    tortue.fd(distance * modifier)
                    #self.x = targetx
                    #self.y = targety 
                    #tortue.goto(int(tortue.xcor())+ x,int(tortue.ycor()) + y)
                    tortue.screen.update()
        
                    tortue.screen.listen()
            elif 'fd' in command:
                distance = command.split(' ')[1].strip()
                distance = int(distance) * modifier
                tortue.fd(distance)
                tortue.screen.update()
                tortue.screen.listen()
            elif 'scale' in command:
                scalar = command.split(' ')[1].strip()
                #self.scale(scalar)
            elif 'pu' in command:
                tortue.pu()
                tortue.screen.update()
        
                tortue.screen.listen()
            elif 'pd' in command:
                tortue.pd()
                tortue.screen.update()
                tortue.screen.listen()
            elif 'bk' in command:
                distance = command.split(' ')[1].strip()
                tortue.bk(int(distance))
            elif 'rt' in command:
                degrees = command.split(' ')[1].strip()
                tortue.rt(degrees)
                tortue.screen.update()
                tortue.screen.listen()
            elif 'lt' in command:
                degrees = command.split(' ')[1].strip()
                tortue.lt(degrees)
                tortue.screen.update()
                tortue.screen.listen()
            elif 'setx' in command:
                xcord = int(command.split(' ')[1].strip())
                tortue.setx(int(xcord))
                tortue.screen.update()
                tortue.screen.listen()
            elif 'sety' in command:
                ycord = int(command.split(' ')[1].strip())
                tortue.sety(int(ycord))
                tortue.screen.update()
                tortue.screen.listen()
            elif 'stop' in command:
                #self.stopping = True
                pass
            elif 'catalog' in command:
                #self.catalog(0)
                pass
            elif 'help' in command:
                #self.help()
                pass
            elif 'clear' in command:
                tortue.clear()
                tortue.screen.update()
                tortue.screen.listen()
            elif 'xcor' in command:
                #self.log(0,str(self.xcor()))
                pass
            elif 'ycor' in command:
                #self.log(0,str(self.ycor()))
                pass
            elif 'heading' in command:
                #self.log(0,str(self.heading()))
                pass
            elif 'towards' in command:
                coords = command.replace(')','').split('(')[1].replace('(','').replace(' ','').strip()
                x = int(coords.split(',')[0])
                y = int(coords.split(',')[1])
                tortue.towards(x,y)
                tortue.screen.update()
                tortue.screen.listen()
            elif 'home' in command:
                tortue.home()
                tortue.screen.update()
                tortue.screen.listen()
            elif 'seth' in command:
                heading = int(command.split(' ')[1].strip())
                tortue.seth(heading)
                tortue.screen.update()
                tortue.screen.listen()
        else:
            had_entry = False
    
def calculate_angle(originx,originy,targetx,targety):
        p1 = (float(originx),float(originy))
        p2 = (float(targetx),float(targety))
        dx = targetx - originx
        dy = targety - originy
        theta = math.atan2(dy, dx)
        degrees = math.degrees(theta)
        return degrees
def calculate_distance(originx,originy,targetx,targety):
    distance = ((originx - targetx)**2 + (originy - targety)**2)**0.5
    return distance


def blit_text(surface, text, pos, font, color=pygame.Color('green')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


text = "This is a really long sentence with a couple of breaks.\nSometimes it will break even if there isn't a break " \
       "in the sentence, but that's because the text is too long to fit the screen.\nIt can look strange sometimes.\n" \
       "This function doesn't check if the text is too high to fit on the height of the surface though, so sometimes " \
       "text will disappear underneath the surface"
font = pygame.font.SysFont('Arial', 64)


def print_square(ser,pygame,lines):
    #while(True):
    try:
        ser.flushInput() #flush input buffer, discarding all its contents
        ser.flushOutput()#flush output buffer, aborting current output 
                    #and discard all that is in buffer

        #write data
        #ser.write("connect".encode())
        #ser.write("help".encode())
        ser.write(('\r\n').encode())
        time.sleep(10)
        ser.write(('to house' + '\r\n').encode())
        time.sleep(2)
        file1 = open('./pict_catalog/house.log', 'r')
        for line in file1:
            inp = line + '\r\n'
            ser.write(inp.encode())
            print(inp)
            time.sleep(0.5)  #give the serial port sometime to receive the data
            response = ser.readline().decode()
        ser.write(('end' + '\r\n').encode())
        
        #time.sleep(2)
        #file1.write(self.code)
        #file1.close()
        #f = file.write(".\\pict_catalog\\house.log")
        #inp = input("?")
        #lines.append(inp)
        #screen(pygame,lines)
        #text = ""
        #try:
            #for i in range(5,1,-1):
                #text += '\n' + lines[len(lines)-i]
        #except Exception as e:
            #pass
        #display_surface.fill(pygame.Color('black'))  
        #font = pygame.font.Font('freesansbold.ttf', 32)   
        #blit_text(display_surface, text, (20, 20), font)
        #pygame.display.update()   
        #ser.write(inp.encode())
        #print("write data: help")
        
        
        #numOfLines = 0

        #while True:
            

        #numOfLines = numOfLines + 1

        #if (numOfLines >= 5):
            #break

        #ser.close()
    except Exception as e1:
        print("error communicating...: " + str(e1))

          
if __name__ == "__main__":
    
    try: 
        ser.open()
    except Exception as e:
        print("error open serial port: " + str(e))
        exit()

    if ser.isOpen():

        pass

    else:
        print("cannot open serial port ")
    # creating thread
    #t1 = threading.Thread(target=print_square, args=(ser,pygame,lines))
    #t2 = threading.Thread(target=print_cube, args=(ser,pygame,lines))
    #t3 = threading.Thread(target=screen, args=(pygame,lines))
    # starting thread 1
    print_cube(ser,pygame,lines)
    #t1.start()
    # starting thread 2
    #t2.start()
    #t3.start()
    # wait until thread 1 is completely executed
    #t1.join()
    # wait until thread 2 is completely executed
    #t2.join()
    #t3.join()
    #print_square(ser,pygame,lines)
    
    # both threads completely executed
    print("Done!")