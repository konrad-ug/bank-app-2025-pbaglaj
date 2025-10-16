from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", '04040414041')
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0
        assert len(account.pesel) == 11
