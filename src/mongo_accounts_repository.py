from pymongo import MongoClient
from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount
import os

class MongoAccountsRepository:
    def __init__(self):
      host = os.getenv('DB_HOST', 'localhost')
      username = os.getenv('DB_USER')
      password = os.getenv('DB_PASSWORD')
      port = int(os.getenv('DB_PORT', 27017))
      
      if username and password:
          self.client = MongoClient(f"mongodb://{username}:{password}@{host}:{port}/")
      else:
          self.client = MongoClient(f"mongodb://{host}:{port}/")
          
      self.db = self.client.bank_db
      self.collection = self.db.accounts

    def save_all(self, accounts):
      self.collection.delete_many({})
      
      if not accounts:
          return

      objects_to_save = [account.to_dict() for account in accounts]
      self.collection.insert_many(objects_to_save)

    def load_all(self):
      documents = list(self.collection.find())
      loaded_accounts = []

      for doc in documents:
          if doc.get("type") == "personal":
              acc = PersonalAccount(doc["first_name"], doc["last_name"], doc["pesel"])
          elif doc.get("type") == "company":
              acc = CompanyAccount(doc["company_name"], doc["nip"])
          else:
              continue 

          acc.balance = doc["balance"]
          acc.history = doc["history"]
          loaded_accounts.append(acc)
      
      return loaded_accounts