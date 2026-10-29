total = int(input("Seconds: "))
hours, rest = divmod(total, 3600)
minutes, seconds = divmod(rest, 60)
print(f"{hours}h {minutes}m {seconds}s")      # 3725 -> 1h 2m 5s
