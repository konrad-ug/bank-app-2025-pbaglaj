import pytest
import requests

BASE_URL = "http://localhost:5000/api/accounts"

class TestApiTransfers:
    @pytest.fixture
    def account_pesel(self):
        pesel = "12345678901"
        requests.post(BASE_URL, json={
            "name": "Test",
            "surname": "Transfer",
            "pesel": pesel
        })
        yield pesel

        requests.delete(f"{BASE_URL}/{pesel}")

    def test_incoming_transfer(self, account_pesel):
        response = requests.post(f"{BASE_URL}/{account_pesel}/transfer", json={
            "amount": 100,
            "type": "incoming"
        })
        assert response.status_code == 200
        assert response.json() == {"message": "Zlecenie przyjęto do realizacji"}
        
        acc = requests.get(f"{BASE_URL}/{account_pesel}").json()
        assert acc["balance"] == 100

    def test_outgoing_transfer_success(self, account_pesel):
        requests.post(f"{BASE_URL}/{account_pesel}/transfer", json={
            "amount": 200,
            "type": "incoming"
        })
        
        response = requests.post(f"{BASE_URL}/{account_pesel}/transfer", json={
            "amount": 100,
            "type": "outgoing"
        })
        assert response.status_code == 200
        
        acc = requests.get(f"{BASE_URL}/{account_pesel}").json()
        assert acc["balance"] == 100

    def test_outgoing_transfer_failure(self, account_pesel):
        response = requests.post(f"{BASE_URL}/{account_pesel}/transfer", json={
            "amount": 100,
            "type": "outgoing"
        })
        assert response.status_code == 422
        
        acc = requests.get(f"{BASE_URL}/{account_pesel}").json()
        assert acc["balance"] == 0

    def test_express_transfer_success(self, account_pesel):
        requests.post(f"{BASE_URL}/{account_pesel}/transfer", json={
            "amount": 200,
            "type": "incoming"
        })
        
        response = requests.post(f"{BASE_URL}/{account_pesel}/transfer", json={
            "amount": 100,
            "type": "express"
        })
        assert response.status_code == 200
        
        acc = requests.get(f"{BASE_URL}/{account_pesel}").json()
        assert acc["balance"] == 99

    def test_express_transfer_failure(self, account_pesel):
        response = requests.post(f"{BASE_URL}/{account_pesel}/transfer", json={
            "amount": 100,
            "type": "express"
        })
        assert response.status_code == 422

    def test_account_not_found(self):
        response = requests.post(f"{BASE_URL}/00000000000/transfer", json={
            "amount": 100,
            "type": "incoming"
        })
        assert response.status_code == 404

    def test_invalid_transfer_type(self, account_pesel):
        response = requests.post(f"{BASE_URL}/{account_pesel}/transfer", json={
            "amount": 100,
            "type": "unknown"
        })
        assert response.status_code == 400
