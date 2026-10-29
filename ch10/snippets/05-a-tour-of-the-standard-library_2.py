from collections import Counter, defaultdict, deque, namedtuple
Counter("mississippi").most_common(2)          # [('i', 4), ('s', 4)]
groups = defaultdict(list); groups["IT"].append("Ana")
recent = deque(maxlen=3)                       # keeps only the last 3
for x in range(10): recent.append(x)           # deque([7, 8, 9])
Point = namedtuple("Point", "x y"); p = Point(2, 3); print(p.x)
