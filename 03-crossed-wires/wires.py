from typing import NamedTuple, List

DIR = {
    "U": (0, 1),
    "D": (0, -1),
    "L": (-1, 0),
    "R": (1, 0)
}

class Coord(NamedTuple):
    x: int
    y: int

class Visited(NamedTuple):
    wire_num: int
    steps: int

class Wire(NamedTuple):
    wire_num: int
    coords: List[Coord]

ORIGIN = Coord(0, 0)

def gen_line_coords(start, direction, distance):
    for i in range(1, distance + 1):
        yield Coord(start.x + i * direction[0], start.y + i * direction[1])

def gen_wire(wire_num, instruction_pairs):
    coords = []
    pos = ORIGIN
    for direction, distance in instruction_pairs:
        for coord in gen_line_coords(pos, DIR[direction], distance):
            coords.append(coord)
            pos = coord
    return Wire(wire_num, coords)

def walk_wire(memory, wire):
    for idx, coord in enumerate(wire.coords):
        v = Visited(wire.wire_num, idx + 1)
        if coord in memory:
            if wire.wire_num not in {v.wire_num for v in memory[coord]}:
                memory[coord].append(v)
        else:
            memory[coord] = [v]

def parse_wire_input(path):
     with open(path, "r") as input_file:
         for line in input_file:
             yield list(map(lambda t: (t[0], int(t[1:])), line.split(",")))

def main():
    memory = dict()
    for idx, wire_instr in enumerate(parse_wire_input("input")):
        walk_wire(memory, gen_wire(idx, wire_instr))

    intersections = list(filter(lambda i: len(i[1]) > 1, memory.items()))

    # Part 1: Nearest intersection
    distances = list(map(lambda t: abs(t[0].x) + abs(t[0].y), intersections))
    distances.sort()
    print(f"Nearest intersection: {distances[0]}");

    # Part 2: Shortest circuit
    circuits = list(map(lambda t: sum(map(lambda v: v.steps, t[1])), intersections))
    circuits.sort()
    print(f"Shortest circuit: {circuits[0]}");

if __name__ == "__main__":
    main()
