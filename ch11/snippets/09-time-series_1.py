import numpy as np
days = pd.date_range("2026-01-01", periods=90, freq="D")
visits = pd.Series(np.random.default_rng(1).poisson(200, 90), index=days)
weekly = visits.resample("W").sum()            # daily -> weekly totals
rolling = visits.rolling(7).mean()             # 7-day moving average
print(weekly.head(), rolling.tail())
print(visits.loc["2026-02"].mean())            # all of February
