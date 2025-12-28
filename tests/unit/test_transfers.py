from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount
from unittest.mock import patch, Mock
import pytest

class TestTransfers:

    @pytest.fixture()
    def personalAccount(self):
        personalAccount = PersonalAccount("John", "Doe", "04310511001")
        return personalAccount


    def test_incoming_transfer(self, personalAccount):
        personalAccount.incoming_transfer(100.0)
        assert personalAccount.balance == 100

    def test_negative_incoming_transfer(self):
        account = PersonalAccount("John", "Doe", "04310511001")
        account.incoming_transfer(-100.0)
        assert account.balance == 0.0

    def test_outgoing_transfer(self):
        account = PersonalAccount("John", "Doe", "04310511001")
        account.balance = 200.0 # 1. Set up
        account.outgoing_transfer(50.0) # 2. Action
        assert account.balance == 150.0 # 3. Assertion

    def test_transfer_insufficient_funds(self):
        account = PersonalAccount("John", "Doe", "04310511001")
        account.outgoing_transfer(30.0)
        assert account.balance == 0.0

    def test_transfer_negative_amount(self):
        account = PersonalAccount("John", "Doe", "04310511001")
        account.outgoing_transfer(-30.0)
        assert account.balance == 0.0

    def test_express_personal_transfer(self):
        account = PersonalAccount("John", "Doe", "04310511001")
        account.balance = 200.0
        account.express_outgoing_transfer(50.0)
        assert account.balance == 149.0

    @patch('src.company_account.requests.get')
    def test_express_company_transfer(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": {"subject": {"statusVat": "Czynny"}}}
        mock_get.return_value = mock_response
        
        account = CompanyAccount("Gillette", "9581153134")
        account.balance = 200.0
        account.express_outgoing_transfer(50.0)
        assert account.balance == 145.0