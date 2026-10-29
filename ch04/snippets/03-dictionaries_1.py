server = {
    "hostname": "web01",
    "ip": "10.0.0.11",
    "cores": 8,
    "services": ["nginx", "ssh"],
}

print(server["ip"])                    # 10.0.0.11
print(server.get("ram", "unknown"))    # default if missing
server["ram_gb"] = 32                  # add
server["cores"] = 16                   # update
del server["ip"]                       # delete
print("hostname" in server)            # True (checks keys)
