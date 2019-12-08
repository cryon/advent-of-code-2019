from itertools import count

class Node:
    parent = None
    children = []
    def __init__(self, name):
        self.name = name

    def iter_parent(self, cache):
        current = self
        while current.parent != None:
            parent = cache[current.parent]
            yield parent
            current = parent

def build_orbit_cache(orbits):
    cache = {}
    for p, c in orbits:
        if c not in cache: cache[c] = Node(c)
        if p not in cache: cache[p] = Node(p)
        cache[p].children.append(c)
        cache[c].parent = p
    return cache

def parse_input(path):
     with open(path, "r") as input_file:
         for line in input_file:
             split = line.split(")")
             yield split[0].strip(), split[1].strip()

if __name__ == "__main__":
    cache = build_orbit_cache(parse_input("input"))

    # Part 1
    orbits = 0
    for k, v in cache.items():
        orbits += sum(1 for x in v.iter_parent(cache))
    print(f"Number of direct and indirect orbits: {orbits}.")

    # Part 2
    you_orbit = cache[cache["YOU"].parent]
    san_orbit = cache[cache["SAN"].parent]

    trail = {}
    for i, n in enumerate(you_orbit.iter_parent(cache)):
        trail[n] = i + 1

    for i, n in enumerate(san_orbit.iter_parent(cache)):
        if n in trail:
            print(f"Number of orbital transfers: {i + trail[n] + 1}.")
            break
