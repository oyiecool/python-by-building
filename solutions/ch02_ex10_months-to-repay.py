def months_to_repay(principal: float, annual_rate: float, payment: float) -> tuple[int, float]:
    r = annual_rate / 12 / 100
    balance, months, interest = principal, 0, 0.0
    while balance > 0:
        i = balance * r
        if payment <= i:
            raise ValueError("payment too small to ever repay")
        interest += i
        balance = balance + i - payment
        months += 1
    return months, round(interest, 2)

print(months_to_repay(1_500_000, 7, 11_629.49))   # (240, 1291074.49)
print(months_to_repay(1_500_000, 7, 16_629.49))   # (129, 635497.21)
