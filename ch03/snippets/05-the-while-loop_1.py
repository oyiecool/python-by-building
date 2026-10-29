balance = 1000.0
years = 0
while balance < 2000:
    balance *= 1.06
    years += 1
print(f"Doubled in {years} years: {balance:,.2f}")
