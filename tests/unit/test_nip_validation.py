import pytest
from unittest.mock import patch, Mock
from src.company_account import CompanyAccount


class TestNipValidation:
    @patch('src.company_account.requests.get')
    def test_valid_nip_czynny_status_creates_account(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": {
                "subject": {
                    "statusVat": "Czynny",
                    "name": "Test Company"
                }
            }
        }
        mock_get.return_value = mock_response
        
        account = CompanyAccount("Test Company", "8461627563")
        
        assert account.nip == "8461627563"
        assert account.company_name == "Test Company"

    @patch('src.company_account.requests.get')
    def test_invalid_nip_not_in_gov_raises_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": {
                "subject": None
            }
        }
        mock_get.return_value = mock_response
        
        with pytest.raises(ValueError) as excinfo:
            CompanyAccount("Fake Company", "1234567890")
        
        assert str(excinfo.value) == "Company not registered!!"

    @patch('src.company_account.requests.get')
    def test_nip_with_nieczynny_status_raises_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": {
                "subject": {
                    "statusVat": "Nieczynny",
                    "name": "Inactive Company"
                }
            }
        }
        mock_get.return_value = mock_response
        
        with pytest.raises(ValueError) as excinfo:
            CompanyAccount("Inactive Company", "1234567890")
        
        assert str(excinfo.value) == "Company not registered!!"

    @patch('src.company_account.requests.get')
    def test_nip_zwolniony_status_raises_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": {
                "subject": {
                    "statusVat": "Zwolniony",
                    "name": "Exempt Company"
                }
            }
        }
        mock_get.return_value = mock_response
        
        with pytest.raises(ValueError) as excinfo:
            CompanyAccount("Exempt Company", "1234567890")
        
        assert str(excinfo.value) == "Company not registered!!"

    def test_nip_too_short_creates_account_without_validation(self):
        account = CompanyAccount("Short NIP Company", "123456789")
        
        assert account.nip == "Invalid"
        assert account.company_name == "Short NIP Company"

    def test_nip_too_long_creates_account_without_validation(self):
        account = CompanyAccount("Long NIP Company", "12345678901")
        
        assert account.nip == "Invalid"
        assert account.company_name == "Long NIP Company"

    @patch('src.company_account.requests.get')
    def test_api_error_returns_false(self, mock_get):
        mock_get.side_effect = Exception("Connection error")
        
        with pytest.raises(ValueError) as excinfo:
            CompanyAccount("Error Company", "1234567890")
        
        assert str(excinfo.value) == "Company not registered!!"

    @patch('src.company_account.requests.get')
    def test_api_non_200_status_raises_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"error": "Not found"}
        mock_get.return_value = mock_response
        
        with pytest.raises(ValueError) as excinfo:
            CompanyAccount("Not Found Company", "1234567890")
        
        assert str(excinfo.value) == "Company not registered!!"

    @patch('src.company_account.requests.get')
    def test_validate_nip_method_returns_true_for_czynny(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": {
                "subject": {
                    "statusVat": "Czynny"
                }
            }
        }
        mock_get.return_value = mock_response
        
        result = CompanyAccount.validate_nip_in_gov("8461627563")
        
        assert result is True

    @patch('src.company_account.requests.get')
    def test_validate_nip_method_returns_false_for_null_subject(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": {
                "subject": None
            }
        }
        mock_get.return_value = mock_response
        
        result = CompanyAccount.validate_nip_in_gov("0000000000")
        
        assert result is False
