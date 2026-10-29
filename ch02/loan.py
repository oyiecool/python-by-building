# loan.py - monthly payment calculator
print("=== Loan Calculator ===")
principal = float(input("Loan amount: "))
annual_rate = float(input("Annual interest rate (%): "))
years = int(input("Term in years: "))

r = annual_rate / 12 / 100
n = years * 12

if r == 0:
    monthly = principal / n
else:
    monthly = principal * r * (1 + r) ** n / ((1 + r) ** n - 1)

total_paid = monthly * n
total_interest = total_paid - principal

print()
print(f"{'Monthly payment':<18}: {monthly:>14,.2f}")
print(f"{'Number of payments':<18}: {n:>14}")
print(f"{'Total paid':<18}: {total_paid:>14,.2f}")
print(f"{'Total interest':<18}: {total_interest:>14,.2f}")
print(f"{'Interest share':<18}: {total_interest / total_paid:>14.1%}")
