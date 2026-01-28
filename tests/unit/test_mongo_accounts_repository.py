import unittest
from unittest.mock import MagicMock, patch
from src.mongo_accounts_repository import MongoAccountsRepository
from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount
import os

class TestMongoAccountsRepository(unittest.TestCase):
    
    @patch('src.mongo_accounts_repository.MongoClient')
    def setUp(self, mock_client):
        self.mock_client = mock_client
        self.repo = MongoAccountsRepository()
        self.mock_collection = self.repo.collection

    def test_save_all(self):
        account = PersonalAccount("Jan", "Kowalski", "12345678901")
        accounts = [account]

        self.repo.save_all(accounts)

        self.mock_collection.delete_many.assert_called_once_with({})
        self.mock_collection.insert_many.assert_called_once()
        
    def test_load_all(self):
        mock_data = [{
            "type": "personal",
            "first_name": "Jan",
            "last_name": "Kowalski",
            "pesel": "12345678901",
            "balance": 100.0,
            "history": [100.0]
        }]
        self.mock_collection.find.return_value = mock_data

        loaded_accounts = self.repo.load_all()

        self.assertEqual(len(loaded_accounts), 1)
        self.assertIsInstance(loaded_accounts[0], PersonalAccount)
        self.assertEqual(loaded_accounts[0].balance, 100.0)

    @patch.dict(os.environ, {"DB_USER": "admin", "DB_PASSWORD": "admin"})
    @patch('src.mongo_accounts_repository.MongoClient')
    def test_init_with_auth(self, mock_client_class):
        _ = MongoAccountsRepository()
        expected_uri = "mongodb://admin:admin@localhost:27017/"
        mock_client_class.assert_called_with(expected_uri)

    def test_save_all_empty(self):
        self.repo.save_all([])
        self.mock_collection.delete_many.assert_called_once_with({})
        self.mock_collection.insert_many.assert_not_called()

    @patch('src.company_account.CompanyAccount.validate_nip_in_gov', return_value=True)
    def test_load_all_company_and_unknown(self, mock_validate_nip_in_gov):
        mock_data = [
            {
                "type": "company",
                "company_name": "Januszex",
                "nip": "8461627563",
                "balance": 5000.0,
                "history": [1000.0]
            },
            {
                "type": "alien_account",
                "balance": 0.0
            }
        ]
        self.mock_collection.find.return_value = mock_data

        loaded_accounts = self.repo.load_all()

        self.assertEqual(len(loaded_accounts), 1)
        
        acc = loaded_accounts[0]
        self.assertIsInstance(acc, CompanyAccount)
        self.assertEqual(acc.company_name, "Januszex")
        self.assertEqual(acc.balance, 5000.0)