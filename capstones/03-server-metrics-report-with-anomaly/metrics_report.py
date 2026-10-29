# metrics_report.py - Capstone 3
"""Analyze health_history.csv from Chapter 13: daily profile, anomalies, disk forecast."""
import argparse
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent
CSV = BASE / "health_history.csv"
DISK_LIMIT = 90.0


def make_sample(path: Path = CSV, days: int = 14, seed: int = 5) -> None:
    """Two weeks of 5-minute readings with a business-hours pattern and a few incidents."""
    rng = np.random.default_rng(seed)
    t = pd.date_range("2026-10-12", periods=days * 288, freq="5min")
    hour = np.asarray(t.hour + t.minute / 60)
    weekday = np.asarray(t.dayofweek < 5)
    office = np.exp(-((hour - 14) ** 2) / 18) * np.where(weekday, 45, 12)
    cpu = np.clip(12 + office + rng.normal(0, 4, len(t)), 1, 100)
    spikes = rng.choice(len(t), 6, replace=False)
    for s in spikes:
        cpu[s:s + 4] = rng.uniform(92, 99)
    mem = np.clip(48 + 0.4 * office + rng.normal(0, 2, len(t)), 5, 100)
    disk = 71 + np.arange(len(t)) * (6 / len(t)) + rng.normal(0, 0.05, len(t))
    pd.DataFrame({"time": t.strftime("%Y-%m-%dT%H:%M:%S"), "host": "web01",
                  "cpu": cpu.round(1), "mem": mem.round(1), "disk": disk.round(2),
                  "down": ""}).to_csv(path, index=False)


def load(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["time"]).set_index("time").sort_index()
    return df[["cpu", "mem", "disk"]].astype(float)


def find_anomalies(cpu: pd.Series, window: int = 36, z: float = 3.0, min_jump: float = 20) -> pd.Series:
    """Readings far above the previous 3 hours: more than z standard deviations
    AND at least min_jump percentage points above the rolling mean."""
    mean = cpu.rolling(window, min_periods=12).mean().shift(1)
    std = cpu.rolling(window, min_periods=12).std().shift(1)
    jump = cpu - mean
    return cpu[(jump > z * std) & (jump > min_jump)]


def disk_forecast(disk: pd.Series) -> tuple[float, pd.Timestamp | None]:
    """Fit a straight line to disk usage; return growth per day and the date it hits the limit."""
    days = (disk.index - disk.index[0]).total_seconds() / 86400
    slope, intercept = np.polyfit(days, disk.values, 1)
    if slope <= 0:
        return slope, None
    days_to_limit = (DISK_LIMIT - intercept) / slope
    return slope, disk.index[0] + pd.Timedelta(days=days_to_limit)


def report(df: pd.DataFrame) -> dict:
    hourly = df["cpu"].groupby(df.index.hour).mean()
    daily = df.resample("D").agg({"cpu": ["mean", "max"], "mem": "max", "disk": "last"})
    anomalies = find_anomalies(df["cpu"])
    growth, full_on = disk_forecast(df["disk"])
    print(f"Readings: {len(df):,} from {df.index[0]:%Y-%m-%d} to {df.index[-1]:%Y-%m-%d}")
    print(f"Busiest hour of day: {hourly.idxmax():02d}:00 (avg CPU {hourly.max():.0f}%)")
    print(f"Quietest hour:       {hourly.idxmin():02d}:00 (avg CPU {hourly.min():.0f}%)")
    print(f"CPU anomalies: {len(anomalies)} readings")
    for ts, v in anomalies.head(10).items():
        print(f"   {ts:%a %Y-%m-%d %H:%M}  {v:.0f}%")
    print(f"Disk grows {growth:.2f} points/day; reaches {DISK_LIMIT:.0f}% around "
          f"{full_on:%Y-%m-%d}" if full_on is not None else "Disk usage is not growing")
    print("\nDaily summary:")
    print(daily.round(1).to_string())
    return {"hourly": hourly, "anomalies": anomalies, "growth": growth, "full_on": full_on}


def plot(df: pd.DataFrame, r: dict, out: Path) -> None:
    import matplotlib.pyplot as plt
    fig, (a1, a2, a3) = plt.subplots(3, 1, figsize=(12, 10))
    a1.plot(df.index, df["cpu"], linewidth=0.6, color="#9aa5b1", label="CPU %")
    a1.plot(df["cpu"].rolling(12).mean(), color="#2b6cb0", label="1-hour average")
    a1.scatter(r["anomalies"].index, r["anomalies"].values, color="crimson", zorder=3, label="Anomaly")
    a1.set(title=f"CPU: {len(r['anomalies'])} anomalous readings", ylabel="%", ylim=(0, 100))
    a1.legend(loc="upper left")

    a2.bar(r["hourly"].index, r["hourly"].values,
           color=["#2b6cb0" if h == r["hourly"].idxmax() else "#b0b7c3" for h in r["hourly"].index])
    a2.set(title=f"Average CPU by hour of day: peak at {r['hourly'].idxmax():02d}:00",
           xlabel="Hour", ylabel="%", xticks=range(0, 24, 2))

    a3.plot(df.index, df["disk"], color="#2b6cb0", label="Disk used %")
    a3.axhline(DISK_LIMIT, color="crimson", linestyle="--", label=f"Limit {DISK_LIMIT:.0f}%")
    if r["full_on"] is not None:
        future = pd.date_range(df.index[0], r["full_on"], periods=50)
        days = (future - df.index[0]).total_seconds() / 86400
        start = df["disk"].iloc[:12].mean()
        a3.plot(future, start + r["growth"] * days, color="gray", linestyle=":", label="Trend")
        a3.set_title(f"Disk grows {r['growth']:.2f} pts/day: full around {r['full_on']:%d %b %Y}")
    a3.set(ylabel="%")
    a3.legend(loc="upper left")
    fig.tight_layout()
    fig.savefig(out, dpi=140)
    print(f"\nChart saved to {out}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", type=Path, default=CSV)
    ap.add_argument("--no-show", action="store_true")
    a = ap.parse_args()
    if a.no_show:
        matplotlib.use("Agg")
    if not a.csv.exists():
        make_sample(a.csv)
        print("Created sample data", a.csv.name)
    data = load(a.csv)
    result = report(data)
    plot(data, result, BASE / "metrics_report.png")
    if not a.no_show:
        import matplotlib.pyplot as plt
        plt.show()
