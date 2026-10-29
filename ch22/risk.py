# risk.py - Chapter 22 mini project
"""Monte Carlo schedule risk: how likely is a project to finish on time?

Each task has optimistic, likely and pessimistic durations (days). We simulate the project
100,000 times with NumPy, drawing every task from a triangular distribution."""
import numpy as np

TASKS = {                         # name: (optimistic, most likely, pessimistic) in working days
    "Requirements":   (3, 5, 9),
    "Database design": (2, 4, 8),
    "Backend API":    (8, 12, 22),
    "Web front end":  (6, 10, 18),
    "Testing":        (4, 6, 12),
    "Deployment":     (1, 2, 5),
}
DEADLINE = 45
RUNS = 100_000


def simulate(tasks: dict, runs: int, seed: int = 42) -> np.ndarray:
    rng = np.random.default_rng(seed)
    lo, mode, hi = (np.array(v, dtype=float) for v in zip(*tasks.values()))
    # shape (runs, n_tasks): one row per simulated project, one column per task
    draws = rng.triangular(lo, mode, hi, size=(runs, len(tasks)))
    return draws.sum(axis=1)          # tasks run one after another


if __name__ == "__main__":
    totals = simulate(TASKS, RUNS)
    naive = sum(v[1] for v in TASKS.values())
    p50, p80, p95 = np.percentile(totals, [50, 80, 95])
    on_time = (totals <= DEADLINE).mean()
    print(f"Sum of 'most likely' estimates: {naive} days")
    print(f"Simulated median: {p50:.1f} days   80% sure: {p80:.1f}   95% sure: {p95:.1f}")
    print(f"Chance of finishing within {DEADLINE} days: {on_time:.1%}")
    counts, edges = np.histogram(totals, bins=np.arange(28, 66, 2))
    for c, e in zip(counts, edges):
        print(f"{e:>3.0f}-{e + 2:<3.0f} {'#' * (c // 800)}")
