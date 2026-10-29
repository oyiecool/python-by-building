tax_rate = 0.12                 # global

def price_with_tax(price):
    total = price * (1 + tax_rate)   # reads global; total is local
    return total

print(price_with_tax(100))
# print(total)  -> NameError: total only existed inside the function
