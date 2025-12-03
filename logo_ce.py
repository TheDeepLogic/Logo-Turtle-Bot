onPC = True
MotorsEnabled = True
if onPC:
    import turtle
    import glob
    screen = turtle.Screen()
    screen.screensize(800, 600)
    tortue = turtle.Turtle()
    screen.tracer(100,0)
else:
    #import logo_motor as motor
    from machine import Pin, PWM, UART #, SPI
    import _thread
    from time import ticks_ms, ticks_diff,sleep_ms
    #m1 = HalfStepMotor.frompins(5,4,3,2)
    #m2 = HalfStepMotor.frompins(6,7,8,9)
    s1 = PWM(Pin(22))
    s1.freq(50)
    uart = UART(0, baudrate=9600)
import os
from time import sleep
import math
import re
from math import acos, cos, sin, radians, atan2
import pict_catalog.logo_pict_catalog as pict
import pict_catalog.logo_pict_python_logo as python_logo
class Bluetooth:
    def __init__(self,ce):
        self.ce = ce
        self.connected = False
    def poll(self):
        if onPC == False:
            if uart.any():
                character = str(uart.read(64).decode("utf-8"))
                print('Received:',character)
                if self.connected == False:
                    self.connected = True
                    uart.write('\r\n'+ self.ce.banner)
                    uart.write('WELCOME TO LOGO\r\n?')
                else:
                    if '\r' in character or '\n' in character:
                        
                        '''uart.write('\r\n')'''
                        FULL_COMMAND = ''
                        if len(character) > 1:
                            self.ce.command_values.append(character)
                        for char in self.ce.command_values:
                            if char != '\n' and char != '\r':
                                FULL_COMMAND += str(char)
                        self.ce.command_values = []
                        '''if FULL_COMMAND == '': FULL_COMMAND = character'''
                        self.ce.run_command(FULL_COMMAND,self.ce)
                    elif '~' in character:
                        del self.ce.command_values[-1]
                        uart.write(character)
                    else:
                        uart.write(character.upper())
                        self.ce.command_values.append(character)
            
class Motor:
    stepms = 10

    # Do be defined by subclasses
    maxpos = 0
    states = []
    
    def __init__(self, p1, p2, p3, p4, stepms=None):
        self.pins = [p1, p2, p3, p4]

        if stepms is not None:
            self.stepms = stepms
  
        self._state = 0
        self._pos = 0
        self.stopping = False
    def __repr__(self):
        return '<{} @ {}>'.format(
            self.__class__.__name__,
            self.pos,
        )

    @property
    def pos(self):
        return self._pos

    @classmethod
    def frompins(cls, *pins, **kwargs):
        return cls(*[Pin(pin, Pin.OUT) for pin in pins],
                   **kwargs)

    def zero(self):
        self._pos = 0

    def _step(self, dir):
        state = self.states[self._state]

        for i, val in enumerate(state):
            self.pins[i].value(val)

        self._state = (self._state + dir) % len(self.states)
        self._pos = (self._pos + dir) % self.maxpos

    def step(self, steps):
        dir = 1 if steps >= 0 else -1
        steps = abs(steps)
        #count = 0
        #btp = 50
        for _ in range(steps):
            #count +=1
            #if count == btp:
                #pass
            #if self.stopping: break
            
            t_start = ticks_ms()

            self._step(dir)

            t_end = ticks_ms()
            t_delta = ticks_diff(t_end, t_start)
            sleep_ms(self.stepms - t_delta)

    def step_until(self, target, dir=None):
        if target < 0 or target > self.maxpos:
            raise ValueError(target)

        if dir is None:
            dir = 1 if target > self._pos else -1
            if abs(target - self._pos) > self.maxpos/2:
                dir = -dir

        while True:
            if self._pos == target:
                break
            self.step(dir)

    def step_until_angle(self, angle, dir=None):
        if angle < 0 or angle > 360:
            raise ValueError(angle)

        target = int(angle / 360 * self.maxpos)
        self.step_until(target, dir=dir)


class FullStepMotor(Motor):
    stepms = 5
    maxpos = 2048
    states = [
        [1, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 1],
        [1, 0, 0, 1],
    ]


class HalfStepMotor(Motor):
    stepms = 3
    maxpos = 4096
    states = [
        [1, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 1],
        [1, 0, 0, 1],
    ]
