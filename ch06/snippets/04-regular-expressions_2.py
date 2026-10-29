log = '192.168.1.20 - - [29/Oct/2026:10:42:01] "GET /index.html HTTP/1.1" 200 5123'
pattern = re.compile(
    r'(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] "(?P<method>\w+) (?P<path>\S+) [^"]*" (?P<status>\d{3}) (?P<size>\d+)'
)
m = pattern.match(log)
print(m["ip"], m["path"], m["status"], m.groupdict())
