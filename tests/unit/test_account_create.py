from src.personal_account import PersonalAccount
from src.account import Account
import pytest

class TestAccount:
    def test_account_creation(self):
        account = PersonalAccount("John", "Doe", "12345678901")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0
        assert account.pesel == "12345678901"
        
    @pytest.mark.parametrize("pesel", [
        "123456789011",  # too long
        "1234567890",    # too short
        "",              # empty
    ])
    def test_invalid_pesel(self, pesel):
        account = PersonalAccount("John", "Doe", pesel)
        assert account.pesel == 'Invalid'

    def test_correct_promo_code(self):
        account = PersonalAccount("John", "Doe", "00302012345", "PROM_123")
        assert account.balance == 50

    @pytest.mark.parametrize("promo_code", [
        "PROM_XYZZ",  # suffix too long
        "PROM_XY",    # suffix too short
        "PRO_XYZ",    # wrong prefix
    ])
    def test_invalid_promo_code(self, promo_code):
        account = PersonalAccount("John", "Doe", "12345678901", promo_code)
        assert account.balance == 0.0

    def test_pesel_after_1960(self):
        account = PersonalAccount("John", "Doe", "00302012345")
        year_of_birth = PersonalAccount.birth_year_from_pesel(account.pesel)
        assert year_of_birth > 1960

    def test_pesel_before_1960(self):
        account = PersonalAccount("John", "Doe", "44051401458")
        year_of_birth = PersonalAccount.birth_year_from_pesel(account.pesel)
        assert year_of_birth < 1960

    def test_valid_pesel_with_promo(self):
        acc = PersonalAccount("Jan", "Kowalski", "01210100000", "PROM_123")
        assert acc.balance == 50

    def test_invalid_pesel(self):
        acc = PersonalAccount("Jan", "Kowalski", "123", None)
        assert acc.pesel == "Invalid"
        assert acc.balance == 0

    def test_promo_code_invalid_no_bonus(self):
        acc = PersonalAccount("Jan", "Kowalski", "01210100000", "BAD")
        assert acc.balance == 0


    @pytest.mark.parametrize("pesel,expected_year", [
        ("99010100000", 1999),  # 1900s
        ("01210100000", 2001),  # 2000s
        ("01410100000", 2101),  # 2100s
        ("01610100000", 2201),  # 2200s
        ("01810100000", 1801),  # 1800s
    ])
    def test_birth_year_from_pesel(self, pesel, expected_year):
        assert PersonalAccount.birth_year_from_pesel(pesel) == expected_year

    def test_pesel_not_string(self):
        assert PersonalAccount.birth_year_from_pesel(12345678901) is None

    def test_birth_year_invalid(self):
        assert PersonalAccount.birth_year_from_pesel("99000000000") is None
        assert PersonalAccount.birth_year_from_pesel("bad") is None
    
    def test_invalid_month_range(self):
        assert PersonalAccount.birth_year_from_pesel("99130100000") is None