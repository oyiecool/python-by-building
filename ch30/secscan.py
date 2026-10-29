# secscan.py - Chapter 30 mini project
"""A small static security checker for Python code. It parses each file into a syntax tree (ast)
and reports risky patterns with file, line and advice. A teaching tool: use bandit for real audits."""
import argparse
import ast
import re
import sys
from pathlib import Path

SECRET_NAME = re.compile(r"(pass(word|wd)?|secret|token|api_?key)", re.I)
RULES = {
    "S1": ("high", "eval()/exec() runs arbitrary code", "parse the data instead (json, ast.literal_eval)"),
    "S2": ("high", "subprocess with shell=True", "pass a list of arguments and keep shell=False"),
    "S3": ("high", "pickle/marshal load of possibly untrusted data", "use json for data from outside"),
    "S4": ("high", "yaml.load without SafeLoader", "use yaml.safe_load"),
    "S5": ("high", "SQL built with an f-string, + or %", "use ? placeholders (Chapter 16)"),
    "S6": ("medium", "hard-coded secret", "read it from an environment variable or a secrets manager"),
    "S7": ("medium", "TLS verification disabled (verify=False)", "fix the certificate; never ship verify=False"),
    "S8": ("medium", "weak hash md5/sha1", "use hashlib.sha256 for checksums, hashlib.scrypt for passwords"),
    "S9": ("low", "random used for something that looks secret", "use the secrets module"),
    "S10": ("low", "assert used for a check", "asserts vanish with python -O; raise an exception"),
}


def call_name(node: ast.Call) -> str:
    f = node.func
    parts = []
    while isinstance(f, ast.Attribute):
        parts.append(f.attr)
        f = f.value
    if isinstance(f, ast.Name):
        parts.append(f.id)
    return ".".join(reversed(parts))


def kw(node: ast.Call, name: str):
    return next((k.value for k in node.keywords if k.arg == name), None)


class Checker(ast.NodeVisitor):
    def __init__(self):
        self.found: list[tuple[int, str]] = []

    def add(self, node, rule):
        self.found.append((node.lineno, rule))

    def visit_Call(self, node: ast.Call):
        name = call_name(node)
        if name in ("eval", "exec"):
            self.add(node, "S1")
        if name.startswith("subprocess.") or name in ("os.system", "os.popen"):
            shell = kw(node, "shell")
            if name in ("os.system", "os.popen") or (isinstance(shell, ast.Constant) and shell.value is True):
                self.add(node, "S2")
        if name in ("pickle.load", "pickle.loads", "marshal.load", "marshal.loads"):
            self.add(node, "S3")
        if name == "yaml.load":
            loader = kw(node, "Loader")
            if loader is None or "Safe" not in ast.unparse(loader):
                self.add(node, "S4")
        if name.endswith(("execute", "executemany", "executescript")) and node.args:
            q = node.args[0]
            if isinstance(q, ast.JoinedStr) or (isinstance(q, ast.BinOp) and isinstance(q.op, (ast.Add, ast.Mod))):
                self.add(node, "S5")
        v = kw(node, "verify")
        if isinstance(v, ast.Constant) and v.value is False:
            self.add(node, "S7")
        if name in ("hashlib.md5", "hashlib.sha1"):
            self.add(node, "S8")
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign):
        for t in node.targets:
            target = t.id if isinstance(t, ast.Name) else t.attr if isinstance(t, ast.Attribute) else ""
            v = node.value
            if SECRET_NAME.search(target) and isinstance(v, ast.Constant) and isinstance(v.value, str) and len(v.value) >= 6:
                self.add(node, "S6")
            if (SECRET_NAME.search(target) and isinstance(v, ast.Call)
                    and call_name(v).startswith("random.")):
                self.add(node, "S9")
        self.generic_visit(node)

    def visit_Assert(self, node: ast.Assert):
        self.add(node, "S10")
        self.generic_visit(node)


def scan(paths: list[Path]) -> list[tuple[Path, int, str]]:
    results = []
    for root in paths:
        files = [root] if root.is_file() else sorted(root.rglob("*.py"))
        for f in files:
            if any(part in {".venv", "venv", "site-packages", "tests"} for part in f.parts):
                continue
            try:
                tree = ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
            except (SyntaxError, UnicodeDecodeError) as e:
                print(f"skip {f}: {e}", file=sys.stderr)
                continue
            c = Checker()
            c.visit(tree)
            results += [(f, line, rule) for line, rule in sorted(c.found)]
    return results


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Find risky patterns in Python code")
    ap.add_argument("paths", nargs="+", type=Path)
    ap.add_argument("--min", choices=["low", "medium", "high"], default="low")
    a = ap.parse_args()
    order = {"low": 0, "medium": 1, "high": 2}
    hits = [h for h in scan(a.paths) if order[RULES[h[2]][0]] >= order[a.min]]
    for f, line, rule in hits:
        sev, what, fix = RULES[rule]
        print(f"{f}:{line}: [{sev.upper():<6}] {rule} {what}\n    fix: {fix}")
    counts = {s: sum(RULES[r][0] == s for _, _, r in hits) for s in ("high", "medium", "low")}
    print(f"\n{len(hits)} findings: {counts['high']} high, {counts['medium']} medium, {counts['low']} low")
    sys.exit(1 if counts["high"] else 0)          # fail CI builds on high-severity findings
