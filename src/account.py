class Account:
    def __init__(self):
        self.balance = 0.0
        self.history = []

    def incoming_transfer(self, amount: int):
        if amount > 0:
            self.balance += amount
            self.history.append(amount)  # zapis dodatni

    
    def outgoing_transfer(self, amount: int):
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.history.append(-amount)  # zapis ujemny

    def to_dict(self):
        return {
            "balance": self.balance,
            "history": self.history
        }
