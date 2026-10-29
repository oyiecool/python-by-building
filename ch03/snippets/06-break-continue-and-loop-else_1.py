for n in range(2, 30):
    for d in range(2, int(n ** 0.5) + 1):
        if n % d == 0:
            break          # not prime
    else:
        print(n, "is prime")
