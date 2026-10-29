def area_of_circle(radius):
    return 3.14159 * radius ** 2

def min_max(values):
    return min(values), max(values)     # returns a tuple

a = area_of_circle(2)
low, high = min_max([4, 9, 1, 7])
print(round(a, 2), low, high)
