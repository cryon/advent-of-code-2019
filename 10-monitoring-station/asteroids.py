from itertools import product, cycle
from collections import namedtuple
from math import sqrt, atan2

Asteroid = namedtuple("Asteroid", "x y")
Vector = namedtuple("Vector", "x y")

def parse_input(path):
    with open(path, "r") as input_file:
        for y, line in enumerate(input_file):
            for x, char in enumerate(line):
                if char == '#': yield Asteroid(x, y)

def uvec(a1, a2):
    v = Vector(a2.x - a1.x, a2.y - a1.y)
    l = sqrt(v.x**2 + v.y**2)
    return Vector(round(v.x/l, 4), round(v.y/l, 4))

def rel_distance(a1, a2):
    return a2.x - a1.x + a2.y - a1.y

def rel_angle_from_y(v):
    return atan2(v.y+1, v.x)

if __name__ == "__main__":
    asteroids = list(parse_input("input"))

    # Vision from each asteroid
    vectors = {}
    for a1, a2 in product(asteroids, repeat=2):
        if a1 == a2: continue
        vectors.setdefault(a1, set()).add(uvec(a1, a2))

    location = max(vectors, key=lambda k: len(vectors[k]))
    print(f"Part 1: {location} has vision of {len(vectors[location])} asteroids.")

    # Sort asteroids on same ray from location
    angles = {}
    for a in asteroids:
        if a == location: continue
        ua = uvec(location, a)
        angles.setdefault(ua, []).append(a)
        angles[ua] = sorted(angles[ua], key=lambda k: rel_distance(location, k))

    # Pop asteriods clockwise from negative y axis
    cw_asteroids = sorted(angles.items(), key=lambda i: rel_angle_from_y(i[0]))
    boom = None
    for i, (k, v) in enumerate(cycle(cw_asteroids)):
        if len(k) == 0: continue
        boom = v.pop(0)
        if i == 199: break

    print(f"Part 2: The 200th asteroid to go is {boom}, solution: {boom.y*100 + boom.x}")
