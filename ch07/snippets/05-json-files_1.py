import json

config = {"app": "monitor", "interval": 60, "hosts": ["web01", "db01"], "debug": False}

with open("config.json", "w", encoding="utf-8") as f:
    json.dump(config, f, indent=2)

with open("config.json", encoding="utf-8") as f:
    loaded = json.load(f)

text = json.dumps(loaded)          # to a string
back = json.loads(text)            # from a string
