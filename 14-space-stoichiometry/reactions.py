from re import findall
from collections import namedtuple as nt
from math import ceil
from itertools import count

Quantity = nt("Quantity", "name amount")
Recipe = nt("Recipe", "produce consume")

def required_ore(recipes, stock, wanted):
    if wanted.name == "ORE":
        stock["ORE"] = stock.setdefault("ORE", 0) + wanted.amount
        return wanted.amount
    recipe = recipes[wanted.name]
    batches = ceil(wanted.amount / recipe.produce.amount)
    total_ore = 0
    for item in recipe.consume:
        available = stock.get(item.name, 0)
        required = item.amount * batches
        if available < required:
            total_ore += required_ore(recipes, stock, Quantity(item.name, required - available))
        stock[item.name] -= required
    stock[wanted.name] = stock.setdefault(wanted.name, 0) + batches * recipe.produce.amount
    return total_ore

def bin_search(predicate, low, high):
    result = 0
    while low < high:
        mid = low + (high - low) // 2
        if predicate(mid): result = high = mid
        else: low = mid + 1
    return result

def parse_input(path):
    recipes = {}
    with open(path, "r") as input_file:
        for line in input_file:
            quantities = [Quantity(x.split()[1], int(x.split()[0])) for x in findall("\d+ \w+", line)]
            produced = quantities[-1]
            recipes[produced.name] = Recipe(produced, quantities[:-1])
    return recipes

if __name__ == "__main__":
    recipes = parse_input("input")
    print(f"Part 1: {required_ore(recipes, {}, Quantity('FUEL', 1))} ORE")

    predicate = lambda i: required_ore(recipes, {}, Quantity("FUEL", i)) > 1000000000000
    print(f"Part 2: {bin_search(predicate, 0, 10000000) - 1} FUEL")
