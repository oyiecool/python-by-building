command = input("Command: ").strip().lower()
match command:
    case "start" | "run":
        print("Starting service")
    case "stop":
        print("Stopping service")
    case "status":
        print("Service is running")
    case _:
        print("Unknown command")
