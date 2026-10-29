class Product:
    tax_rate = 0.12                       # shared by all products

    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def price_with_tax(self) -> float:
        return round(self.price * (1 + Product.tax_rate), 2)

    def __str__(self):                    # used by print()
        return f"{self.name}: {self.price:,.2f}"

    def __repr__(self):                   # used in the REPL and debugger
        return f"Product({self.name!r}, {self.price})"

    def __eq__(self, other):
        return isinstance(other, Product) and (self.name, self.price) == (other.name, other.price)

    def __lt__(self, other):              # lets sorted() compare products
        return self.price < other.price

items = [Product("Mouse", 450), Product("Monitor", 8990), Product("Cable", 120)]
print(sorted(items))
print(max(items))
