import re
from logo_ce import command_engine
ce = command_engine()

class command_interpreter:
    def __init__(self):
        #[COMMAND,FULLNAME,WANTSVALUE,DESCRIPTION,EXAMPLE,VALUETYPE,[MIN,MAX]]
        self.command_list = [['pu','penup',False,'Raises the pen','pu',None,[None,None]]]
        self.command_list.append(['pd','pendown',False,'Lowers the pen','pd',None,[None,None]])
        self.command_list.append(['fd','forward',True,'Moves the turtle forward','fd 50',float,[-9999999.00,9999999.00]])
        self.command_list.append(['bk','backward',True,'Moves the turtle backward','bk 50',float,[-9999999.00,9999999.00]])
        self.command_list.append(['lt','left',True,'Rotates the turtle to the left','lt 90',float,[-9999999.00,9999999.00]])
        self.command_list.append(['rt','right',True,'Rotates the turtle to the right','rt 90',float,[-9999999.00,9999999.00]])
        self.command_list.append(['setxy','setxy',True,'Sets the X and Y coordinates','setxy (0,15)',tuple,[None,None]])
        self.command_list.append(['shiftxy','shiftxy',True,'Shifts the turtle by the specified number of steps on the X and Y coordinates','shiftxy (-15,20)',tuple,[None,None]])
        self.command_list.append(['seth','setheading',True,'Sets the heading of the turtle in degrees',float,[0,360]])
        self.command_list.append(['towards','towards',True,'Rotates the turtle towards the specified X and Y coordinates','towards (0,15)',tuple,[None,None]])
        self.command_list.append(['draw','draw',False,'Begins drawing','draw',None,[None,None]])
        self.command_list.append(['home','home',False,'Moves the turtle to the home coordinates of (0,0)','home',None,[None,None]])
        self.command_list.append(['xcor','xcoordinate',False,'Returns the current X coordinate of the turtle','xcor',None,[None,None]])
        self.command_list.append(['ycor','ycoordinate',False,'Returns the current Y coordinate of the turtle','ycor',None,[None,None]])
        self.command_list.append(['readpict','readpicture',True,'Reads the specified picture file and begins drawing','readpict triangle',str,[3,32]])
        self.command_list.append(['repeat','repeat',True,'Repeats commands the specified number of times','repeat 4 [rt 90 fd 100]',int,[1,100000]])
        self.command_list.append(['stop','stop',False,'Stops the turtle from excuting further commands','stop',None,[None,None]])
        self.command_list.append(['to','to',True,'Begins program creation mode with the filename specified','to triangle',str,[3,32]])
        self.command_list.append(['end','end',False,'Ends program creation mode and writes the commands entered to the file','end',None,[None,None]])
        self.command_list.append(['showvalue','showvalue',True,'Returns the evaluation of the specified value by the Micropython interpreter used to execute Logo','showvalue 14/5, showvalue logo.dprot',str,[1,100000]])
        self.command_list.append(['clear','clear',False,'Clears the screen when running Logo on your PC','clear',None,[None,None]])
        self.command_list.append(['help','help',False,'Returns this help','help',None,[None,None]])
        self.command_list.append(['scale','scale',True,'Sets a value that will be used to factor step values','scale 15',float,[1,100000]])
        self.command_list.append(['setr','setrotationratio',True,'Sets a value (cm) that indicates how far the turtle physically moves per degree instructed','setr 19.7',float,[0.01,1000]])
        self.command_list.append(['setpw','setpagewidth',True,'Sets a value (cm) that indicates page width',float,[1,1000]])
        self.command_list.append(['setph','setpageheight',True,'Sets a value (cm) that indicates page height',float,[1,1000]])
        self.command_list.append(['setdpr','setdistanceperrevolution',True,'Sets a value (cm) that indicates how far the turtle physically moves per one wheel revolution',float,[1,100000]])
        self.command_list.append(['setppr','setpulsesperrevolution',True,'Sets a value that indicates how many pulses it takes the motors to achieve one wheel revolution',float,[1,100000]])
        self.command_list.append(['setpu','setpenup',True,'Sets a value that indicates the servo motor duty cycle to be used for the penup position',int,[0,65000]])
        self.command_list.append(['setpd','setpendown',True,'Sets a value that indicates the servo motor duty cycle to be used for the penup position',int,[0,65000]])
        self.command_list.append(['setpds','setpendropspeed',True,'Sets a value that indicates the amount of time to allow for the pen to be dropped before again moving the turtle',float,[0,60]])
        self.command_list.append(['setspeed','setspeed',True,'Sets a value (1-10) that indicates at what speed to move the turtle',int,[1,10]])
    def process_command_string(self,command='repeat 4 [fd 50 pd rt 90 FD 12 repeat 2 [fd 50 rt 90] pu setXY ( 34 ,  34   )] pd fD    500 rt 90.0 pu'):
        command = command.lower().strip()
        monitored_characters = ['+',']','[',')','(','/','-',',','*']
        command = ' '.join(command.split())
        for i in range (10):
            for character in monitored_characters:
                if character != '[' and character != '(': command = command.replace(' '*i + character,character)
                if character != ']' and character != ')': command = command.replace(character + ' '*i,character)
        commands_to_execute = []
        commands_with_issues = []
        word_index = -1
        char_index = -1
        value_index = -1
        buffered_command = ''
        command_list_index = -1
        jump_to_index = -1
        for word in command.split(' '):
            word_index +=1
            char_index += len(word)
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
                    pass
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
                        failure_type = buffered_command + ' WILL NOT ACCEPT THE TYPE OF VALUE "' + word + '" REPRESENTS'
                    
                elif self.command_list[command_list_index][5] == float:
                    passed_validation = True
                    try:
                        if float(word) == word:
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
                        failure_type = buffered_command + ' WILL NOT ACCEPT THE TYPE OF VALUE "' + word + '" REPRESENTS'
                elif self.command_list[command_list_index][5] == tuple:
                    passed_validation = True
                    try:
                        if tuple(word) == word:
                            passed_validation = True
                            word = tuple(word)
                    except Exception as e:
                        passed_validation = False
                        failure_type = buffered_command + ' WILL NOT ACCEPT THE TYPE OF VALUE "' + word + '" REPRESENTS'
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
                        failure_type = buffered_command + ' WILL NOT ACCEPT THE TYPE OF VALUE "' + word + '" REPRESENTS'
                if passed_validation:  
                    if buffered_command == 'repeat':
                        repeat_block = ''
                        closing_right_bracket_index =  command.find(']',char_index,len(command))
                        try:
                            prefix_length = len(word) + 3
                            for i in range(char_index,len(command)):
                                if command[i] == "]":
                                    if 'repeat' in command[char_index:i]:
                                        pattern = '([a-z_]*)\s*[0-9*]\s*\[*\]'
                                        thestring = command[char_index:len(command)]
                                        repeats = re.subn(pattern, '', thestring)[1]
                                        current_bracket_search_index = char_index
                                        for j in range(repeats):
                                            current_bracket_search_index = command.find(']',current_bracket_search_index,len(command))+1
                                        closing_right_bracket_index = command.find(']',current_bracket_search_index+1,len(command))
                            repeat_block = command[char_index + prefix_length:closing_right_bracket_index]
                            repeat_block_word_count = len(repeat_block.split(' '))
                            #commands_to_execute.append([buffered_command,word,repeat_block])
                            repeat_results = self.process_repeat_strings([buffered_command,word,repeat_block])
                            if len(repeat_results[1]) > 0: commands_with_issues.append(repeat_results[1])
                            for result in repeat_results[0]:
                                commands_to_execute.append(result)
                            jump_to_index = word_index + repeat_block_word_count + 1
                        except Exception as e:
                            passed_validation = False
                            failure_type = buffered_command + ' WILL NOT ACCEPT A VALUE WITHOUT BRACKETS'
                            commands_with_issues.append([buffered_command,word,failure_type])
                            print(e)
                    else:
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
            pattern = '([a-z_]*)\s*[0-9*]\s*\[*\]'
            thestring = command[2]
            repeats = re.subn(pattern, '', thestring)[1]
            if repeats == 0:
                results = self.process_command_string(command[2])
                for i in range(command[1]):
                    for result in results[0]:
                        commands_to_execute.append[result]
                if len(results[1]) > 0: commands_with_issues.append[results[1]] 
            else:
                for o in range(int(command[1])):
                    current_bracket_search_index = 0
                    current_start_index = command[2].find('[')
                    main_block_start_index = 0
                    remove_portions = []
                    for j in range(repeats):
                        current_bracket_search_index = command[2].find(']',current_bracket_search_index,len(command[2]))
                        repeat_block = command[2][current_start_index+1:current_bracket_search_index]
                        analysis_block = command[2][0:current_start_index-1].split(' ')
                        iteration_block = analysis_block[len(analysis_block)-1]
                        repeat_block_iterations = 0
                        try:
                            repeat_block_iterations = int(iteration_block)
                            results = self.process_command_string(repeat_block)
                            prefix_length = len(str(repeat_block_iterations)) + len('repeat') + 3
                            start_index = current_bracket_search_index -  len(repeat_block) - prefix_length
                            main_repeat_block_pre = command[2][main_block_start_index:start_index].strip()
                            end_index = len(main_repeat_block_pre) + len(repeat_block) + prefix_length + 1
                            remove_portions.append([start_index,end_index])
                            main_pre_results = self.process_command_string(main_repeat_block_pre)
                            for result in main_pre_results[0]:
                                commands_to_execute.append(result)
                            if len(main_pre_results[1]) > 0: commands_with_issues.append[results[1]] 
                            main_block_start_index = end_index + 1
                            for i in range(repeat_block_iterations):
                                for result in results[0]:
                                    commands_to_execute.append(result)
                            if len(results[1]) > 0: commands_with_issues.append[results[1]] 
                            main_repeat_block_post = command[2][main_block_start_index:len(command[2])].strip()
                            main_repeat_block_post = main_repeat_block_post.split('[')[0].split('repeat')[0]
                            main_post_results = self.process_command_string(main_repeat_block_post)
                            for result in main_post_results[0]:
                                commands_to_execute.append(result)
                            if len(main_post_results[1]) > 0: commands_with_issues.append[results[1]]
                        except Exception as e:
                            commands_with_issues.append([command[0],None,str(command[0]) + ' DID NOT LIKE THE VALUE ' + str(repeat_block.split(' ')[len(repeat_block.split(' '))-2])])
        return [commands_to_execute,commands_with_issues]
    def run_command(self,command):
        ir = self.process_command_string(command)
        ir_issues = ir[1]
        ir_commands = ir[0]
        self.process_output(ir_issues,ir_commands)
    def process_output(self,commands_with_issues,commands_to_execute):
        ret = []
        if len(commands_with_issues) > 0:
            for entry in commands_with_issues:
                print(str(entry[2]))
        else:
            for entry in commands_to_execute:
                if entry[1] != None:
                    self.display_output(entry[0] + ' ' + entry[1])
                else:
                    self.display_output(entry[0])
                ce.execute_command(ce,entry[0],entry[1],self)
    def display_output(self,string):
        print(str(string))
