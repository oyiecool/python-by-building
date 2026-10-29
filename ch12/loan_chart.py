# loan_chart.py
import matplotlib.pyplot as plt

def schedule(principal, annual_rate, years):
    r, n = annual_rate / 12 / 100, years * 12
    payment = principal * r * (1 + r) ** n / ((1 + r) ** n - 1)
    balance, rows = principal, []
    for month in range(1, n + 1):
        interest = balance * r
        principal_part = payment - interest
        balance -= principal_part
        rows.append((month, principal_part, interest, max(balance, 0)))
    return payment, rows

def yearly(rows):
    years = {}
    for month, p, i, _ in rows:
        y = (month - 1) // 12 + 1
        prev = years.get(y, (0, 0))
        years[y] = (prev[0] + p, prev[1] + i)
    return years

if __name__ == "__main__":
    payment, rows = schedule(1_500_000, 7, 20)
    yrs = yearly(rows)
    x = list(yrs)
    principal = [v[0] for v in yrs.values()]
    interest = [v[1] for v in yrs.values()]
    cross = next(y for y in x if yrs[y][0] > yrs[y][1])

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    ax1.bar(x, principal, label="Principal", color="#b0b7c3")
    ax1.bar(x, interest, bottom=principal, label="Interest", color="#2b6cb0")
    ax1.axvline(cross - 0.5, linestyle="--", color="gray")
    ax1.set(title=f"Interest outweighs principal until year {cross}",
            xlabel="Year", ylabel="Amount paid")
    ax1.legend()

    ax2.plot([r[0] for r in rows], [r[3] for r in rows])
    ax2.set(title=f"Remaining balance (monthly payment {payment:,.2f})",
            xlabel="Month", ylabel="Balance")
    ax2.set_ylim(0)
    fig.tight_layout()
    fig.savefig("loan_chart.png", dpi=150)
    plt.show()
