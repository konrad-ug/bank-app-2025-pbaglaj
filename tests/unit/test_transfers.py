from src.account import Account

class TestTransfers:
    def test_incoming_transfer(self):
        account = Account("John", "Doe", "04310511001")
        account.incoming_transfer(100.0)
        assert account.balance == 100

    def test_negative_incoming_transfer(self):
        account = Account("John", "Doe", "04310511001")
        account.incoming_transfer(-100.0)
        assert account.balance == 0.0

    def test_outgoing_transfer(self):
        account = Account("John", "Doe", "04310511001")
        account.balance = 200.0 # 1. Set up
        account.outgoing_transfer(50.0) # 2. Action
        assert account.balance == 150.0 # 3. Assertion

    def test_transfer_insufficient_funds(self):
        account = Account("John", "Doe", "04310511001")
        account.outgoing_transfer(30.0)
        assert account.balance == 0.0

    def test_transfer_negative_amount(self):
        account = Account("John", "Doe", "04310511001")
        account.outgoing_transfer(-30.0)
        assert account.balance == 0.0