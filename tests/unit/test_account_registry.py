from src.personal_account import PersonalAccount
from src.personal_account import AccountRegistry
import pytest

class TestAccountRegistry:

    @pytest.fixture()
    def account(self):
        personalAccount = PersonalAccount("John", "Doe", "04310511001")
        return personalAccount
    
    @pytest.fixture()
    def account_registry(self):
        return AccountRegistry()
    
    @pytest.fixture()
    def account_registry_with_account(self, account_registry, account):
        account_registry.add_account(account)
        return account_registry
    
    def test_register_account(self, account_registry, account):
        account_registry.add_account(account)
        assert len(account_registry.accounts) == 1

    def test_find_account_by_pesel(self, account_registry_with_account, account):
        assert account_registry_with_account.find_account_by_pesel(account.pesel) == account

    def test_return_2_accounts_with_return_all_accounts(self, account_registry_with_account, account):
        account_registry_with_account.add_account(account)
        all_accounts = account_registry_with_account.return_all_accounts()
        assert len(all_accounts) == 2

    def test_return_amount_of_accounts(self, account_registry_with_account, account):
        amount_of_accounts = account_registry_with_account.return_amount_of_accounts()
        assert amount_of_accounts == 1