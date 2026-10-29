# app.py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Hello from Flask</h1><p>It works.</p>"

@app.route("/hello/<name>")
def hello(name):
    return f"<h1>Hello, {name.title()}!</h1>"

@app.route("/square/<int:n>")
def square(n):
    return {"n": n, "square": n * n}          # a dict becomes JSON

if __name__ == "__main__":
    app.run(debug=True)
