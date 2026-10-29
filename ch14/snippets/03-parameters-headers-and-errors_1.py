import requests

def search_repos(term: str, n: int = 5):
    url = "https://api.github.com/search/repositories"
    params = {"q": term, "sort": "stars", "order": "desc", "per_page": n}
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "python-by-building"}
    try:
        r = requests.get(url, params=params, headers=headers, timeout=10)
        r.raise_for_status()                 # raises HTTPError for 4xx/5xx
    except requests.exceptions.Timeout:
        print("The server took too long.")
        return []
    except requests.exceptions.HTTPError as e:
        print("HTTP error:", e.response.status_code, e.response.text[:200])
        return []
    except requests.exceptions.ConnectionError:
        print("No network connection.")
        return []
    return [(i["full_name"], i["stargazers_count"]) for i in r.json()["items"]]

for name, stars in search_repos("web scraping python"):
    print(f"{stars:>8,}  {name}")
