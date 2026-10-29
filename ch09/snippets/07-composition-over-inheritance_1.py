class Bank:
    def __init__(self, name):
        self.name = name
        self.accounts: dict[str, BankAccount] = {}

    def open(self, account: BankAccount):
        self.accounts[account.owner] = account

    def total_deposits(self) -> float:
        return sum(a.balance for a in self.accounts.values())
