from src.account import Account

class CompanyAccount(Account): # Dziedziczenie
    def __init__(self, company_name, nip):
        self.company_name = company_name
        self.nip = nip if len(nip) == 10 else "Invalid"
        self.balance = 0.0