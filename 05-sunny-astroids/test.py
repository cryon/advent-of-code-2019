class Intcomp:
    def __init__(self, init_mem):
        self.mem = init_mem.copy()
        self.instr_ptr = 0
        self.handlers = {}
        self.incr_instr_ptr = True

        self.add_handler(1, self.handle_add)
        self.add_handler(2, self.handle_mul)
        self.add_handler(3, self.handle_input)
        self.add_handler(4, self.handle_output)
        self.add_handler(5, self.handle_jump_if_true)
        self.add_handler(6, self.handle_jump_if_false)
        self.add_handler(7, self.handle_is_greater)
        self.add_handler(8, self.handle_is_equal)

    def handle_add(self, p1, p2, p3):
        self.store(p3, self.fetch(p1) + self.fetch(p2))

    def handle_mul(self, p1, p2, p3):
        self.store(p3, self.fetch(p1) * self.fetch(p2))

    def handle_input(self, p1):
        self.store(p1, int(input("Input: ")))

    def handle_output(self, p1):
        print(f"Output: {self.fetch(p1)}")

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

    def run(self):
        for func, params in self.instructions():
            func(*params)

    def fetch(self, addr_param):
        mode, val = addr_param
        if mode == 1: return val
        if mode == 0: return self.mem[val]
        sys.exit(f"Unknown mode {mode}")

    def store(self, addr_param, val):
        _, addr = addr_param
        self.mem[addr] = val

    def jmp(self, addr_param):
        self.incr_instr_ptr = False
        self.instr_ptr = self.fetch(addr_param)

    def add_handler(self, op, func):
        arity = func.__code__.co_argcount - 1
        self.handlers[op] = (arity, func)

    def instructions(self):
        while True:
            t = self.mem[self.instr_ptr]
            op = t % 100
            if op == 99:
                break
            arity, handler = self.handlers[op]
            modes = [int(m) for m in list(reversed(str(t)[:-2]))] + [0] * 5
            parameters = list(zip(modes, self.mem[self.instr_ptr + 1:self.instr_ptr + arity + 1]))
            yield handler, parameters
            if self.incr_instr_ptr:
                self.instr_ptr += arity + 1
            self.incr_instr_ptr = True

def parse_input(path):
    res = []
    with open(path, "r") as input_file:
        for line in input_file:
            res += map(int, line.split(","))
    return res

if __name__ == "__main__":
    ic = Intcomp(parse_input("input"))
    ic.run()
