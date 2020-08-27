from intcomp import Intcomp, parse_input
from operator import itemgetter

class Robot:
    def __init__(self, brain, hull):
        self.brain = brain
        self.hull = hull

        self.direction = 0, 1
        self.pos = 0, 0
        self.mem = None

        self.brain.input_func = lambda: hull.get(self.pos, 0)
        self.brain.output_func = self.react

    def go(self):
        self.brain.run()

    def react(self, stimuli):
        if self.mem == None:
            self.mem = stimuli
            return

        self.hull[self.pos] = self.mem
        self.mem = None

        # rotate
        dx, dy = self.direction
        self.direction = (dy, -dx) if stimuli else (-dy, dx)

        # move forward
        x, y = self.pos
        self.pos = (x + self.direction[0]), (y + self.direction[1])

def render(hull):
    max_x = max(hull, key=itemgetter(0))[0]
    min_y = min(hull, key=itemgetter(1))[1]
    for y in range(0, min_y - 1, -1):
        for x in range(max_x):
            print("⬛" if hull.get((x, y), 0) else "⬜", end = "")
        print()

if __name__ == "__main__":
    program = parse_input("input")

    # Part 1
    hull = {}
    Robot(Intcomp(program), hull).go()
    print(f"Panels painted: {len(hull)}")

    # Part 2
    hull = {(0, 0): 1}
    Robot(Intcomp(program), hull).go()
    render(hull)
