# day 13: playing intcode breakout game
import time
start_time = time.time()

# Reads file into string, code adapted from ( https://github.com/imhoffman/advent/blob/master/2015/01/one.py )
def file_to_string(file_name):
    with open(file_name) as fp:
        while True:
            line = fp.read()
            if not line:         # a little bit of error catching
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
    buffer = 0
    for i in range(len(comma_index)+1):
        start = buffer
        if i == len(comma_index):
            end = len(opcode_string)+1
            opcode.append(int(opcode_string[start:end]))
            break
        if i < len(comma_index):
            end = comma_index[i]
        opcode.append(int(opcode_string[start:end]))
        buffer = comma_index[i]+1
    return opcode


# adds memory to the end of the program
# MIGHT NEED MORE MEMORY
def add_memory(program):
    # for _ in range(math.floor(len(program)/2)):
    for _ in range(7000):
        program.append(0)
    return program


# makes number str and back-fills with 0s
def yarnifier(number):
    yarn = str(number)
    yarn = ("0" * int(5-len(yarn))) + yarn
    return yarn


# returns true if number was a valid opcode, false if not
def opcode_checker(number):
    answer = False                             # default falseyness
    yarn = str(number)                         # string of number
    if len(yarn) > 5:                          # greater than 5 digits c/t be an opcode
        return answer
    if number < 1:                             # 0 or -#s c/t be opcodes
        return answer

    yarn = ("0" * int(5-len(yarn))) + yarn     # backfill yarn with 0s, just like yarnifier

    opcode     = int(yarn[3:5])                # purely symbolic
    mode_three = int(yarn[0])
    mode_two   = int(yarn[1])
    mode_one   = int(yarn[2])

    # https://stackoverflow.com/questions/148042/using-or-comparisons-with-if-statements
    if opcode in (1, 2, 3, 4, 5, 6, 7, 8, 9):
        if mode_three in (0, 1, 2) and mode_two in (0, 1, 2) and mode_one in (0, 1, 2):
            answer = True

    if opcode == 99:
        answer = True

    return answer


# given a pointer and a program, executes instructions and returns modified program + pointer
def opcode_processor(pointer, program, relative_base, outputs, ball, paddle):
    opcode = program[pointer]         # purely symbolic
    if opcode_checker(opcode):        # this is only helpful for debugging
        yarn = yarnifier(opcode)
        first = int(yarn[2])
        second = int(yarn[1])
        third = int(yarn[0])

        if int(yarn[4]) == 1:
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

        elif int(yarn[4]) == 2:
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

        elif int(yarn[4]) == 3:  # get input rule
            x = generate_inputs(ball, paddle)
            if first == 0:
                program[program[pointer + 1]] = x
            elif first == 2:
                program[program[pointer + 1] + relative_base] = x
            # stick = 'NULL'
            pointer += 2

        elif int(yarn[4]) == 4:  # print rule
            if first == 0:
                outputs.append(program[program[pointer + 1]])
            if first == 1:
                outputs.append(program[pointer + 1])
            elif first == 2:
                outputs.append(program[program[pointer + 1] + relative_base])
            pointer += 2

        elif int(yarn[4]) == 5:   # jump-if-true
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

        elif int(yarn[4]) == 6:   # jump-if-false
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

        elif int(yarn[4]) == 7:   # less-than rule
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

        elif int(yarn[4]) == 8:   # equal-to rule
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

        elif int(yarn[3:5]) == 9:   # relative base modifier rule
            # leading 0s not allowed https://stackoverflow.com/questions/36386346/syntaxerror-invalid-token
            value = program[pointer + 1]
            if first == 0:
                value = program[value]
            elif first == 2:
                value = program[value + relative_base]
            relative_base += value
            pointer += 2

        elif int(yarn[3:5]) == 99:
            return 'END', program, relative_base, outputs
    else:
        print("--- ERORR ---")
        print("@ adress: ", pointer, "which is int: ", opcode)
        return 'DONE', 'ERROR', 0, 0

    return pointer, program, relative_base, outputs


# runs program until END, then prints final score and returns
def run_program(ram):
    pointer = 0
    rel_base = 0
    block_count = 0
    outputs = []
    ball = 'null'
    paddle = 'null'
    while True:
        pointer, ram, rel_base, outputs = opcode_processor(pointer, ram, rel_base, outputs, ball, paddle)
        ball, paddle, score, new_block_count = render_screen(outputs, ball, paddle)   # should work now
        if pointer == 'END':
            print('FINAL SCORE: ', score)
            return
        elif new_block_count < block_count:
            render_block_count(new_block_count, score)
            block_count = new_block_count


# generates inputs such that paddle is always under ball
def generate_inputs(ball, paddle):
    if ball == paddle:
        move = 0
    else:
        if ball > paddle:
            move = 1
        elif ball < paddle:
            move = -1
    return move


# prints the number of blocks destroyed and score
def render_block_count(blocks, score):
    print('%d blocks left,' %blocks, ' score: ', score)
    print('--- %s minuets ---' %((time.time() - start_time)//60))
    return


# actually printing the screen takes too long, so this just prints when block are destroyed
def render_screen(output, ball, paddle):
    output = output_processor(output)
    ball, paddle, score, block_count = object_tracker(output, ball, paddle)
    return ball, paddle, score, block_count


# tides up output to make processing easier
def output_processor(dirty_output):
    clean_output = []
    iii = 0
    for _ in range(len(dirty_output)//3):
        clean_output.append((dirty_output[iii], dirty_output[iii+1], dirty_output[iii+2]))
        iii += 3
    return clean_output


# finds ball, paddle, and counts blocks
def object_tracker(output, ball, paddle):
    score = 0
    block_count = 0

    for elem in output:
        x = elem[0]               # symbolic
        tile_id = elem[2]        
        if x == -1:         # find score, print and remove
            score = tile_id
        if tile_id == 1:
            block_count += 1
        if tile_id == 3:
            paddle = x
        if tile_id == 4:
            ball = x

    return ball, paddle, score, block_count


# main program:
program = file_to_string('hacked_input.txt')  # change file name here!
all_commas = comma_finder(program)
program = string_to_array(program, all_commas)
program = add_memory(program)
# done with file io / formatting

# these steps need to be changed for inputs
output = run_program(program)

# just out of interest
print("--- %s hours ---" % ((time.time() - start_time)//60//60))  # print hours at the end

