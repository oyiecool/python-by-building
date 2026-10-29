# main.py
from fastapi import FastAPI

app = FastAPI(title="Hello API")

@app.get("/")
def root():
    return {"message": "Hello from FastAPI"}

@app.get("/square/{n}")
def square(n: int):                         # the type hint does the validation
    return {"n": n, "square": n * n}

@app.get("/greet")
def greet(name: str = "world", shout: bool = False):   # query parameters: /greet?name=Ana&shout=true
    text = f"Hello, {name}!"
    return {"greeting": text.upper() if shout else text}
