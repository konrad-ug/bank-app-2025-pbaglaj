from src.personal_account import PersonalAccount
import pytest

class TestLoans:

    @pytest.fixture()
    def account(self):
        account = PersonalAccount("John", "Doe", "1234567890")
        return account
    
    def test_3_positive_transfers(self, account):
        account.history=[100, 200, 500]
        result = account.submit_for_loan(300)
        assert result
        assert account.balance == 300

    def test_second_law_for_loan(self, account):
        account.history = [100, 100, 100, -50, -1, 100, 100]
        result = account.submit_for_loan(100)
        assert result
        assert account.balance == 100

    def test_loan_returns_true(self, account):
        account.incoming_transfer(100.0)
        account.incoming_transfer(100.0)
        account.incoming_transfer(100.0)
        assert account.submit_for_loan(400) is True

    def test_loan_returns_false(self, account):
        account.incoming_transfer(100.0)
        account.incoming_transfer(100.0)
        account.outgoing_transfer(100.0)
        assert account.submit_for_loan(300) is False


