import re
from collections import namedtuple, defaultdict

TestCase = namedtuple('TestCase', 'case expected')


def check_case(test_case, actual):
    if test_case.expected == actual:
        print("OK %s" % (test_case.case,))
    else:
        print("FAIL %s, expected %s, got %s" % (test_case.case, test_case.expected, actual))


TEST_CASES = [
    TestCase("""
Begin in state A.
Perform a diagnostic checksum after 6 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state B.

In state B:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A.
""", 3),
]

Instruction = namedtuple('Instruction', 'state current write move next')
Cursor = namedtuple('Cursor', 'pos state')


def parse_program(input):
    program = {}
    lines = (l for l in input.strip().split('\n'))

    # initial state
    m = re.match(r'Begin in state (\w).', next(lines))
    cursor = Cursor(0, m.group(1))

    # iterations
    m = re.match(r'Perform a diagnostic checksum after (\d+) steps.', next(lines))
    iterations = int(m.group(1))

    parsing_state, parsing_value = None, None
    while True:
        line = next(lines, None)
        if line is None:
            break

        if line == '':
            continue

        m = re.match(r'In state (\w):', line)
        if m:
            parsing_state = m.group(1)
            continue

        m = re.match(r'  If the current value is (\d):', line)
        if m:
            parsing_value = int(m.group(1))
            continue

        m = re.match(r'    - Write the value (\d).', line)
        if m:
            write = int(m.group(1))
            continue

        m = re.match(r'    - Move one slot to the (\w+).', line)
        if m:
            move = +1 if m.group(1) == 'right' else -1
            continue

        m = re.match(r'    - Continue with state (\w).', line)
        if m:
            next_state = m.group(1)
            instruction = Instruction(parsing_state, parsing_value, write, move, next_state)
            program[(instruction.state, instruction.current)] = instruction
            continue

        assert False, 'bad line [%s]' % (line,)

    return program, cursor, iterations


def solve(input):
    tape = defaultdict(int)
    program, cursor, iterations = parse_program(input)

    print(cursor, iterations)

    while iterations:
        current = tape[cursor.pos]
        instruction = program[(cursor.state, current)]
        tape[cursor.pos] = instruction.write
        cursor = Cursor(cursor.pos + instruction.move, instruction.next)
        iterations -= 1
        if iterations % 100000 == 0:
            print(iterations)

    return list(tape.values()).count(1)


INPUT = """
Begin in state A.
Perform a diagnostic checksum after 12368930 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the right.
    - Continue with state C.

In state B:
  If the current value is 0:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the right.
    - Continue with state D.

In state C:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state D.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A.

In state D:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state E.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state D.

In state E:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state F.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state B.

In state F:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state E.
"""

if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        check_case(case, result)

    print(solve(INPUT))
