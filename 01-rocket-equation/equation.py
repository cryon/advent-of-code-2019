def main():
    module_masses = parse_input("input")

    modules_req = list(map(calculate_req, module_masses))
    modules_total = sum(modules_req)
    print(f"Fuel requirements for all modules: {modules_total}.")

    fuel_req = sum(map(lambda req: sum(fuel_req_gen(req)), modules_req))
    print(f"Additional fuel requrement to carry fuel: {fuel_req}.")

    total = modules_total + fuel_req
    print(f"Total fuel requirement: {total}.")

def calculate_req(mass):
    return max(mass // 3 - 2, 0)

def fuel_req_gen(fuel):
    req = calculate_req(fuel)
    while req > 0:
        yield req
        req = calculate_req(req)

def parse_input(path):
    with open(path, "r") as input_file:
        return map(int, input_file.readlines())

if __name__ == "__main__":
    main()
