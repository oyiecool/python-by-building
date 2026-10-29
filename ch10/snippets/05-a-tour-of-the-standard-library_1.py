from datetime import datetime, date, timedelta
now = datetime.now()
print(now.strftime("%A %d %B %Y, %H:%M"))      # Thursday 29 October 2026, 10:42
d = datetime.strptime("2026-12-25", "%Y-%m-%d")
print((d - now).days, "days to Christmas")
print(date.today() + timedelta(weeks=2))
