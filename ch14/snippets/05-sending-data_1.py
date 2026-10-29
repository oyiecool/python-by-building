import requests
# httpbin.org echoes back whatever you send: great for practice
r = requests.post("https://httpbin.org/post", json={"name": "Ana", "role": "admin"}, timeout=10)
print(r.json()["json"])

# a chat webhook alert (Slack, Discord, Teams use similar JSON)
# requests.post(os.environ["WEBHOOK_URL"], json={"text": "Disk 92% on web01"}, timeout=10)
