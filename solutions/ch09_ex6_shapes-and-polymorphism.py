import math

class Shape:
    def area(self) -> float:
        raise NotImplementedError

class Circle(Shape):
    def __init__(self, r): self.r = r
    def area(self): return math.pi * self.r ** 2

class Rectangle(Shape):
    def __init__(self, w, h): self.w, self.h = w, h
    def area(self): return self.w * self.h

class Triangle(Shape):
    def __init__(self, base, height): self.base, self.height = base, height
    def area(self): return 0.5 * self.base * self.height

shapes = [Circle(1), Rectangle(2, 3), Triangle(4, 5)]
print(round(sum(s.area() for s in shapes), 2))     # 19.14
