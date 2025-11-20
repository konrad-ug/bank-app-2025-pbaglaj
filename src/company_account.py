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

    def submit_for_loan(self, amount: int):
        if self._has_two_times_larger_balance(amount) and self._has_zus_transfer():
            self.balance += amount
            return True
        return False

    def _has_zus_transfer(self):
        zus_transfer = -1775.0
        return zus_transfer in self.history
    
    def _has_two_times_larger_balance(self, amount: int):
        return self.balance >= 2 * amount