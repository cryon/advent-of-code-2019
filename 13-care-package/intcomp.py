from collections import namedtuple
from itertools import starmap
from sys import exit

Param = namedtuple("Param", "mode value")
Statement = namedtuple("Statement", "handler params")

class Intcomp:
    def __init__(self, init_mem):
        self.mem = {}
        self.instr_ptr = 0
        self.handlers = {}
        self.incr_instr_ptr = True
        self.relative_base = 0

        self.input_func = lambda: input("Input: ")
        self.output_func = lambda o: print(f"Output: {o}")

        for idx, instr in enumerate(init_mem):
            self.mem[idx] = instr

        self.add_handler(1, self.handle_add)
        self.add_handler(2, self.handle_mul)
        self.add_handler(3, self.handle_input)
        self.add_handler(4, self.handle_output)
        self.add_handler(5, self.handle_jump_if_true)
        self.add_handler(6, self.handle_jump_if_false)
        self.add_handler(7, self.handle_is_greater)
        self.add_handler(8, self.handle_is_equal)
        self.add_handler(9, self.handle_relative_base_offset)

    def handle_add(self, p1, p2, p3):
        self.store(p3, self.fetch(p1) + self.fetch(p2))

    def handle_mul(self, p1, p2, p3):
        self.store(p3, self.fetch(p1) * self.fetch(p2))

    def handle_input(self, p1):
        self.store(p1, int(self.input_func()))

    def handle_output(self, p1):
        self.output_func(self.fetch(p1))

    def handle_jump_if_true(self, p1, p2):
        if self.fetch(p1) != 0:
            self.jmp(p2)

    def handle_jump_if_false(self, p1, p2):
        if self.fetch(p1) == 0:
            self.jmp(p2)

    def handle_is_greater(self, p1, p2, p3):
        if self.fetch(p1) < self.fetch(p2):
            self.store(p3, 1)
        else:
            self.store(p3, 0)

    def handle_is_equal(self, p1, p2, p3):
        if self.fetch(p1) == self.fetch(p2):
            self.store(p3, 1)
        else:
            self.store(p3, 0)

    def handle_relative_base_offset(self, p1):
        self.relative_base += self.fetch(p1)

    def fetch(self, p):
        if p.mode == 0: return self.mem.get(p.value, 0)#self.mem[p.value]
        if p.mode == 1: return p.value
        if p.mode == 2: return self.mem.get(p.value + self.relative_base, 0)#self.mem[p.value + self.relative_base]
        exit(f"Unknown mode {p.mode}")

    def store(self, p, val):
        if p.mode == 0: self.mem[p.value] = val
        elif p.mode == 2: self.mem[p.value + self.relative_base] = val
        else: exit(f"Cannot store to param with mode {p.mode}")

    def jmp(self, p):
        self.instr_ptr = self.fetch(p)
        self.incr_instr_ptr = False

    def add_handler(self, op, func):
        arity = func.__code__.co_argcount - 1
        self.handlers[op] = (arity, func)

    def run(self):
        for statement in self.statements():
            statement.handler(*statement.params)

    def statements(self):
        while True:
            val = self.mem[self.instr_ptr]
            op = val % 100
            if (op == 99): return
            arity, handler = self.handlers[op]
            modes = [int(m) for m in reversed(str(val)[:-2])] + [0] * 5
            mem_range = range(self.instr_ptr + 1, self.instr_ptr + 1 + arity)
            raw_params = [self.mem.get(x, 0) for x in mem_range]
            params = starmap(Param, zip(modes, raw_params))
            yield Statement(handler, params)
            self.instr_ptr += (arity + 1) if self.incr_instr_ptr else 0
            self.incr_instr_ptr = True

def parse_input(path):
    res = []
    with open(path, "r") as input_file:
        for line in input_file:
            res += map(int, line.split(","))
    return res
