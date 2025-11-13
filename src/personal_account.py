from src.account import Account

class PersonalAccount(Account):
    def __init__(self, first_name, last_name, pesel, promo_code = None):
        super().__init__()  # <-- zaciągamy history i balance z Account
        self.first_name = first_name
        self.last_name = last_name
        self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"
        birth_year = self.birth_year_from_pesel(pesel)
        self.balance = 50 if self.is_promo_code_valid(promo_code) and birth_year is not None and birth_year > 1960 else 0.0


    def is_pesel_valid(self, pesel):
        return isinstance(pesel, str) and len(pesel) == 11
    
    def is_promo_code_valid(self, promo_code):
        return promo_code is not None and promo_code.startswith("PROM_") and len(promo_code) == 8
    
    # PESEL[0:2] → dwie ostatnie cyfry roku (RR)
    # PESEL[2:4] → zakodowany miesiąc (MM)
    # PESEL[4:6] → dzień (DD)

    # 01–12 → urodzeni w latach 1900–1999 
    # 21–32 → urodzeni w latach 2000–2099 
    # 41–52 → urodzeni w latach 2100–2199 
    # 61–72 → urodzeni w latach 2200–2299 
    # 81–92 → urodzeni w latach 1800–1899
    @staticmethod
    def birth_year_from_pesel(pesel: str) -> int | None:
        if not isinstance(pesel, str):
            return None
        pesel = pesel.strip()
        if len(pesel) != 11 or not pesel.isdigit():
            return None

        rr = int(pesel[0:2])
        mm_code = int(pesel[2:4])

        if 1 <= mm_code <= 12:
            return 1900 + rr
        elif 21 <= mm_code <= 32:
            return 2000 + rr
        elif 41 <= mm_code <= 52:
            return 2100 + rr
        elif 61 <= mm_code <= 72:
            return 2200 + rr
        elif 81 <= mm_code <= 92:
            return 1800 + rr
        else:
            return None
    
    def express_outgoing_transfer(self, amount: int):
        fee = 1
        if 0 < amount <= self.balance and self.balance - (fee + amount) >= -fee:
            self.balance -= (amount + fee)
            self.history.append(-amount)
            self.history.append(-fee)

    def submit_for_loan(self, amount: int):
        if self._has_good_recent_history() or self._has_strong_balance_history(amount):
            self.balance += amount
            return True
        return False


    def _has_good_recent_history(self) -> bool:
        """Sprawdza, czy 3 ostatnie transakcje są dodatnie."""
        return len(self.history) >= 3 and all(tx > 0 for tx in self.history[-3:])


    def _has_strong_balance_history(self, amount: int) -> bool:
        """Sprawdza, czy suma 5 ostatnich transakcji przekracza żądaną kwotę pożyczki."""
        return len(self.history) >= 5 and sum(self.history[-5:]) > amount

