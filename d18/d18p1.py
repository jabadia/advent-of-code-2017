from collections import namedtuple, defaultdict

TestCase = namedtuple('TestCase', 'case expected')


def check_case(test_case, actual):
    if test_case.expected == actual:
        print("OK %s" % (test_case.case,))
    else:
        print("FAIL %s, expected %s, got %s" % (test_case.case, test_case.expected, actual))


TEST_CASES = [
    TestCase("""
set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2    
    """, 4),
]


def get_value(registers, v):
    try:
        val = int(v)
        return val
    except ValueError:
        return registers.get(v, 0)


Instruction = namedtuple('Instruction', 'op X Y')
Instruction.__new__.__defaults__ = ('-', None, None)


def solve(input):
    program = [Instruction(*instruction.split()) for instruction in input.strip().split('\n')]
    pc = 0
    registers = defaultdict(int)
    last_sound = -1

    while 0 <= pc < len(program):
        current = program[pc]
        if current.op == 'snd':
            last_sound = get_value(registers, current.X)
            pc += 1
        elif current.op == 'set':
            registers[current.X] = get_value(registers, current.Y)
            pc += 1
        elif current.op == 'add':
            registers[current.X] += get_value(registers, current.Y)
            pc += 1
        elif current.op == 'mul':
            registers[current.X] *= get_value(registers, current.Y)
            pc += 1
        elif current.op == 'mod':
            registers[current.X] = registers[current.X] % get_value(registers, current.Y)
            pc += 1
        elif current.op == 'rcv':
            if get_value(registers, current.X) != 0:
                print('recovered', last_sound)
                break
            pc += 1
        elif current.op == 'jgz':
            if get_value(registers, current.X) > 0:
                pc += get_value(registers, current.Y)
            else:
                pc += 1
        else:
            assert False, 'Bad Operation'

    return last_sound

INPUT = """
set i 31
set a 1
mul p 17
jgz p p
mul a 2
add i -1
jgz i -2
add a -1
set i 127
set p 680
mul p 8505
mod p a
mul p 129749
add p 12345
mod p a
set b p
mod b 10000
snd b
add i -1
jgz i -9
jgz a 3
rcv b
jgz b -1
set f 0
set i 126
rcv a
rcv b
set p a
mul p -1
add p b
jgz p 4
snd a
set a b
jgz 1 3
snd b
set f 1
add i -1
jgz i -11
snd a
jgz f -16
jgz a -19
"""

if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        check_case(case, result)
    print(solve(INPUT))
