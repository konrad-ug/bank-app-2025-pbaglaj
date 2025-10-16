class Account:
    def __init__(self, first_name, last_name, pesel, promo_code = None):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 50 if self.is_promo_code_valid(promo_code) else 0.0
        self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"

    def is_pesel_valid(self, pesel):
        return isinstance(pesel, str) and len(pesel) == 11
    
    def is_promo_code_valid(self, promo_code):
        return promo_code is not None and promo_code.startswith("PROM_") and len(promo_code) == 8