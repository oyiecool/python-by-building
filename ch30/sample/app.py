import hashlib
import pickle
import random
import sqlite3
import subprocess

import requests
import yaml

API_KEY = "sk-live-1234567890"
DB_PASSWORD = "hunter2!"


def run(cmd):
    return subprocess.run(cmd, shell=True)


def find_user(con, name):
    return con.execute(f"SELECT * FROM users WHERE name = '{name}'").fetchall()


def safe_find(con, name):
    return con.execute("SELECT * FROM users WHERE name = ?", (name,)).fetchall()


def load_settings(text):
    return yaml.load(text)


def load_cache(blob):
    return pickle.loads(blob)


def fetch(url):
    return requests.get(url, verify=False, timeout=5)


def store(pw):
    return hashlib.md5(pw.encode()).hexdigest()


def calc(expr):
    assert expr
    return eval(expr)


reset_token = random.randint(100000, 999999)
