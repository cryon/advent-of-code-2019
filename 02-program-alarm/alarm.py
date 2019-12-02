class Intcomp:
    def __init__(self, init_mem):
        self.mem = init_mem.copy()
        self.instr_ptr = 0
        self.handlers = {}

        self.add_instr(1, lambda a1, a2, t: self.store(t, self.fetch(a1) + self.fetch(a2))) # add
        self.add_instr(2, lambda a1, a2, t: self.store(t, self.fetch(a1) * self.fetch(a2))) # mul

    def run(self):
        for func, args in self.instructions():
            func(*args)

    def fetch(self, addr):
        return self.mem[addr]

    def store(self, addr, val):
        self.mem[addr] = val

    def add_instr(self, op, func):
        arity = func.__code__.co_argcount
        self.handlers[op] = (arity, func)

    def instructions(self):
        while True:
            op = self.fetch(self.instr_ptr)
            if op == 99:
                break
            arity, handler = self.handlers[op]
            yield handler, list(self.mem[self.instr_ptr + 1:self.instr_ptr + arity + 1])
            self.instr_ptr += arity + 1

def parse_input(path):
    res = []
    with open(path, "r") as input_file:
        for line in input_file:
            res += map(int, line.split(","))
    return res

if __name__ == "__main__":
    input = parse_input("patched_input")

    # Part 1
    ic = Intcomp(input)
    ic.run()
    print(f"Part 1: {ic.fetch(0)}")

    # Part 2, aka. brute the force
    wanted = 19690720
    for noun, verb in [(a, b) for a in range(100) for b in range(100)]:
        ic2 = Intcomp(input)
        ic2.store(1, noun)
        ic2.store(2, verb)
        ic2.run()
        res = ic2.fetch(0)
        if res == wanted:
            print(f"Part 2: noun=[{noun}] verb=[{verb}] noun + verb = [{100 * noun + verb}]")
            break
