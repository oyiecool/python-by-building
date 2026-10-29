key, _, value = "timeout = 30".partition("=")
print(key.strip(), int(value))
