import os
import requests
from datetime import date
from src.account import Account
from smtp.smtp import SMTPClient

class CompanyAccount(Account): # Dziedziczenie
    def __init__(self, company_name, nip):
        super().__init__()  # <-- zaciągamy history i balance z Account
        self.company_name = company_name
        
        if len(nip) != 10:
            self.nip = "Invalid"
        else:
            if not self.validate_nip_in_gov(nip):
                raise ValueError("Company not registered!!")
            self.nip = nip

    @staticmethod
    def validate_nip_in_gov(nip):
        base_url = os.getenv("BANK_APP_MF_URL", "https://wl-test.mf.gov.pl")
        today = date.today().strftime("%Y-%m-%d")
        url = f"{base_url}/api/search/nip/{nip}?date={today}"
        
        try:
            response = requests.get(url)
            response_json = response.json()
            print(f"MF API Response for NIP {nip}: {response_json}")
            
            if response.status_code == 200:
                subject = response_json.get("result", {}).get("subject")
                if subject and subject.get("statusVat") == "Czynny":
                    return True
            return False
        except Exception as e:
            print(f"Error validating NIP {nip}: {e}")
            return False

    def express_outgoing_transfer(self, amount: int):
        fee = 5
        if 0 < amount <= self.balance and self.balance - (fee + amount) >= -fee:
            self.balance -= (amount + fee)
            self.history.append(-amount)  # operacja główna
            self.history.append(-fee)    # oddzielna opłata

    def submit_for_loan(self, amount: int):
        if self._has_two_times_larger_balance(amount) and self._has_zus_transfer():
            self.balance += amount
            return True
        return False

    def _has_zus_transfer(self):
        zus_transfer = -1775.0
        return zus_transfer in self.history
    
    def _has_two_times_larger_balance(self, amount: int):
        return self.balance >= 2 * amount

    def send_history_via_email(self, email_address: str) -> bool:
        today = date.today().strftime("%Y-%m-%d")
        subject = f"Account Transfer History {today}"
        text = f"Company account history: {self.history}"
        smtp_client = SMTPClient()
        return smtp_client.send(subject, text, email_address)