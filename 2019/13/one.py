
# Reads file into string
def file_to_string(file_name):
    with open(file_name) as file_pointer:
        while True:
            line = file_pointer.read()
            if not line:    
                break
            string_opcode = line
    return string_opcode


# finds commas in string
# could be done with .split(), but oh well
def comma_finder(string_opcode):
    start_search = 0
    all_commas = []
    while True:
        comma_loc = string_opcode.find(',', start_search)
        if comma_loc == -1:                   # breaks out of loop once all commas found
            break
        all_commas.append(comma_loc)
        start_search = comma_loc + 1
    return all_commas


# parses string into an array
# could be done with .split()
def string_to_array(opcode_string, comma_index):
    opcode = []
    temp = 0
    for i in range(len(comma_index)+1):
        start = temp
        if i == len(comma_index):
            end = len(opcode_string)+1
            opcode.append(int(opcode_string[start:end]))
            break
        if i < len(comma_index):
            end = comma_index[i]
        opcode.append(int(opcode_string[start:end]))
        temp = comma_index[i]+1
    return opcode


# adds memory to the end of the program
# MIGHT NEED MORE MEMORY
def add_memory(program):
    # for _ in range(math.floor(len(program)/2)):
    for _ in range(5000):
        program.append(0)
    return program


# makes number str and back-fills with 0s
def make_useable(number):
    string_of_number = str(number)
    string_of_number = ('0' * int(5-len(string_of_number))) + string_of_number
    return string_of_number


# returns true if number was a valid opcode, false if not
def opcode_checker(number):
    answer = False                             # default falseyness
    string_of_number = str(number)                         # string of number
    if len(string_of_number) > 5:                          # greater than 5 digits c/t be an opcode
        return answer
    if number < 1:                             # 0 or -#s c/t be opcodes
        return answer

    string_of_number = ('0' * int(5-len(string_of_number))) + string_of_number 

    opcode     = int(string_of_number[3: 5])                # purely symbolic
    mode_three = int(string_of_number[0])
    mode_two   = int(string_of_number[1])
    mode_one   = int(string_of_number[2])

    # https://stackoverflow.com/questions/148042/using-or-comparisons-with-if-statements
    if opcode in (1, 2, 3, 4, 5, 6, 7, 8, 9):
        if mode_three in (0, 1, 2) and mode_two in (0, 1, 2) and mode_one in (0, 1, 2):
            answer = True

    if opcode == 99:
        answer = True

    return answer


