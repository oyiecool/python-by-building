import requests
from bs4 import BeautifulSoup

html = requests.get("https://books.toscrape.com/", timeout=10).text
soup = BeautifulSoup(html, "html.parser")

for book in soup.select("article.product_pod")[:5]:
    title = book.h3.a["title"]
    price = book.select_one("p.price_color").get_text()
    rating = book.select_one("p.star-rating")["class"][1]   # e.g. "Three"
    print(f"{price:>8}  {rating:<6} {title}")
