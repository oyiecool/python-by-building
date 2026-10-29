# vault.py - Capstone 12
"""An encrypted command-line password vault.

The vault file holds a random salt and an encrypted JSON blob. The key is derived from your
master password with PBKDF2 (600,000 iterations), and the data is encrypted with Fernet
(AES-128-CBC + HMAC-SHA256) from the 'cryptography' package. Without the master password the
file is useless; with a wrong password decryption fails instead of returning garbage.
"""
import argparse
import base64
import getpass
import json
import os
import secrets
import string
import sys
from datetime import datetime
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

VAULT = Path(os.environ.get("VAULT_FILE", Path.home() / ".pyvault"))
ITERATIONS = 600_000


def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITERATIONS)
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


class Vault:
    def __init__(self, path: Path, password: str):
        self.path, self.password = path, password
        if path.exists():
            raw = json.loads(path.read_text())
            self.salt = base64.b64decode(raw["salt"])
            try:
                plain = Fernet(derive_key(password, self.salt)).decrypt(raw["data"].encode())
            except InvalidToken:
                raise SystemExit("Wrong master password (or the vault file was tampered with).")
            self.entries: dict[str, dict] = json.loads(plain)
        else:
            self.salt = secrets.token_bytes(16)
            self.entries = {}

    def save(self) -> None:
        token = Fernet(derive_key(self.password, self.salt)).encrypt(json.dumps(self.entries).encode())
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps({"version": 1, "salt": base64.b64encode(self.salt).decode(),
                                   "data": token.decode()}))
        tmp.replace(self.path)                 # atomic: never leaves a half-written vault
        if os.name == "posix":
            os.chmod(self.path, 0o600)         # readable by you only

    def add(self, site: str, username: str, password: str, note: str = "") -> None:
        self.entries[site.lower()] = {"username": username, "password": password, "note": note,
                                      "updated": datetime.now().isoformat(timespec="seconds")}
        self.save()

    def get(self, site: str) -> dict | None:
        return self.entries.get(site.lower())

    def delete(self, site: str) -> bool:
        if self.entries.pop(site.lower(), None) is None:
            return False
        self.save()
        return True

    def search(self, text: str = "") -> list[str]:
        return sorted(s for s in self.entries if text.lower() in s)


def generate(length: int = 20, symbols: bool = True) -> str:
    pool = string.ascii_letters + string.digits + ("!@#$%^&*-_=+" if symbols else "")
    while True:
        pw = "".join(secrets.choice(pool) for _ in range(length))
        if any(c.islower() for c in pw) and any(c.isupper() for c in pw) and any(c.isdigit() for c in pw):
            return pw


def strength(pw: str) -> str:
    kinds = sum([any(c.islower() for c in pw), any(c.isupper() for c in pw),
                 any(c.isdigit() for c in pw), any(not c.isalnum() for c in pw)])
    if len(pw) >= 16 and kinds >= 3:
        return "strong"
    if len(pw) >= 12 and kinds >= 3:
        return "ok"
    return "weak"


def master_password(confirm: bool) -> str:
    if env := os.environ.get("VAULT_PASSWORD"):         # for automated tests only
        return env
    pw = getpass.getpass("Master password: ")
    if confirm:
        if len(pw) < 12:
            sys.exit("Use a master password of at least 12 characters.")
        if getpass.getpass("Repeat master password: ") != pw:
            sys.exit("Passwords do not match.")
    return pw


def main(argv=None):
    ap = argparse.ArgumentParser(description="Encrypted password vault")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add", help="store a login")
    a.add_argument("site")
    a.add_argument("username")
    a.add_argument("--generate", type=int, metavar="LENGTH", help="create a random password")
    a.add_argument("--note", default="")
    g = sub.add_parser("get", help="show a login")
    g.add_argument("site")
    sub.add_parser("list", help="list sites").add_argument("filter", nargs="?", default="")
    sub.add_parser("delete", help="remove a login").add_argument("site")
    sub.add_parser("gen", help="just print a random password").add_argument("length", nargs="?", type=int, default=20)
    sub.add_parser("audit", help="find weak and reused passwords")
    args = ap.parse_args(argv)

    if args.cmd == "gen":
        print(generate(args.length))
        return
    vault = Vault(VAULT, master_password(confirm=not VAULT.exists()))
    if args.cmd == "add":
        pw = generate(args.generate) if args.generate else getpass.getpass(f"Password for {args.site}: ")
        vault.add(args.site, args.username, pw, args.note)
        print(f"Saved {args.site} ({strength(pw)} password).")
    elif args.cmd == "get":
        e = vault.get(args.site)
        if not e:
            sys.exit(f"No entry for {args.site}")
        print(f"Site:     {args.site}\nUsername: {e['username']}\nPassword: {e['password']}")
        if e["note"]:
            print(f"Note:     {e['note']}")
    elif args.cmd == "list":
        for s in vault.search(args.filter):
            print(f"{s:<30}{vault.entries[s]['username']}")
    elif args.cmd == "delete":
        print("Deleted." if vault.delete(args.site) else "Not found.")
    elif args.cmd == "audit":
        seen: dict[str, list[str]] = {}
        for site, e in vault.entries.items():
            seen.setdefault(e["password"], []).append(site)
            if strength(e["password"]) == "weak":
                print(f"WEAK      {site}")
        for sites in seen.values():
            if len(sites) > 1:
                print(f"REUSED    {', '.join(sorted(sites))}")
        print(f"Audited {len(vault.entries)} entries.")


if __name__ == "__main__":
    main()