if onPC == False:
    #import logo_motor as motor
    m1 = HalfStepMotor.frompins(5,4,3,2)
    m2 = HalfStepMotor.frompins(6,7,8,9)
class command_engine:
    def __init__(self):
        #ALL PHYSICAL VALUES IN CM
        self.onPC = onPC
        self.logging = True
        self.verbose_logging = False
        self.bearing = 0
        self.dprot = 7050
        self.ppr = 4096 #pulses per revolution
        self.dpr = 20.18 #distance per revolution
        self.pw = 45
        self.ph = 45
        self.dw = 0
        self.dh = 0
        self.x = 0
        self.y = 0
        self.modifier = 1 #8
        self.xoffset = 0
        self.yoffset = 0
        self.downposition = 3800
        self.upposition = 4450 #3800
        self.pendropspeed = 0.5
        self.penposition = -1
        self.speed = 10
        self.bluetooth = Bluetooth(self)
        self.banner = "THE TERRAPIN LOGO LANGUAGE\r\n\r\nWRITTEN BY L. KLOTZ, P. SOBALVARRO\r\nAND S. HAIN UNDER THE SUPERVISION\r\nOF H. ABELSON\r\n\r\nCOPYRIGHT (C) 1981 MIT\r\nPORTIONS COPYRIGHT (C) 2023 AARON SMITH\r\nVERSION 1.0\r\n\r\n"
        self.command_values = []
        self.routine_write = False
        if self.onPC == False: self.baton = _thread.allocate_lock()
        self.code = ''
        self.code_name = ''
        self.cat = self.catalog()
        self.stopping = False
        self.load_configuration()
        self.configure()
        self.log(0,self.banner.replace('\r\n','\n'))
        self.command_list = [['pu','penup',False,'Raises the pen','pu',None,[None,None],False]]
        self.command_list.append(['pd','pendown',False,'Lowers the pen','pd',None,[None,None],False])
        self.command_list.append(['fd','forward',True,'Moves the turtle forward','fd 50',float,[-9999999.00,9999999.00],False])
        self.command_list.append(['bk','backward',True,'Moves the turtle backward','bk 50',float,[-9999999.00,9999999.00],False])
        self.command_list.append(['lt','left',True,'Rotates the turtle to the left','lt 90',float,[-9999999.00,9999999.00],False])
        self.command_list.append(['rt','right',True,'Rotates the turtle to the right','rt 90',float,[-9999999.00,9999999.00],False])
        self.command_list.append(['setxy','setxy',True,'Sets the X and Y coordinates','setxy (0,15)',tuple,[None,None],False])
        self.command_list.append(['shiftxy','shiftxy',True,'Shifts the turtle by the specified number of steps on the X and Y coordinates','shiftxy (-15,20)',tuple,[None,None],False])
        self.command_list.append(['seth','setheading',True,'Sets the heading of the turtle in degrees','seth 90.75',float,[0,360],False])
        self.command_list.append(['heading','heading',False,'Returns the heading of the turtle in degrees','heading',None,[None,None],True])
        self.command_list.append(['towards','towards',True,'Rotates the turtle towards the specified X and Y coordinates','towards (0,15)',tuple,[None,None],False])
        self.command_list.append(['home','home',False,'Moves the turtle to the home coordinates of (0,0)','home',None,[None,None],False])
        self.command_list.append(['xcor','xcoordinate',False,'Returns the current X coordinate of the turtle','xcor',None,[None,None],True])
        self.command_list.append(['ycor','ycoordinate',False,'Returns the current Y coordinate of the turtle','ycor',None,[None,None],True])
        self.command_list.append(['readpict','readpicture',True,'Reads the specified picture file and begins drawing','readpict triangle',str,[3,32],False])
        self.command_list.append(['repeat','repeat',True,'Repeats commands the specified number of times','repeat 4 [rt 90 fd 100]',int,[1,100000],False])
        self.command_list.append(['stop','stop',False,'Stops the turtle from excuting further commands','stop',None,[None,None],False])
        self.command_list.append(['to','to',True,'Begins program creation mode with the filename specified','to triangle',str,[3,32],False])
        self.command_list.append(['end','end',False,'Ends program creation mode and writes the commands entered to the file','end',None,[None,None],False])
        self.command_list.append(['showvalue','showvalue',True,'Returns the evaluation of the specified value by the Micropython interpreter used to execute Logo','showvalue 14/5, showvalue logo.dprot',str,[1,100000],True])
        self.command_list.append(['clear','clear',False,'Clears the screen when running Logo on your PC','clear',None,[None,None],False])
        self.command_list.append(['help','help',False,'Returns this help','help',None,[None,None],True])
        self.command_list.append(['catalog','catalog',False,'Returns a list of picture files on the disk','catalog',None,[None,None],True])
        self.command_list.append(['scale','scale',True,'Sets a value that will be used to factor step values','scale 15',float,[1,100000],False])
        self.command_list.append(['setr','setrotationratio',True,'Sets a value (cm) that indicates how far the turtle physically moves per degree instructed','setr 19.7',float,[1,10000],False])
        self.command_list.append(['setpw','setpagewidth',True,'Sets a value (cm) that indicates page width','setpw 45',float,[1,1000],False])
        self.command_list.append(['setph','setpageheight',True,'Sets a value (cm) that indicates page height','setpw 45',float,[1,1000],False])
        self.command_list.append(['setdpr','setdistanceperrevolution',True,'Sets a value (cm) that indicates how far the turtle physically moves per one wheel revolution','setdpr 20.5',float,[1,100000],False])
        self.command_list.append(['setppr','setpulsesperrevolution',True,'Sets a value that indicates how many pulses it takes the motors to achieve one wheel revolution','setppr 4096',float,[1,100000],False])
        self.command_list.append(['setpu','setpenup',True,'Sets a value that indicates the servo motor duty cycle to be used for the penup position','setpu 4000',int,[0,65000],False])
        self.command_list.append(['setpd','setpendown',True,'Sets a value that indicates the servo motor duty cycle to be used for the penup position','setpd 3500',int,[0,65000],False])
        self.command_list.append(['setpds','setpendropspeed',True,'Sets a value that indicates the amount of time to allow for the pen to be dropped before again moving the turtle','setpds 0.5',float,[0,60],False])
        self.command_list.append(['setspeed','setspeed',True,'Sets a value (1-10) that indicates at what speed to move the turtle','setspeed 10',int,[1,10],False])
    def process_command_string(self,precommand):
        command = precommand.lower().strip()
        monitored_characters = ['+',']','[',')','(','/','-',',','*']
        command = ' '.join(command.split())
        for i in range (10):
            for character in monitored_characters:
                if character != '[' and character != '(': command = command.replace(' '*i + character,character)
                if character != ']' and character != ')': command = command.replace(character + ' '*i,character)
        command = command.replace('[','[ ')
        command = command.replace(']',' ]')
        commands_to_execute = []
        commands_with_issues = []
        word_index = -1
        char_index = -1
        value_index = -2
        buffered_command = ''
        command_list_index = -1
        jump_to_index = -1
        for word in command.split(' '):
            word_index +=1
            char_index += len(word) + 1
            word = word.lower()
            if word_index != value_index and word_index >= jump_to_index:
                problem_word = True
                current_command_list_index = -1
                for command_entry in self.command_list:
                    current_command_list_index += 1
                    if word == str(command_entry[0]) or word == str(command_entry[1]):
                        command_list_index = current_command_list_index
                        problem_word = False
                        if command_entry[2]:
                            value_index = word_index + 1
                            buffered_command = word
                        else:
                            commands_to_execute.append([word,None,None])
                if problem_word:
                    if len(word) > 2 and word.upper() in self.cat:
                        command_list_index = current_command_list_index
                        problem_word = False
                        commands_to_execute.append(['readpict',word,None])
            elif word_index == value_index:
                failure_type = ''
                passed_validation = False
                if self.command_list[command_list_index][5] == int:
                    passed_validation = True
                    try:
                        if int(word) == word:
                            passed_validation = True
                            word = int(word)
                            if word < self.command_list[command_list_index][6][0]:
                                passed_validation = False
                                failure_type = buffered_command + ' WILL NOT ACCEPT A VALUE LOWER THAN ' + str(self.command_list[command_list_index][5][0])
                            if word > self.command_list[command_list_index][6][1]:
                                passed_validation = False
                                failure_type = buffered_command + ' WILL NOT ACCEPT A VALUE HIGHER THAN ' + str(self.command_list[command_list_index][5][1])
                    except Exception as e:
                        passed_validation = False
                        failure_type = buffered_command + ' WILL NOT ACCEPT THE TYPE OF VALUE "' + str(word) + '" REPRESENTS'
                elif self.command_list[command_list_index][5] == float:
                    passed_validation = True
                    try:
                        if float(word) == word or word.split('.')[0] == str(float(word)).split('.')[0]:
                            passed_validation = True
                            word = float(word)
                            if word < self.command_list[command_list_index][6][0]:
                                passed_validation = False
                                failure_type = buffered_command + ' WILL NOT ACCEPT A VALUE LOWER THAN ' + str(self.command_list[command_list_index][5][0])
                            if word > self.command_list[command_list_index][6][1]:
                                passed_validation = False
                                failure_type = buffered_command + ' WILL NOT ACCEPT A VALUE HIGHER THAN ' + str(self.command_list[command_list_index][5][1])
                    except Exception as e:
                        passed_validation = False
                        failure_type = buffered_command + ' WILL NOT ACCEPT THE TYPE OF VALUE "' + str(word) + '" REPRESENTS'
                elif self.command_list[command_list_index][5] == tuple:
                    passed_validation = True
                    try:
                        if tuple(word) == word:
                            passed_validation = True
                            word = tuple(word)
                    except Exception as e:
                        passed_validation = False
                    if ',' in word == False:
                        passed_validation = False
                    if passed_validation == False: failure_type = buffered_command + ' WILL NOT ACCEPT THE TYPE OF VALUE "' + word + '" REPRESENTS'
                elif self.command_list[command_list_index][5] == str:
                    passed_validation = True
                    try:
                        if str(word) == word:
                            passed_validation = True
                            word = str(word)
                        if len(word) < self.command_list[command_list_index][6][0]:
                            passed_validation = False
                            failure_type = buffered_command + ' WILL NOT ACCEPT A VALUE WITH LESS THAN ' + str(self.command_list[command_list_index][5][0]) + ' CHARACTERS'
                        if len(word) > self.command_list[command_list_index][6][1]:
                            passed_validation = False
                            failure_type = buffered_command + ' WILL NOT ACCEPT A VALUE WITH MORE THAN ' + str(self.command_list[command_list_index][5][1]) + ' CHARACTERS'
                    except Exception as e:
                        passed_validation = False
                        failure_type = buffered_command + ' WILL NOT ACCEPT THE TYPE OF VALUE "' + str(word) + '" REPRESENTS'
                if passed_validation:  
                    if buffered_command == 'repeat':
                        if '[' not in command[char_index + len(word)+1:len(command)]  and ']' not in command[char_index + len(word)+1:len(command)] :
                            passed_validation = False
                            failure_type = buffered_command + ' NEEDS OPENING AND CLOSING BRACKETS'
                            commands_with_issues.append([buffered_command,word,failure_type])
                        else:
                            repeat_block = ''
                            closing_right_bracket_index =  command.find(']',char_index,len(command))-1
                            repeat_block = command[char_index + len(word)+1:closing_right_bracket_index]
                            if command[char_index + len(word)] != '[':
                                passed_validation = False
                                failure_type = buffered_command + ' NEEDS OPENING AND CLOSING BRACKETS'
                                commands_with_issues.append([buffered_command,word,failure_type])
                            else:
                                try:
                                    repeat_block_word_count = len(repeat_block.split(' '))
                                    repeats = repeat_block.count('repeat')
                                    if repeats > 0 or 'repeat' in repeat_block or ']' in repeat_block:
                                        commands_with_issues.append([buffered_command,word,'CHECK FOR MISCPLACED BRACKETS'])
                                    else:
                                        repeat_results = self.process_repeat_strings([buffered_command,word,repeat_block])
                                        if len(repeat_results[1]) > 0: commands_with_issues.append(repeat_results[1])
                                        for result in repeat_results[0]:
                                            commands_to_execute.append(result)
                                    jump_to_index = word_index + repeat_block_word_count + 1
                                except Exception as e:
                                    passed_validation = False
                                    failure_type = buffered_command + ' WILL NOT ACCEPT A VALUE WITHOUT BRACKETS: ' + str(e).upper
                                    commands_with_issues.append([buffered_command,word,failure_type])
                    else:
                        if buffered_command == 'showvalue':
                            word = precommand.split(' ')[1]    
                        commands_to_execute.append([buffered_command,word,None])
                    buffered_command = ''
                else:
                    commands_with_issues.append([buffered_command,word,failure_type])
                    buffered_command = ''
        return([commands_to_execute,commands_with_issues])
    def process_repeat_strings(self,command):
        commands_with_issues = []
        commands_to_execute = []
        if command[0] == 'repeat':
            results = self.process_command_string(command[2])
            for i in range(int(command[1])):
                for result in results[0]:
                    commands_to_execute.append(result)
            if len(results[1]) > 0: commands_with_issues.append(results[1])
        return [commands_to_execute,commands_with_issues]
    def run_command(self,command,ce):
        if onPC == False: m1.stopping = False
        if onPC == False: m2.stopping = False
        self.stopping = False
        ir = self.process_command_string(command)
        ir_issues = ir[1]
        ir_commands = ir[0]
        self.process_output(ir_issues,ir_commands,ce)
    def process_output(self,commands_with_issues,commands_to_execute,ce):
        ret = []
        if len(commands_with_issues) > 0:
            for entry in commands_with_issues:
                #print(str(entry[2]))
                self.log(1,str(entry[2]).upper())
        else:
            if len(commands_to_execute) == 0:
                self.log(1,'NO COMMAND RECOGNIZED')
            else:
                for entry in commands_to_execute:
                    if entry[1] != None:
                        if self.verbose_logging: self.log(1,str(entry[0]).upper() + ' ' + str(entry[1]).upper())
                    else:
                        if self.verbose_logging: self.log(1,entry[0].upper())
                    reference_command = []
                    index = -1
                    for command_entry in self.command_list:
                        index +=1
                        if entry[0] == str(command_entry[0]) or entry[0] == str(command_entry[1]):
                            reference_command = self.command_list[index]
                            break
                    if reference_command[7]:
                        if reference_command[1] == 'catalog':
                            self.log(1,str('\r\n'.join(self.execute_command(reference_command[0],entry[1],True,ce))).upper())
                        else:
                            self.log(1,str(self.execute_command(reference_command[0],entry[1],True,ce)))
                    else:
                        self.execute_command(reference_command[0],entry[1],False,ce)
        if onPC == False: self.log(2,'?')
    def execute_command(self,command,value,return_output,ce):
        self.bluetooth.poll()
        method_name = command
        my_cls = ce
        method = None
        ret = ''
        proceed = False
        try:
            method = getattr(my_cls, method_name)
            proceed = True
        except AttributeError:
            #raise NotImplementedError("Class `{}` does not implement `{}`".format(my_cls.__class__.__name__, method_name))
            ret = 'THERE IS NO FUNCTION NAMED ' + str(method_name).upper()
            self.log(1,ret)
            proceed = False
        if value != None and proceed:
            if  ',' in str(value):
                try:
                    pass_value1 = float(value.replace('(','').replace(')','').split(',')[0].strip())
                    pass_value2 = float(value.replace('(','').replace(')','').split(',')[1].strip())
                    if return_output:
                        ret = method(pass_value1,pass_value2)
                    else:
                        method(pass_value1,pass_value2)
                except Exception as e:
                    self.log(1,str(command).upper() + ' DID NOT LIKE THE VALUE ' + str(value).upper())
            else:
                if return_output:
                    ret = method(value)
                else:
                    if command == 'readpict':
                        method(value,ce)
                    else:
                        try:
                            method(value)
                        except Exception as e:
                            self.log(1,str(command).upper() + ' DID NOT LIKE THE VALUE ' + str(value).upper())
        elif proceed:
            if return_output:
                ret = method()
            else:
                method()
        if self.onPC: screen.update()
        if return_output: return ret
    def configure(self):
        self.dpp = self.dpr / self.ppr #distance per pulse
        self.pppw = self.pw / self.dpp #pulses per page width
        self.ppph = self.ph / self.dpp #pulses per page height
        self.cat = self.catalog()
    def load_configuration(self):
        try:
            config_file = open('config.txt', 'r')
            count = 1
            for line in config_file:
                if count == 1:
                    self.dprot = float(line.strip())
                elif count == 2:
                    self.pw = float(line.strip())
                elif count == 3:
                    self.ph = float(line.strip())
                elif count == 4:
                    self.dpr = float(line.strip())
                elif count == 5:
                    self.ppr = float(line.strip())
                elif count == 6:
                    self.upposition = int(line.strip())
                elif count == 7:
                    self.downposition = int(line.strip())
                elif count == 8:
                    self.speed = int(line.strip())
                elif count == 9:
                    self.modifier = float(line.strip())
                elif count == 10:
                    self.pendropspeed = float(line.strip())
                else:
                    count -=1
                count +=1
            config_file.close()
        except Exception as e:
            self.save_configuration()
    def save_configuration(self):
        config_file = open('config.txt', 'w')
        res = str(self.dprot) + '\r\n' + str(self.pw) + '\r\n' + str(self.ph) + '\r\n' + str(self.dpr) + '\r\n' + str(self.ppr) + '\r\n' + str(self.upposition) + '\r\n' + str(self.downposition) + '\r\n' + str(self.speed) + '\r\n' + str(self.modifier) + '\r\n' + str(self.pendropspeed)
        config_file.write(res)
        config_file.close()
    def movepen(self,position):
        s1.duty_u16(position)
        sleep(0.01) 
    def movemotors(self,phase,dir,steps):
        if phase == 1:
            if dir == 'fd':
                if self.speed == 1:
                    for i in range(steps):
                        m1.step(-1)
                        m2.step(1)
                else:
                    for i in range(11- self.speed):
                        self.baton.acquire()
                        _thread.start_new_thread(self.movemotors, (2, 'fd',steps/(11-self.speed)))
                        m1.step(-steps/(11-self.speed))
            elif dir == 'bk':
                if self.speed == 1:
                    for i in range(steps):
                        m1.step(1)
                        m2.step(-1)
                else:
                    for i in range(11- self.speed):
                        self.baton.acquire()
                        _thread.start_new_thread(self.movemotors, (2, 'bk',-steps/(11-self.speed)))
                        m1.step(steps/(11-self.speed))
            elif dir == 'rt':
                if self.speed == 1:
                    for i in range(steps):
                        m1.step(-1)
                        m2.step(-1)
                else:
                    for i in range(11- self.speed):
                        self.baton.acquire()
                        _thread.start_new_thread(self.movemotors, (2, 'rt',-steps/(11-self.speed)))
                        m1.step(-steps/(11-self.speed))
            elif dir == 'lt':
                if self.speed == 1:
                    for i in range(steps):
                        m1.step(1)
                        m2.step(1)
                else:
                    for i in range(11- self.speed):
                        self.baton.acquire()
                        _thread.start_new_thread(self.movemotors, (2, 'lt',steps/(11-self.speed)))
                        m1.step(steps/(11-self.speed))
        elif phase == 2:
            m2.step(steps)
            self.baton.release()
    def set_ratio(self,image_width,image_height,hx,lx,hy,ly):
        new_image_width = image_width
        new_image_height = image_height
        while new_image_width < self.pppw - 5 or new_image_width > self.pppw :
            if new_image_width > (self.pppw):
                new_image_width = new_image_width - 1
                new_image_height = new_image_height - 1
            elif new_image_width < (self.pppw):
                new_image_width = new_image_width + 1
                new_image_height = new_image_height + 1
        if new_image_height > self.ppph:
            while new_image_height > self.ppph - 5 :
                new_image_height = new_image_height - 1
                new_image_width = new_image_width - 1
        if new_image_height == 0 or image_height == 0:
            self.modifier = 1
        else:
            self.modifier = new_image_height / image_height
        if self.modifier < 2 and self.modifier > 1 :self.modifier = 1
        self.modifier = self.modifier / 2
        if self.onPC:   
            if new_image_height != 0 and image_height != 0:
                self.modifier = self.modifier * (self.pw /350)
                pass
    def help(self):
        ret = ''
        for entry in self.command_list:
            ret = ret + '\r\n' + 'COMMAND: ' + str(entry[1]).upper() + '\r\nDESCRIPTION: ' + str(entry[3]).upper() + '\r\nEXAMPLE: ' + str(entry[4]).upper() + '\r\n'
        return ret
    def catalog(self):
        dir_path = './pict_catalog'
        res = ""
        for entry in os.listdir(dir_path):
            if '.log' in entry:
                res += entry.replace('.log','').upper() + '\r\n'
        return res.split('\r\n')  
    def to(self,pict):
        self.code_name = pict
        self.routine_write = True
    def end(self):
        pict = self.code_name
        file1 = open('./pict_catalog/' + str(pict) + '.log', 'w')
        file1.write(self.code)
        file1.close()
        self.code = ''
        self.code_name = ''
        self.routine_write = False
        self.configure()
    def fd(self,steps):
        steps = eval(str(steps))
        steps = steps * self.modifier
        if self.onPC:
            tortue.forward(steps)
        else:
            if MotorsEnabled: self.movemotors(1,'fd',steps)
    def showvalue(self,value):
        try:
            ret = eval(str(value))
        except Exception as e:
            ret = 'SHOWVALUE DID NOT LIKE ' + str(value) + ' AS AN INPUT:' + str(e)
        return ret
    def bk(self,steps):
        steps = eval(str(steps))
        steps = steps * self.modifier
        if self.onPC:
            tortue.backward(steps)
        else:
            if MotorsEnabled: self.movemotors(1,'bk',steps)
    def pu(self):
        if self.onPC:
            tortue.pu()
        else:
            if self.penposition != 1:
                self.movepen(self.downposition + int((self.upposition - self.downposition) / 2))
                sleep(0.1)
                self.movepen(self.upposition)
                self.penposition = 1
                sleep(self.pendropspeed)
    def pd(self):
        if self.onPC:
            tortue.pd()
        else:
            if self.penposition != 0:
                self.movepen(self.downposition + int((self.upposition - self.downposition) / 2))
                sleep(0.1)
                self.movepen(self.downposition)
                self.penposition = 0
                sleep(self.pendropspeed)
    def rt(self,degrees):
        degrees = eval(str(degrees))
        if degrees < 0:
            self.lt(degrees)
        else:
            self.bearing = (self.bearing + degrees) % 360
            if self.bearing < 0: self.bearing = 360 + self.bearing
            #steps = degrees * self.dprot
            #steps = int(degrees / 360 * (4096-(degrees / 360)*4096))
            steps = int(degrees / 360 * self.dprot)
            if self.onPC:
                tortue.rt(degrees)
            else:
                if MotorsEnabled: self.movemotors(1,'rt',steps)
    def lt(self,degrees):
        degrees = eval(str(degrees))
        if degrees < 0:
            self.rt(degrees)
        else:
            self.bearing = (self.bearing - degrees) % 360
            if self.bearing < 0: self.bearing = 360 + self.bearing
            #steps = degrees * self.dprot
            #steps = int(degrees / 360 * (4096-(degrees / 360)*4096))
            steps = int(degrees / 360 * self.dprot)
            if self.onPC:
                tortue.lt(degrees)
            else:
                if MotorsEnabled: self.movemotors(1,'lt',steps)
    def stop(self):
        if MotorsEnabled: m1.stopping = True
        if MotorsEnabled: m2.stopping = True
        self.stopping = True
    def clear(self):
        if self.onPC:
            tortue.clear()
    def xcor(self):
        return self.x
    def ycor(self):
        return self.y
    def heading(self):
        return self.bearing
    def towards(self,targetx,targety):
        angle = self.calculate_angle(self.x,self.y,targetx,targety)
        self.seth(angle)
    def home(self):
        self.setxy(0,0)
    def seth(self,heading):
        heading = eval(str(heading))
        if self.bearing > heading:
            if (self.bearing - heading) < ((360-self.bearing) + heading):
                self.lt(self.bearing - heading)
            else:
                self.rt((360-self.bearing) + heading)
        elif heading > self.bearing:
            if (heading - self.bearing) < ((360-heading) + self.bearing):
                self.rt(heading - self.bearing)
            else:
                self.lt((360-heading) + self.bearing)
        self.bearing = heading
    def setx(self,targetx):
        angle = self.calculate_angle(self.x,self.y,targetx,self.y)
        distance = self.calculate_distance(self.x,self.y,targetx,self.y)
        self.towards(targetx,self.y)
        self.fd(distance)
        self.x = targetx 
    def sety(self,targety):
        angle = self.calculate_angle(self.x,self.y,self.x,targety)
        distance = self.calculate_distance(self.x,self.y,self.x,targety)
        self.towards(self.x,targety)
        self.fd(distance)
        self.y = targety 
    def setxy(self,targetx,targety):
        angle = self.calculate_angle(self.x,self.y,targetx,targety)
        distance = self.calculate_distance(self.x,self.y,targetx,targety)
        self.towards(targetx,targety)
        self.fd(distance)
        self.x = targetx
        self.y = targety 
    def shiftxy(self,targetx,targety):
        targetx = self.x + targetx
        targety = self.y + targety
        angle = self.calculate_angle(self.x,self.y,targetx,targety)
        # opposite_angle = (angle + 180) % 360
        # angle_diff = abs(self.bearing - angle)
        # oangle_diff = (self.bearing - opposite_angle)
        # if oangle_diff < angle_diff: flipped = True
        distance = self.calculate_distance(self.x,self.y,targetx,targety)
        self.towards(targetx,targety)
        self.fd(distance)
        self.x = targetx
        self.y = targety
    def scale(self,factor):
        self.modifier = float(factor)
    def setr(self,dprot):
        self.dprot = float(dprot)
        self.save_configuration()
    def setpw(self,value):
        self.pw = float(value)
        self.configure()
        self.save_configuration()
    def setph(self,value):
        self.ph = float(value)
        self.configure()
        self.save_configuration()
    def setdpr(self,value):
        self.dpr = float(value)
        self.configure()
        self.save_configuration()
    def setppr(self,value):
        self.ppr = value
        self.configure()
        self.save_configuration()
    def setpu(self,value):
        self.upposition = int(value)
        self.pu()
        self.save_configuration()
    def setpd(self,value):
        self.downposition = int(value)
        self.pd()
        self.save_configuration()
    def setpds(self,value):
        self.pds = float(value)
        self.save_configuration()
    def setspeed(self,value):
        self.speed = int(value)
        self.save_configuration()
    def readpict(self,filename,ce):
        file1 = open('./pict_catalog/' + str(filename) + '.log', 'r')
        hx = 0
        hy = 0
        lx = 0
        ly = 0
        cx = 0
        cy = 0
        shift_file = False
        for line in file1:
            if 'shiftxy' in line or 'setxy' in line:
                shift_file = True
                coords = line.replace(')','').split('(')[1].replace('(','').replace(' ','').strip()
                x = int(coords.split(',')[0])
                y = int(coords.split(',')[1])
                cx = cx + x
                cy = cy + y
                if cx > hx: hx = cx
                if cy > hy: hy = cy
                if cx < lx: lx = cx
                if cy < ly: ly = cy
        if shift_file:
            self.set_ratio(hx - lx,hy - ly ,hx,lx,hy,ly)
            if onPC:
                tortue.setx(tortue.xcor() - screen.canvwidth / 4 )
                tortue.sety(tortue.ycor() + screen.canvheight / 2 )
                
        #self.log(0,"RATIO SET TO " + str(self.modifier))
        file1.close()
        file1 = open('./pict_catalog/' + str(filename) + '.log', 'r')
        count = 0
        prior_verbose_value = self.verbose_logging
        self.verbose_logging = True
        for line in file1:
            if self.stopping == False:
                count += 1
                self.run_command(line.strip(),ce)
        if onPC:
            tortue.setx(tortue.xcor() + screen.canvwidth / 4 )
            tortue.sety(tortue.ycor() - screen.canvheight / 2 )
        self.verbose_logging = prior_verbose_value
        self.stopping = False
    def log(self,type,string):
        if self.logging or type == 1:
            if self.onPC == False and self.bluetooth.connected:
                try:
                    tail = '\r\n'
                    if type == 2: tail = ''
                    uart.write(string + tail)
                except Exception as e:
                    pass
            if type != 2:
                print(string)
            else:
                print('? AWAITING COMMAND VIA UART')
    def calculate_angle(self,originx,originy,targetx,targety):
        p1 = (float(originx),float(originy))
        p2 = (float(targetx),float(targety))
        dx = targetx - originx
        dy = targety - originy
        theta = math.atan2(dy, dx)
        degrees = math.degrees(theta)
        return degrees
    def calculate_distance(self,originx,originy,targetx,targety):
        distance = ((originx - targetx)**2 + (originy - targety)**2)**0.5
        return distance
