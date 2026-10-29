import asyncio
import time

async def brew(name: str, seconds: float) -> str:
    print(f"start {name}")
    await asyncio.sleep(seconds)        # a non-blocking wait
    print(f"done  {name}")
    return name

async def main():
    t = time.perf_counter()
    results = await asyncio.gather(brew("coffee", 3), brew("toast", 2), brew("eggs", 1))
    print(results, f"{time.perf_counter() - t:.1f} s")   # about 3 s, not 6

asyncio.run(main())
