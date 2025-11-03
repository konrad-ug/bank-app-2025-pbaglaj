class Account:
    def __init__(self):
        self.balance = 0.0

    def incoming_transfer(self, amount: int):
        if amount > 0:
            self.balance += amount
    
    def outgoing_transfer(self, amount: int):
        if 0 < amount <= self.balance:
            self.balance -= amount