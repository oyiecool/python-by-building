def dedupe(items):
    seen, out = set(), []
    for x in items:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out

print(dedupe([3, 1, 3, 2, 1, 5]))            # [3, 1, 2, 5]
print(list(dict.fromkeys([3, 1, 3, 2, 1, 5])))  # same, in one line
