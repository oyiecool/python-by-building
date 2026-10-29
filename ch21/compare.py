# compare.py - sequential vs threads vs processes
import math
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


def wait_for_network(n: int) -> int:
    time.sleep(0.5)                 # stands in for a slow web request or disk read
    return n


def count_primes(limit: int) -> int:
    """CPU-heavy: count primes below limit the slow way."""
    return sum(all(n % d for d in range(2, int(math.isqrt(n)) + 1)) for n in range(2, limit))


def timed(label, fn):
    t = time.perf_counter()
    fn()
    print(f"{label:<28}{time.perf_counter() - t:6.2f} s")


if __name__ == "__main__":                     # required for processes on Windows and macOS
    jobs = list(range(8))
    timed("I/O, sequential", lambda: [wait_for_network(j) for j in jobs])
    with ThreadPoolExecutor(8) as pool:
        timed("I/O, 8 threads", lambda: list(pool.map(wait_for_network, jobs)))

    limits = [200_000] * 4
    timed("CPU, sequential", lambda: [count_primes(n) for n in limits])
    with ThreadPoolExecutor(4) as pool:
        timed("CPU, 4 threads (GIL)", lambda: list(pool.map(count_primes, limits)))
    with ProcessPoolExecutor(4) as pool:
        timed("CPU, 4 processes", lambda: list(pool.map(count_primes, limits)))
