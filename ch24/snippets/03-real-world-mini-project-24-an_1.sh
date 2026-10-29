$ python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
$ pip install -e ".[dev]"
$ pytest -q
.....                                                   [100%]
5 passed in 0.02s
$ passgen --version
passgen 1.0.0
$ passgen -l 20 -c 2
CRfU?4T&ckB-mOfcrFr0
k5e2tBwcke-ms3dYyn=M
# about 125 bits of entropy each
$ passgen --words 5
bamboo-saddle-fennel-canyon-island
# about 27 bits of entropy each
