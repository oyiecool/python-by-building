for key in server:
    print(key)
for key, value in server.items():
    print(f"{key:>10}: {value}")
print(list(server.keys()), list(server.values()))
