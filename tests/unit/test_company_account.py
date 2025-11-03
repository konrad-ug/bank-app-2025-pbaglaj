from src.company_account import CompanyAccount

class TestCompanyAccount:
    def test_nip_too_short(self):
        account = CompanyAccount('Gillette', '958115313')
        assert account.nip == 'Invalid'

    def test_nip_too_long(self):
        account = CompanyAccount('Gillette', '95811531344')
        assert account.nip == 'Invalid'