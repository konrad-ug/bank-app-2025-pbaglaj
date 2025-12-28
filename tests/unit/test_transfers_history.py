from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount
from src.account import Account
from unittest.mock import patch, Mock

class TestTransfersHistory:
    def test_history_starts_empty(self):
        acc = Account()
        assert acc.history == []

    def test_incoming_transfer_adds_positive_history_item(self):
        acc = Account()
        acc.incoming_transfer(200)
        assert acc.history == [200]


    def test_outgoing_transfer_adds_negative_history_item(self):
        acc = Account()
        acc.incoming_transfer(300)  # ensure enough balance
        acc.outgoing_transfer(100)
        assert acc.history == [300, -100]


    @patch('src.company_account.requests.get')
    def test_company_express_transfer_records_fee_separately(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": {"subject": {"statusVat": "Czynny"}}}
        mock_get.return_value = mock_response
        
        comp = CompanyAccount("Test SA", "1234567890")
        comp.incoming_transfer(500)
        comp.express_outgoing_transfer(300)
        # fee = -5 must be recorded separately
        assert comp.history == [500, -300, -5]


    def test_outgoing_transfer_blocked_if_insufficient_funds(self):
        acc = Account()
        acc.outgoing_transfer(100)
        # No history because transfer blocked
        assert acc.history == []


    @patch('src.company_account.requests.get')
    def test_express_transfer_blocked_if_insufficient_funds(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": {"subject": {"statusVat": "Czynny"}}}
        mock_get.return_value = mock_response
        
        comp = CompanyAccount("Test SA", "1234567890")
        comp.express_outgoing_transfer(500)  # No balance
        assert comp.history == []