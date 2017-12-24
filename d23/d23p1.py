from collections import namedtuple, defaultdict

TestCase = namedtuple('TestCase', 'case expected')


def check_case(test_case, actual):
    if test_case.expected == actual:
        print("OK %s" % (test_case.case,))
    else:
        print("FAIL %s, expected %s, got %s" % (test_case.case, test_case.expected, actual))


TEST_CASES = [
    TestCase('x', -1),
]


Instruction = namedtuple('Instruction', 'op X Y')
Instruction.__new__.__defaults__ = ('-', None, None)

def get_value(registers, v):
    try:
        val = int(v)
        return val
    except ValueError:
        return registers.get(v, 0)


def solve(input):
    program = [Instruction(*instruction.split()) for instruction in input.strip().split('\n')]
    pc = 0
    registers = defaultdict(int)
    mul_count = 0

    while 0 <= pc < len(program):
        current = program[pc]
        if current.op == 'set':
            registers[current.X] = get_value(registers, current.Y)
            pc += 1
        elif current.op == 'sub':
            registers[current.X] -= get_value(registers, current.Y)
            pc += 1
        elif current.op == 'mul':
            registers[current.X] *= get_value(registers, current.Y)
            mul_count += 1
            pc += 1
        elif current.op == 'jnz':
            if get_value(registers, current.X) != 0:
                pc += get_value(registers, current.Y)
            else:
                pc += 1
        else:
            assert False, 'Bad Operation'

    return mul_count

INPUT = """
set b 81
set c b
jnz a 2
jnz 1 5
mul b 100
sub b -100000
set c b
sub c -17000
set f 1
set d 2
set e 2
set g d
mul g e
sub g b
jnz g 2
set f 0
sub e -1
set g e
sub g b
jnz g -8
sub d -1
set g d
sub g b
jnz g -13
jnz f 2
sub h -1
set g b
sub g c
jnz g 2
jnz 1 3
sub b -17
jnz 1 -23
"""

if __name__ == '__main__':
    print(solve(INPUT))
