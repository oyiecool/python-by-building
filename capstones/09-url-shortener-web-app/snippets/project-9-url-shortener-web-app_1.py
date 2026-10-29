import requests
r = requests.post("http://127.0.0.1:5000/api/links", json={"url": "https://docs.python.org/3/", "code": "pydocs"})
print(r.status_code, r.json())     # 201 {'code': 'pydocs', 'short_url': 'http://127.0.0.1:5000/pydocs'}
