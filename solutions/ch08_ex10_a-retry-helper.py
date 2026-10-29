import logging, time
log = logging.getLogger("retry")

def retry(func, attempts: int = 3, delay: float = 1.0):
    for n in range(1, attempts + 1):
        try:
            return func()
        except Exception as err:
            log.warning("attempt %d/%d failed: %s", n, attempts, err)
            if n == attempts:
                raise
            time.sleep(delay)

def test_retry_succeeds_on_third_try():
    calls = {"n": 0}
    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise ConnectionError("temporary")
        return "ok"
    assert retry(flaky, delay=0) == "ok" and calls["n"] == 3
