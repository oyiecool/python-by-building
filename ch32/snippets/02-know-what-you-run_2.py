from importlib import metadata

for d in sorted(metadata.distributions(), key=lambda d: d.metadata["Name"].lower())[:3]:
    print(d.metadata["Name"], d.version)
