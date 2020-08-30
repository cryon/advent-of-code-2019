from intcomp import Intcomp, parse_input

class ArgumentCombiner:
    def __init__(self, function):
        self.function = function
        self.mem = []
        self.arity = function.__code__.co_argcount - 1

    def __call__(self, argument):
        self.mem.append(argument)
        if len(self.mem) == self.arity:
            self.function(*self.mem)
            self.mem = []

def cmp(a, b):
    return (a > b) - (a < b)

class Arcade:
    def __init__(self, game_code):
        self.comp = Intcomp(game_code)
        self.comp.output_func = ArgumentCombiner(self.process_output)
        self.comp.input_func = self.process_input

        self.screen = {}
        self.score = 0
        self.ball_x = 0
        self.paddle_x = 0

    def process_input(self):
        return cmp(self.ball_x - self.paddle_x, 0)

    def process_output(self, x, y, tile_id):
        if x == -1 and y == 0:
            self.score = tile_id
        else:
            self.screen[(x, y)] = tile_id

            if tile_id == 4:
                self.ball_x = x

            if tile_id == 3:
                self.paddle_x = x

    def play(self):
        self.comp.run()

if __name__ == "__main__":
    game = parse_input("input")
    arcade = Arcade(game)
    arcade.play()

    num_blocks = sum(tile == 2 for tile in arcade.screen.values())
    print(f"Part 1: There are {num_blocks} blocks in the screen")

    game[0] = 2
    arcade = Arcade(game)
    arcade.play()
    print(f"Part 2: The final score is {arcade.score}")