# given a pointer and a program, executes instructions and returns modified program + pointer
def opcode_processor(pointer, program, relative_base, outputs):
    opcode = program[pointer]         # purely symbolic
    if opcode_checker(opcode):        # this is only helpful for debugging
        string_opcode = make_useable(opcode)
        first  = int(string_opcode[2])
        second = int(string_opcode[1])
        third  = int(string_opcode[0])

        if int(string_opcode[4]) == 1:
            # used this page to figure out an error message:
            # https://www.pythonforbeginners.com/concatenation/string-concatenation-and-formatting-in-python
            # used this to figure out another error:
            # https://www.reddit.com/r/adventofcode/comments/e8aw9j/2019_day_9_part_1_how_to_fix_203_error/
            x = program[pointer + 1]    # default set to value not address (mode 1)
            y = program[pointer + 2]
            if first == 0:                   # x and y updated if modes not 1
                x = program[x]
            elif first == 2:
                x = program[x + relative_base]
            if second == 0:
                y = program[y]
            elif second == 2:
                y = program[y + relative_base]
            address = program[pointer + 3]
            if third == 2:
                address = program[pointer + 3] + relative_base
            program[address] = x + y      # + rule
            pointer += 4

        elif int(string_opcode[4]) == 2:
            x = program[pointer + 1]   # default x and y set to raw (mode 1)
            y = program[pointer + 2]
            if first == 0:
                x = program[x]
            elif first == 2:
                x = program[x + relative_base]
            if second == 0:
                y = program[y]
            elif second == 2:
                y = program[y + relative_base]
            address = program[pointer + 3]
            if third == 2:
                address = program[pointer + 3] + relative_base
            program[address] = x * y  # * rule
            pointer += 4

        elif int(string_opcode[4]) == 3:  # get input rule
	    # this should not be activated for day 13 part 1
            x = input('~INPUT: ')
            if first == 0:
                program[program[pointer + 1]] = x
            elif first == 2:
                program[program[pointer + 1] + relative_base] = x
            pointer += 2

        elif int(string_opcode[4]) == 4:  # print rule
            if first == 0:
                outputs.append(program[program[pointer + 1]])
            if first == 1:
                outputs.append(program[pointer + 1])
            elif first == 2:
                outputs.append(program[program[pointer + 1] + relative_base])
            pointer += 2

        elif int(string_opcode[4]) == 5:   # jump-if-true
            x = program[pointer + 1]
            y = program[pointer + 2]
            if first == 0:
                x = program[x]
            elif first == 2:
                x = program[x + relative_base]
            if second == 0:
                y = program[y]
            elif second == 2:
                y = program[y + relative_base]
            if x != 0:
                pointer = y
            else:
                pointer += 3

        elif int(string_opcode[4]) == 6:   # jump-if-false
            x = program[pointer + 1]  # default mode 1
            y = program[pointer + 2]
            if first == 0:
                x = program[x]
            elif first == 2:
                x = program[x + relative_base]
            if second == 0:
                y = program[y]
            elif second == 2:
                y = program[y + relative_base]
            if x == 0:
                pointer = y
            else:
                pointer += 3

        elif int(string_opcode[4]) == 7:   # less-than rule
            x = program[pointer + 1]
            y = program[pointer + 2]
            if first == 0:
                x = program[x]
            elif first == 2:
                x = program[x + relative_base]
            if second == 0:
                y = program[y]
            elif second == 2:
                y = program[y + relative_base]
            address = program[pointer + 3]
            if third == 2:
                address = program[pointer + 3] + relative_base
            if x < y:
                program[address] = 1
            else:
                program[address] = 0
            pointer += 4

        elif int(string_opcode[4]) == 8:   # equal-to rule
            x = program[pointer + 1]
            y = program[pointer + 2]
            if first == 0:
                x = program[x]
            elif first == 2:
                x = program[x + relative_base]
            if second == 0:
                y = program[y]
            elif second == 2:
                y = program[y + relative_base]
            address = program[pointer + 3]
            if third == 2:
                address = program[pointer + 3] + relative_base
            if x == y:
                program[address] = 1
            else:
                program[address] = 0
            pointer += 4

        elif int(string_opcode[3:5]) == 9:   # relative base modifier rule
            # leading 0s not allowed https://stackoverflow.com/questions/36386346/syntaxerror-invalid-token
            value = program[pointer + 1]
            if first == 0:
                value = program[value]
            elif first == 2:
                value = program[value + relative_base]
            relative_base += value
            pointer += 2

        elif int(string_opcode[3:5]) == 99:
            return 'END', program, relative_base, outputs
    else:
        print("--- ERORR ---")
        print("@ adress: ", pointer, "which is int: ", opcode)
        return 'DONE', 'ERROR', 0, 0

    return pointer, program, relative_base, outputs


# runs program until program returns END, then returns outputs
def run_program(ram):
    outputs = []
    pointer = 0
    relative_base = 0
    while True:
        pointer, ram, relative_base, outputs = opcode_processor(pointer, ram, relative_base, outputs)
        if pointer == 'END':                  
            return outputs


# tidies up output into tuples
def output_processor(dirty_output):
    clean_output = []
    iii = 0
    for _ in range(len(dirty_output)//3):   # _ is idiomatic
        clean_output.append((dirty_output[iii], dirty_output[iii+1], dirty_output[iii+2]))
        iii += 3
    return clean_output


# processes output into a complete askii_map and also counts blocks to answer one
def map_maker(output):
    x_min = 10000000
    y_min = 10000000
    x_max = 0
    y_max = 0

    for elem in output:   # finds bounds of the screen
        x = elem[0]       # symbolic
        y = elem[1]
        if x > x_max:
            x_max = x
        if y > y_max:
            y_max = y
        if x < x_min:
            x_min = x
        if y < y_min:
            y_min = y
    length = x_max - x_min
    height = y_max - y_min

    askii_map = []               # makes an empty map the size of the screen
    for i in range(height + 1):  # not sure why these two +1s are needed?
        line = []
        for ii in range(length + 1):
            line.append(0)
        askii_map.append(line)

    block_count = 0
    for elem in output:          # fills map with tile_ids
        x = elem[0]              # symbolic
        y = elem[1]
        tile_id = elem[2]
        if tile_id == 0:
            tile = ' '
        elif tile_id == 1:
            tile = '&'
        elif tile_id == 2:
            tile = '#'
            block_count += 1
        elif tile_id == 3:
            tile = '-'
        elif tile_id == 4:
            tile = '@'
        askii_map[y][x] = tile

    return askii_map, length, height, block_count


# main program:
program = file_to_string('input.txt')  # change file name here!
all_commas = comma_finder(program)
program = string_to_array(program, all_commas)
program = add_memory(program)
# done with file io / formatting

output = run_program(program)
output = output_processor(output)
askii_map, l, h, block_count = map_maker(output)

print('\nNumber of blocks: ', block_count, '\n')   # answer

