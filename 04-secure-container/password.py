from itertools import groupby

def valid_passwords(start, end, grp_len_pred):
    for pwd in range(start, end + 1):
        digits = [int(d) for d in str(pwd)]
        if digits != sorted(digits): continue
        if grp_len_pred({len(list(n)) for d, n in groupby(digits)}):
            yield pwd

if __name__ == "__main__":
    valid1 = valid_passwords(367479, 893698, lambda g: max(g) > 1)
    print(f"Part 1: {len(list(valid1))}")

    valid2 = list(valid_passwords(367479, 893698, lambda g: 2 in g))
    print(f"Part 2: {len(list(valid2))}")
