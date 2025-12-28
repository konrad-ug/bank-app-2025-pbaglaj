from src.company_account import CompanyAccount
from unittest.mock import patch, Mock
import pytest


@pytest.fixture()
def account():
    with patch('src.company_account.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": {"subject": {"statusVat": "Czynny"}}}
        mock_get.return_value = mock_response
        return CompanyAccount('Gillette', '9581153134')

@pytest.fixture
def zus_amount():
    return -1775.0

class TestCompanyLoans:
    @pytest.mark.parametrize("balance, loan, expected_result", [
        (2000.0, 1000.0, True),
        (1500.0, 1000.0, False),
        (1999.99, 1000.0, False),
    ])
    def test_is_loan_amount_valid_logic(self, account, balance, loan, expected_result):
        account.balance = balance
        assert (account.balance >= 2 * loan) is expected_result

    @pytest.mark.parametrize("initial_balance, has_zus, expected_final_balance", [
        (5000.0, True, 7000.0),  
        (3000.0, True, 3000.0),  
        (5000.0, False, 5000.0), 
    ])
    def test_submit_for_loan_scenarios(self, account, zus_amount, initial_balance, has_zus, expected_final_balance):
        loan_request = 2000.0
        account.balance = initial_balance
        
        base_history = [1000.0, -500.0]
        if has_zus:
            base_history.append(zus_amount)
        
        account.history = base_history
        
        account.submit_for_loan(loan_request)
        
        assert account.balance == expected_final_balance

class TestCompanyLoansWithZus:
    def test_at_least_one_transfer_to_zus(self, account, zus_amount):
        account.history = [500.0, -200.0, -300.0, -150.0, zus_amount]
        zus_transfers = [amount for amount in account.history if amount == zus_amount]
        assert len(zus_transfers) == 1
    
    def test_no_transfer_to_zus(self, account, zus_amount):
        account.history = [500.0, -200.0, -300.0, -150.0]
        zus_transfers = [amount for amount in account.history if amount == zus_amount]
        assert len(zus_transfers) == 0
