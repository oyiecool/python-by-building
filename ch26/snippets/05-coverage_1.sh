$ pytest -q --cov=syncbackup --cov=weather --cov-report=term-missing
.........                                                   [100%]
Name            Stmts   Miss  Cover   Missing
---------------------------------------------
syncbackup.py      88     14    84%   76-78, 101-112
weather.py          9      0   100%
---------------------------------------------
TOTAL              97     14    86%
9 passed in 0.20s
