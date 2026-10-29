# finance_dashboard.py - Capstone 1
import argparse
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent
DATA = BASE / "expenses.csv"
BUDGET = {"Food": 5500, "Transport": 1500, "Utilities": 4500, "Rent": 12000,
          "Entertainment": 2000, "Health": 1500, "Shopping": 2500}


def make_sample(path: Path = DATA, seed: int = 42) -> None:
    """Create 9 months of realistic sample expenses if no data exists."""
    rng = np.random.default_rng(seed)
    rows = []
    for month in pd.period_range("2026-01", "2026-09", freq="M"):
        days = month.days_in_month
        rows.append((f"{month}-01", "Rent", "Monthly rent", 12000))
        rows.append((f"{month}-05", "Utilities", "Electricity", round(rng.normal(2800, 400))))
        rows.append((f"{month}-07", "Utilities", "Internet", 1699))
        for _ in range(rng.integers(35, 50)):
            cat = rng.choice(["Food", "Transport", "Entertainment", "Health", "Shopping"],
                             p=[.5, .25, .1, .05, .1])
            mean = {"Food": 260, "Transport": 140, "Entertainment": 450, "Health": 600, "Shopping": 700}[cat]
            day = rng.integers(1, days + 1)
            rows.append((f"{month}-{day:02d}", cat, cat.lower(), round(abs(rng.normal(mean, mean * .4)))))
    df = pd.DataFrame(rows, columns=["date", "category", "description", "amount"])
    df.sort_values("date").to_csv(path, index=False)


def load(path: Path = DATA) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["date"])
    df["category"] = df["category"].str.strip().str.title()
    df = df[df["amount"] > 0].copy()
    df["month"] = df["date"].dt.to_period("M")
    return df


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    monthly = df.pivot_table(index="month", columns="category", values="amount",
                             aggfunc="sum", fill_value=0)
    monthly["Total"] = monthly.sum(axis=1)
    return monthly


def dashboard(df: pd.DataFrame, out: Path) -> None:
    import matplotlib.pyplot as plt
    monthly = summarize(df)
    total_budget = sum(BUDGET.values())
    last = monthly.index.max()
    this_month = df[df["month"] == last]

    fig, axes = plt.subplots(2, 2, figsize=(13, 8))
    fig.suptitle(f"Personal finance dashboard - through {last}", fontsize=15, fontweight="bold")

    ax = axes[0, 0]
    x = monthly.index.astype(str)
    ax.plot(x, monthly["Total"], marker="o", color="#2b6cb0", label="Spent")
    ax.axhline(total_budget, color="gray", linestyle="--", label=f"Budget {total_budget:,}")
    over = monthly["Total"] > total_budget
    ax.scatter(x[over], monthly["Total"][over], color="crimson", zorder=3, label="Over budget")
    ax.set(title="Monthly spending vs budget", ylabel="Amount")
    ax.set_ylim(0)
    ax.tick_params(axis="x", rotation=45)
    ax.legend()

    ax = axes[0, 1]
    cats = this_month.groupby("category")["amount"].sum().sort_values()
    budget = pd.Series(BUDGET).reindex(cats.index).fillna(0)
    colors = ["crimson" if s > b else "#b0b7c3" for s, b in zip(cats, budget)]
    ax.barh(cats.index, cats.values, color=colors)
    ax.scatter(budget.values, cats.index, marker="|", s=300, color="black", label="Budget")
    ax.set(title=f"{last}: spending by category (red = over budget)", xlabel="Amount")
    ax.legend()

    ax = axes[1, 0]
    daily = this_month.groupby(this_month["date"].dt.day)["amount"].sum()
    days = range(1, last.days_in_month + 1)
    cumulative = daily.reindex(days, fill_value=0).cumsum()
    ax.plot(list(days), cumulative.values, color="#2b6cb0", label="Actual")
    ax.plot([1, last.days_in_month], [0, total_budget], color="gray", linestyle="--", label="Even pace")
    ax.set(title=f"{last}: cumulative spending", xlabel="Day of month", ylabel="Amount")
    ax.legend()

    ax = axes[1, 1]
    top = (df.groupby("category")["amount"].sum() / df["amount"].sum()).sort_values()
    ax.barh(top.index, top.values * 100, color="#2b6cb0")
    for i, v in enumerate(top.values * 100):
        ax.text(v + 0.5, i, f"{v:.0f}%", va="center")
    ax.set(title="Share of all spending", xlabel="%")

    fig.tight_layout()
    fig.savefig(out, dpi=150)
    print(f"Dashboard saved to {out}")


def report(df: pd.DataFrame) -> None:
    monthly = summarize(df)
    total_budget = sum(BUDGET.values())
    print(f"{'Month':<9}{'Spent':>12}{'Budget':>12}{'Diff':>12}")
    for month, spent in monthly["Total"].items():
        print(f"{str(month):<9}{spent:>12,.0f}{total_budget:>12,.0f}{total_budget - spent:>+12,.0f}")
    avg = monthly["Total"].mean()
    print(f"\nAverage month: {avg:,.0f}   Projected year: {avg * 12:,.0f}")
    worst = monthly.drop(columns="Total").mean().sub(pd.Series(BUDGET)).sort_values(ascending=False)
    print(f"Category most over budget on average: {worst.index[0]} ({worst.iloc[0]:+,.0f}/month)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Personal finance dashboard")
    ap.add_argument("--csv", type=Path, default=DATA)
    ap.add_argument("--out", type=Path, default=BASE / "finance_dashboard.png")
    ap.add_argument("--no-show", action="store_true", help="save only, do not open a window")
    args = ap.parse_args()
    if args.no_show:
        matplotlib.use("Agg")
    if not args.csv.exists():
        print("No data found, creating sample expenses.csv")
        make_sample(args.csv)
    data = load(args.csv)
    report(data)
    dashboard(data, args.out)
    if not args.no_show:
        import matplotlib.pyplot as plt
        plt.show()
