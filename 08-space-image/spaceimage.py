from collections import Counter

def parse_input(path):
    with open(path, "r") as input_file:
        for line in input_file:
            for char in line.strip():
                yield char

def print_image(image, width):
    for i, p in enumerate(image):
        if i % width == 0:
            print()
        if p == '0':
            print("⬜", end = "")
        else:
            print("⬛", end = "")

if __name__ == "__main__":
    w = 25
    h = 6

    layers = list(zip(*[iter(parse_input("input"))]*(w*h)))
    counters = map(Counter, layers)
    least_zeroes = sorted(counters, key = lambda c: c['0'])[0]
    checksum = least_zeroes['1'] * least_zeroes['2']
    print(f"Checksum for part 1: {checksum}.")

    rendered = [next(x for x in p if x != '2') for p in zip(*layers)]
    print("Image for part 2:")
    print_image(rendered, w)
    print()
