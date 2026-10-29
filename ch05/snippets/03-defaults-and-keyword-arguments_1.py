def make_backup_name(filename, suffix="bak", stamp=True):
    from datetime import date
    if stamp:
        return f"{filename}.{date.today():%Y%m%d}.{suffix}"
    return f"{filename}.{suffix}"

print(make_backup_name("config.yml"))
print(make_backup_name("config.yml", "old"))
print(make_backup_name("config.yml", stamp=False))
