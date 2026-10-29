class Temperature:
    def __init__(self, celsius: float):
        self.celsius = celsius

    @classmethod
    def from_fahrenheit(cls, f: float):     # alternative constructor
        return cls((f - 32) * 5 / 9)

    @staticmethod
    def is_freezing(c: float) -> bool:      # utility, needs no object
        return c <= 0

t = Temperature.from_fahrenheit(98.6)
print(round(t.celsius, 1), Temperature.is_freezing(t.celsius))
