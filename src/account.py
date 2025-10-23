class Account:
    def __init__(self, first_name, last_name, pesel, promo_code = None):
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
            century = 1900
            offset = 0
        elif 21 <= mm_code <= 32:
            century = 2000
            offset = 20
        elif 41 <= mm_code <= 52:
            century = 2100
            offset = 40
        elif 61 <= mm_code <= 72:
            century = 2200
            offset = 60
        elif 81 <= mm_code <= 92:
            century = 1800
            offset = 80
        else:
            return None

        month = mm_code - offset
        if not (1 <= month <= 12):
            return None

        year = century + rr
        return year
    
    def incoming_transfer(self, amount: int):
        if amount > 0:
            self.balance += amount
    
    def outgoing_transfer(self, amount: int):
        if self.balance - amount >= 0 and amount > 0:
            self.balance -= amount
    