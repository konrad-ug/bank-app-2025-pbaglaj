from src.account import Account

class CompanyAccount(Account): # Dziedziczenie
    def __init__(self, company_name, nip):
        self.company_name = company_name
        self.nip = nip if len(nip) == 10 else "Invalid"
        self.balance = 0.0

    def express_outgoing_transfer(self, amount: int):
        if 0 < amount <= self.balance and self.balance - (5 + amount) > 0:
            self.balance -= (amount + 5)
