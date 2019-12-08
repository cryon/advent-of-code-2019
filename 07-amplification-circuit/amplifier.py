from intcomp import Intcomp, ExitStatus, parse_input

class IoMem:
    def __init__(self, init):
        self.mem = init

    def input(self, amp):
        if self.mem[amp]:
            val = self.mem[amp].pop(0)
            return val
        return None

    def output(self, amp, o):
        self.mem[amp].append(o)

def run(settings):
    highest_signal = 0
    for setting in settings:
        mem = IoMem({
             "a": [setting[0], 0], # init
             "b": [setting[1]],
             "c": [setting[2]],
             "d": [setting[3]],
             "e": [setting[4]]
        })

        a = Intcomp(amplifier_program,
                    lambda: mem.input("a"),
                    lambda o: mem.output("b", o))

        b = Intcomp(amplifier_program,
                    lambda: mem.input("b"),
                    lambda o: mem.output("c", o))

        c = Intcomp(amplifier_program,
                    lambda: mem.input("c"),
                    lambda o: mem.output("d", o))

        d = Intcomp(amplifier_program,
                    lambda: mem.input("d"),
                    lambda o: mem.output("e", o))

        e = Intcomp(amplifier_program,
                    lambda: mem.input("e"),
                    lambda o: mem.output("a", o))

        while True:
            next(a.run())
            next(b.run())
            next(c.run())
            next(d.run())
            if next(e.run()) is ExitStatus.HALTED:
                break

        highest_signal = max(highest_signal, mem.input("a"))
    return highest_signal

def phase_settings1():
    for i in range(44445):
        l = list(map(int, list("{:05d}".format(i))))
        if all(map(lambda x: x < 5, l)) and len(set(l)) == len(l):
            yield l

def phase_settings2():
    for i in range(44445, 100000):
        l = list(map(int, list("{:05d}".format(i))))
        if all(map(lambda x: x >= 5 and x <= 9, l)) and len(set(l)) == len(l):
            yield l

if __name__ == "__main__":
    amplifier_program = parse_input("input")

    res1 = run(phase_settings1())
    print(f"Higest signal for part 1: {res1}.")

    res2 = run(phase_settings2())
    print(f"Higest signal for part 2: {res2}.")
