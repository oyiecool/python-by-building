class Server:
    """A server we monitor."""

    def __init__(self, hostname: str, ip: str, cores: int = 4):
        self.hostname = hostname      # instance attributes
        self.ip = ip
        self.cores = cores
        self.online = False

    def start(self):
        self.online = True
        print(f"{self.hostname} started")

    def describe(self) -> str:
        state = "online" if self.online else "offline"
        return f"{self.hostname} ({self.ip}), {self.cores} cores, {state}"

web = Server("web01", "10.0.0.11", cores=8)
db = Server("db01", "10.0.0.21")
web.start()
print(web.describe())
print(db.describe())
