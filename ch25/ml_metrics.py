# ml_metrics.py - Chapter 25 mini project
"""Learn a server's normal CPU pattern with scikit-learn, then flag readings the model did not expect."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

CSV = Path(__file__).resolve().parent / "health_history.csv"     # from Chapter 13 / Capstone 3


def features(df: pd.DataFrame) -> pd.DataFrame:
    t = df["time"]
    return pd.DataFrame({
        "hour": t.dt.hour + t.dt.minute / 60,
        "weekday": t.dt.dayofweek,
        "is_weekend": (t.dt.dayofweek >= 5).astype(int),
    })   # only things known in advance: no memory reading, which rises WITH cpu (a leak)


def main() -> None:
    if not CSV.exists():
        sys.exit("Run metrics_report.py (Capstone 3) first to create health_history.csv")
    df = pd.read_csv(CSV, parse_dates=["time"])
    X, y = features(df), df["cpu"]

    # 1. Regression: predict normal CPU from the calendar alone
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)
    baseline = np.full(len(y_test), y_train.mean())
    model = RandomForestRegressor(n_estimators=200, min_samples_leaf=5, random_state=0, n_jobs=-1)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    print(f"Baseline (always predict the mean): MAE {mean_absolute_error(y_test, baseline):5.1f} points")
    print(f"Random forest:                      MAE {mean_absolute_error(y_test, pred):5.1f} points, "
          f"R² {r2_score(y_test, pred):.2f}")
    importance = sorted(zip(model.feature_importances_, X.columns), reverse=True)
    print("What drives CPU:", ", ".join(f"{name} {imp:.0%}" for imp, name in importance))

    # 2. Surprises: readings far above what the model expected for that moment
    df["expected"] = model.predict(X)
    df["surprise"] = df["cpu"] - df["expected"]
    big = df[df["surprise"] > 30].sort_values("surprise", ascending=False)
    print(f"\n{len(big)} readings more than 30 points above expectation:")
    for _, r in big.head(8).iterrows():
        print(f"  {r['time']:%a %d %b %H:%M}  cpu {r['cpu']:5.1f}%  expected {r['expected']:5.1f}%")

    # 3. Unsupervised: Isolation Forest finds unusual (hour, cpu, mem) combinations with no labels at all
    iso = IsolationForest(contamination=0.01, random_state=0)
    df["outlier"] = iso.fit_predict(pd.DataFrame({"hour": X["hour"], "cpu": df["cpu"], "mem": df["mem"]})) == -1
    both = df[df["outlier"] & (df["surprise"] > 30)]
    print(f"\nIsolation Forest flagged {df['outlier'].sum()} readings; {len(both)} agree with the regression.")


if __name__ == "__main__":
    main()
