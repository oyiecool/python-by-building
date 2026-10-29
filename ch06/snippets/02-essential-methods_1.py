line = "  2026-10-29  ERROR   disk   full  "
parts = line.split()          # ['2026-10-29', 'ERROR', 'disk', 'full']
date, level, *message = parts
print(level, " ".join(message))
