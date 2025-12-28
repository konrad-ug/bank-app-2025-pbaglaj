import unittest
from unittest.mock import patch, Mock
from datetime import date
from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount


class TestPersonalAccountSendHistoryEmail(unittest.TestCase):
    def setUp(self):
        self.account = PersonalAccount("Jan", "Kowalski", "12345678901")
        self.account.history = [100, -1, 500]
    
    @patch("src.personal_account.SMTPClient")
    def test_send_history_email_success(self, mock_smtp_class):
        mock_smtp_instance = Mock()
        mock_smtp_instance.send.return_value = True
        mock_smtp_class.return_value = mock_smtp_instance
        
        result = self.account.send_history_via_email("test@example.com")
        
        self.assertTrue(result)
        mock_smtp_instance.send.assert_called_once()
        
        call_args = mock_smtp_instance.send.call_args
        today = date.today().strftime("%Y-%m-%d")
        expected_subject = f"Account Transfer History {today}"
        expected_text = "Personal account history: [100, -1, 500]"
        
        self.assertEqual(call_args[0][0], expected_subject)
        self.assertEqual(call_args[0][1], expected_text)
        self.assertEqual(call_args[0][2], "test@example.com")
    
    @patch("src.personal_account.SMTPClient")
    def test_send_history_email_failure(self, mock_smtp_class):
        mock_smtp_instance = Mock()
        mock_smtp_instance.send.return_value = False
        mock_smtp_class.return_value = mock_smtp_instance
        
        result = self.account.send_history_via_email("test@example.com")
        
        self.assertFalse(result)
        mock_smtp_instance.send.assert_called_once()
    
    @patch("src.personal_account.SMTPClient")
    def test_send_history_email_empty_history(self, mock_smtp_class):
        mock_smtp_instance = Mock()
        mock_smtp_instance.send.return_value = True
        mock_smtp_class.return_value = mock_smtp_instance
        
        self.account.history = []
        
        result = self.account.send_history_via_email("test@example.com")
        
        self.assertTrue(result)
        call_args = mock_smtp_instance.send.call_args
        expected_text = "Personal account history: []"
        self.assertEqual(call_args[0][1], expected_text)


class TestCompanyAccountSendHistoryEmail(unittest.TestCase):
    @patch("src.company_account.CompanyAccount.validate_nip_in_gov")
    def test_send_history_email_success(self, mock_validate_nip):
        mock_validate_nip.return_value = True
        account = CompanyAccount("Firma Test", "1234567890")
        account.history = [5000, -1000, 500]
        
        with patch("src.company_account.SMTPClient") as mock_smtp_class:
            mock_smtp_instance = Mock()
            mock_smtp_instance.send.return_value = True
            mock_smtp_class.return_value = mock_smtp_instance
            
            result = account.send_history_via_email("company@example.com")
            
            self.assertTrue(result)
            mock_smtp_instance.send.assert_called_once()
            
            call_args = mock_smtp_instance.send.call_args
            today = date.today().strftime("%Y-%m-%d")
            expected_subject = f"Account Transfer History {today}"
            expected_text = "Company account history: [5000, -1000, 500]"
            
            self.assertEqual(call_args[0][0], expected_subject)
            self.assertEqual(call_args[0][1], expected_text)
            self.assertEqual(call_args[0][2], "company@example.com")
    
    @patch("src.company_account.CompanyAccount.validate_nip_in_gov")
    def test_send_history_email_failure(self, mock_validate_nip):
        mock_validate_nip.return_value = True
        account = CompanyAccount("Firma Test", "1234567890")
        account.history = [5000, -1000, 500]
        
        with patch("src.company_account.SMTPClient") as mock_smtp_class:
            mock_smtp_instance = Mock()
            mock_smtp_instance.send.return_value = False
            mock_smtp_class.return_value = mock_smtp_instance
            
            result = account.send_history_via_email("company@example.com")
            
            self.assertFalse(result)
            mock_smtp_instance.send.assert_called_once()
    
    @patch("src.company_account.CompanyAccount.validate_nip_in_gov")
    def test_send_history_email_empty_history(self, mock_validate_nip):
        mock_validate_nip.return_value = True
        account = CompanyAccount("Firma Test", "1234567890")
        account.history = []
        
        with patch("src.company_account.SMTPClient") as mock_smtp_class:
            mock_smtp_instance = Mock()
            mock_smtp_instance.send.return_value = True
            mock_smtp_class.return_value = mock_smtp_instance
            
            result = account.send_history_via_email("company@example.com")
            
            self.assertTrue(result)
            call_args = mock_smtp_instance.send.call_args
            expected_text = "Company account history: []"
            self.assertEqual(call_args[0][1], expected_text)
    
    @patch("src.company_account.CompanyAccount.validate_nip_in_gov")
    def test_send_history_email_correct_date_format(self, mock_validate_nip):
        mock_validate_nip.return_value = True
        account = CompanyAccount("Firma Test", "1234567890")
        
        with patch("src.company_account.SMTPClient") as mock_smtp_class:
            mock_smtp_instance = Mock()
            mock_smtp_instance.send.return_value = True
            mock_smtp_class.return_value = mock_smtp_instance
            
            account.send_history_via_email("test@example.com")
            
            call_args = mock_smtp_instance.send.call_args
            subject = call_args[0][0]
            
            self.assertTrue(subject.startswith("Account Transfer History "))
            date_part = subject.replace("Account Transfer History ", "")
            self.assertRegex(date_part, r"^\d{4}-\d{2}-\d{2}$")


if __name__ == "__main__":
    unittest.main()
