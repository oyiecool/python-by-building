def read_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("That is not a number, try again.")

def load_config(path):
    try:
        f = open(path, encoding="utf-8")
    except FileNotFoundError:
        print(f"{path} missing, using defaults")
        return {}
    except PermissionError as e:
        print(f"Cannot read {path}: {e}")
        return {}
    else:                      # runs only if no exception
        with f:
            return dict(line.strip().split("=", 1) for line in f if "=" in line)
    finally:                   # always runs
        print("config check done")
