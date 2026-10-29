import itertools as it
list(it.combinations("ABC", 2))   # AB AC BC
list(it.permutations("AB"))       # AB BA
list(it.product([0, 1], repeat=2))# all 2-bit combinations
list(it.chain([1, 2], [3]))       # [1, 2, 3]
for key, grp in it.groupby(sorted(["apple", "avocado", "banana"]), key=lambda s: s[0]):
    print(key, list(grp))
