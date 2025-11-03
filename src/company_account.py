from src.account import Account

class CompanyAccount(Account): # Dziedziczenie
    def __init__(self, company_name, nip):
        super().__init__()  # <-- zaciągamy history i balance z Account
        self.company_name = company_name
        self.nip = nip if len(nip) == 10 else "Invalid"

    def express_outgoing_transfer(self, amount: int):
        fee = 5
        if 0 < amount <= self.balance and self.balance - (fee + amount) >= -fee:
            self.balance -= (amount + fee)
            self.history.append(-amount)  # operacja główna
            self.history.append(-fee)    # oddzielna opłata