class SavingsAccount(BankAccount):
    def __init__(self, owner, balance=0, rate=0.025):
        super().__init__(owner, balance)
        self.rate = rate

    def add_interest(self):
        self.deposit(round(self._balance * self.rate / 12, 2))

class CheckingAccount(BankAccount):
    def __init__(self, owner, balance=0, overdraft=5000):
        super().__init__(owner, balance)
        self.overdraft = overdraft

    def withdraw(self, amount):             # override
        if amount > self._balance + self.overdraft:
            raise ValueError("overdraft limit exceeded")
        self._balance -= amount
        self._history.append(("withdraw", amount))

accounts = [SavingsAccount("Ana", 10000), CheckingAccount("Ben", 200)]
for a in accounts:
    a.withdraw(1000)          # same call, different behaviour: polymorphism
    print(type(a).__name__, a.owner, a.balance)
