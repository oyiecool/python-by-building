# payroll.py
OVERTIME_AFTER = 40       # hours per week
OVERTIME_RATE = 1.25

def gross_pay(hours: float, rate: float) -> float:
    regular = min(hours, OVERTIME_AFTER)
    overtime = max(hours - OVERTIME_AFTER, 0)
    return regular * rate + overtime * rate * OVERTIME_RATE

def deductions(gross: float, tax_rate: float = 0.10,
               insurance: float = 250.0, pension_rate: float = 0.045) -> dict:
    return {
        "tax": round(gross * tax_rate, 2),
        "insurance": insurance,
        "pension": round(gross * pension_rate, 2),
    }

def payslip(name: str, hours: float, rate: float) -> str:
    g = gross_pay(hours, rate)
    d = deductions(g)
    net = g - sum(d.values())
    lines = [f"PAYSLIP: {name}", f"Hours {hours}, rate {rate:.2f}",
             f"{'Gross':<12}{g:>12,.2f}"]
    for item, amount in d.items():
        lines.append(f"{item.title():<12}{-amount:>12,.2f}")
    lines.append(f"{'NET PAY':<12}{net:>12,.2f}")
    return "\n".join(lines)

if __name__ == "__main__":
    staff = [("Ana", 45, 150.0), ("Ben", 38, 175.0)]
    for name, hours, rate in staff:
        print(payslip(name, hours, rate), end="\n\n")
