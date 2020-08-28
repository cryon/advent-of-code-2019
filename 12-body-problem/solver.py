from re import findall
from itertools import combinations
from functools import reduce
from collections import namedtuple

Moon = namedtuple("Moon",  "pos vel")

def parse_input(path):
    res = []
    with open(path, "r") as input_file:
        for line in input_file:
            p = list(map(int, findall("-?\d+", line)))
            res.append(Moon(p, [0, 0, 0]))
    return res

# From https://stackoverflow.com/questions/147515/least-common-multiple-for-3-or-more-numbers
def lcm(a, b):
    x, y = a, b
    while b:
        a, b = b, a % b
    return x * y // a

def simulate(system, pairs, dim):
    for m1, m2 in pairs:
        if m1.pos[dim] < m2.pos[dim]:
            m1.vel[dim] += 1
            m2.vel[dim] -= 1
        elif m1.pos[dim] > m2.pos[dim]:
            m1.vel[dim] -= 1
            m2.vel[dim] += 1
    for m in system:
        m.pos[dim] = m.pos[dim] + m.vel[dim]
    return tuple((m.pos[d], m.vel[d]) for m in system)

def total_energy(system):
    energy = 0
    for body in system:
        p, k = 0, 0
        for d in range(3):
            p += abs(body.pos[d])
            k += abs(body.vel[d])
        energy += p * k
    return energy

if __name__ == "__main__":
    system = parse_input("input")
    moon_pairs = list(combinations(system, 2))

    for i in range(1000):
        for d in range(3):
            simulate(system, moon_pairs, d)

    print(f"Part 1: Total energy after 1000 steps: {total_energy(system)}")

    system = parse_input("input")
    moon_pairs = list(combinations(system, 2))

    periods = [0] * 3
    for d in range(3):
        mem = set()
        while True:
            state = simulate(system, moon_pairs, d)
            if state in mem: break
            mem.add(state)
            periods[d] += 1

    print(f"Part 2: {reduce(lcm, periods)}")
