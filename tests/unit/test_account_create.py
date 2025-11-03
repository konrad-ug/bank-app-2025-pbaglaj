from src.account import Account

class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "12345678901")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0
        assert account.pesel == "12345678901"
        
    def test_pesel_too_long(self):
        account = Account("John", "Doe", "123456789011")
        assert account.pesel == 'Invalid'

    def test_pesel_too_short(self):
        account = Account("John", "Doe", "1234567890")
        assert account.pesel == 'Invalid'

    def test_pesel_none(self):
        account = Account("John", "Doe", "")
        assert account.pesel == 'Invalid'

    def test_correct_promo_code(self):
        account = Account("John", "Doe", "00302012345", "PROM_123")
        assert account.balance == 50

    def test_promo_code_suffix_too_long(self):
        account = Account("John", "Doe", "12345678901", "PROM_XYZZ")
        assert account.balance == 0.0

    def test_promo_code_suffix_too_short(self):
        account = Account("John", "Doe", "12345678901", "PROM_XY")
        assert account.balance == 0.0

    def test_wrong_promo_code_prefix(self):
        account = Account("John", "Doe", "12345678901", "PRO_XYZ")
        assert account.balance == 0.0

    def test_pesel_after_1960(self):
        account = Account("John", "Doe", "00302012345")
        year_of_birth = Account.birth_year_from_pesel(account.pesel)
        assert year_of_birth > 1960

    def test_pesel_before_1960(self):
        account = Account("John", "Doe", "44051401458")
        year_of_birth = Account.birth_year_from_pesel(account.pesel)
        assert year_of_birth < 1960

    def test_valid_pesel_with_promo(self):
        acc = Account("Jan", "Kowalski", "01210100000", "PROM_123")
        assert acc.balance == 50

    def test_invalid_pesel(self):
        acc = Account("Jan", "Kowalski", "123", None)
        assert acc.pesel == "Invalid"
        assert acc.balance == 0

    def test_promo_code_invalid_no_bonus(self):
        acc = Account("Jan", "Kowalski", "01210100000", "BAD")
        assert acc.balance == 0


    def test_birth_year_1900s(self):
        assert Account.birth_year_from_pesel("99010100000") == 1999

    def test_birth_year_2000s(self):
        assert Account.birth_year_from_pesel("01210100000") == 2001

    def test_birth_year_2100s(self):
        assert Account.birth_year_from_pesel("01410100000") == 2101

    def test_birth_year_2200s(self):
        assert Account.birth_year_from_pesel("01610100000") == 2201

    def test_birth_year_1800s(self):
        assert Account.birth_year_from_pesel("01810100000") == 1801

    def test_pesel_not_string(self):
        assert Account.birth_year_from_pesel(12345678901) is None

    def test_birth_year_invalid(self):
        assert Account.birth_year_from_pesel("99000000000") is None
        assert Account.birth_year_from_pesel("bad") is None
    
    def test_invalid_month_range(self):
        assert Account.birth_year_from_pesel("99130100000") is None

