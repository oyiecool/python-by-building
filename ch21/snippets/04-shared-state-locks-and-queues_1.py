import threading

counter = 0
lock = threading.Lock()

def add_many(n):
    global counter
    for _ in range(n):
        with lock:                  # only one thread at a time inside this block
            counter += 1

threads = [threading.Thread(target=add_many, args=(100_000,)) for _ in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()                        # wait for all to finish
print(counter)                      # always 400000
