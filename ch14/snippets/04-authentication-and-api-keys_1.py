import os, requests
token = os.environ["GITHUB_TOKEN"]          # set in your shell or a .env file
r = requests.get("https://api.github.com/user",
                 headers={"Authorization": f"Bearer {token}"}, timeout=10)
