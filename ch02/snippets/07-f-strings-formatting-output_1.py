name = "Ana"
score = 92.456
print(f"{name} scored {score:.1f}%")      # Ana scored 92.5%
print(f"{1234567.891:,.2f}")              # 1,234,567.89
print(f"|{'left':<10}|{'right':>10}|")    # padding and alignment
print(f"|{'centre':^12}|")
print(f"{0.075:.1%}")                     # 7.5%
print(f"{255:b} {255:x}")                 # binary and hex: 11111111 ff
print(f"{score=}")                        # debugging: score=92.456
