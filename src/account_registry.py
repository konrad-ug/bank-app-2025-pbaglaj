from src.personal_account import PersonalAccount

class AccountRegistry:
    def __init__(self):
        self.accounts = []

    def add_account(self, account: PersonalAccount):
        self.accounts.append(account)

    def find_account_by_pesel(self, pesel: str) -> PersonalAccount | None:
        for account in self.accounts:
            if account.pesel == pesel:
                return account
        return None
    
    def return_all_accounts(self) -> list[PersonalAccount]:
        return self.accounts
    
    def return_amount_of_accounts(self) -> int:
        return len(self.accounts)
    
    def remove_account(self, account: PersonalAccount):
        if account in self.accounts:
            self.accounts.remove(account)
        