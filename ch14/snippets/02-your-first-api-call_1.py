import requests

r = requests.get("https://api.github.com/users/python", timeout=10)
print(r.status_code)                  # 200
print(r.headers["Content-Type"])
data = r.json()                       # parse JSON into a dict
print(data["name"], data["public_repos"], data["followers"])
