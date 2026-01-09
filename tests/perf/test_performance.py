import pytest
import requests
import random

BASE_URL = "http://localhost:5000/api/accounts"
TIMEOUT = 0.5


class TestPerformance:
    def generate_random_pesel(self):
        return str(random.randint(10000000000, 99999999999))

    def test_create_and_delete_account_100_times(self):
        iterations = 100
        
        for i in range(iterations):
            pesel = self.generate_random_pesel()
            payload = {
                "name": f"PerfTest{i}",
                "surname": f"User{i}",
                "pesel": pesel
            }
            
            create_response = requests.post(
                BASE_URL, 
                json=payload, 
                timeout=TIMEOUT
            )
            assert create_response.status_code == 201, \
                f"Iteracja {i}: Błąd tworzenia konta - status {create_response.status_code}"
            
            delete_response = requests.delete(
                f"{BASE_URL}/{pesel}", 
                timeout=TIMEOUT
            )
            assert delete_response.status_code == 200, \
                f"Iteracja {i}: Błąd usuwania konta - status {delete_response.status_code}"

    def test_100_incoming_transfers(self):
        pesel = self.generate_random_pesel()
        transfer_amount = 50
        iterations = 100
        expected_balance = transfer_amount * iterations
        
        payload = {
            "name": "TransferPerf",
            "surname": "Test",
            "pesel": pesel
        }
        create_response = requests.post(BASE_URL, json=payload, timeout=TIMEOUT)
        assert create_response.status_code == 201, \
            f"Błąd tworzenia konta - status {create_response.status_code}"
        
        try:
            for i in range(iterations):
                transfer_response = requests.post(
                    f"{BASE_URL}/{pesel}/transfer",
                    json={
                        "amount": transfer_amount,
                        "type": "incoming"
                    },
                    timeout=TIMEOUT
                )
                assert transfer_response.status_code == 200, \
                    f"Iteracja {i}: Błąd przelewu - status {transfer_response.status_code}"
            
            account_response = requests.get(f"{BASE_URL}/{pesel}", timeout=TIMEOUT)
            assert account_response.status_code == 200
            
            account_data = account_response.json()
            assert account_data["balance"] == expected_balance, \
                f"Nieprawidłowe saldo: oczekiwano {expected_balance}, otrzymano {account_data['balance']}"
        
        finally:
            requests.delete(f"{BASE_URL}/{pesel}")

    # def test_create_1000_accounts_then_delete_all(self):
    #     iterations = 1000
    #     created_pesels = []
        
    #     for i in range(iterations):
    #         pesel = self.generate_random_pesel()
    #         payload = {
    #             "name": f"BulkTest{i}",
    #             "surname": f"User{i}",
    #             "pesel": pesel
    #         }
            
    #         create_response = requests.post(
    #             BASE_URL, 
    #             json=payload, 
    #             timeout=TIMEOUT
    #         )
    #         assert create_response.status_code == 201, \
    #             f"Iteracja {i}: Błąd tworzenia konta - status {create_response.status_code}"
            
    #         created_pesels.append(pesel)
        
    #     for i, pesel in enumerate(created_pesels):
    #         delete_response = requests.delete(
    #             f"{BASE_URL}/{pesel}", 
    #             timeout=TIMEOUT
    #         )
    #         assert delete_response.status_code == 200, \
    #             f"Iteracja {i}: Błąd usuwania konta - status {delete_response.status_code}"
