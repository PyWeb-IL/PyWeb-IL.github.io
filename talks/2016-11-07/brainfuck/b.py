"""
A Brainfuck[1] virtual machine

[1] https://en.wikipedia.org/wiki/Brainfuck
"""

import sys

_, program = sys.argv

BUFFER_SIZE = 30000
buffer = [0] * BUFFER_SIZE
current = 0
instruction_pointer = 0

def build_matching_parens(code):
    result = {}
    stack = []
    for i, c in enumerate(code):
        if c == '[':
            stack.append(i)
        elif c == ']':
            match = stack.pop()
            result[i] = match
            result[match] = i
    assert not stack
    return result
assert build_matching_parens('') == {}
assert build_matching_parens('[]') == {0: 1, 1: 0}
assert build_matching_parens('[[][]][]') == {
    0: 5, 5: 0,
    1: 2, 2: 1,
    3: 4, 4: 3,
    6: 7, 7: 6}

matching_paren = build_matching_parens(program)

def read(): return buffer[current]
def write(x): buffer[current] = x % 256
def set_current(x):
    global current
    current = x % BUFFER_SIZE

while instruction_pointer < len(program):
    instruction = program[instruction_pointer]
    if instruction == '-':
        write(read() - 1)
    elif instruction == '+':
        write(read() + 1)
    elif instruction == '<':
        set_current(current - 1)
    elif instruction == '>':
        set_current(current + 1)
    elif instruction == ',':
        c = sys.stdin.read(1)
        if not c:
            break
        write(ord(c))
    elif instruction == '.':
        sys.stdout.write(chr(read()))
    elif instruction == '[':
        if read() == 0:
            instruction_pointer = matching_paren[instruction_pointer]
    elif instruction == ']':
        instruction_pointer = matching_paren[instruction_pointer]
        continue
    else:
        pass # comment
    instruction_pointer += 1
