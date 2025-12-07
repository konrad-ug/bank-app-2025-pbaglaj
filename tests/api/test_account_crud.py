import pytest
import requests
import random

BASE_URL = "http://localhost:5000/api/accounts"

class TestAccountCRUD:
    @pytest.fixture
    def random_pesel(self):
        return str(random.randint(10000000000, 99999999999))
    
    @pytest.fixture
    def created_account(self, random_pesel):
        pesel = random_pesel
        payload = {
            "name": "Test",
            "surname": "User",
            "pesel": pesel
        }
        requests.post(BASE_URL, json=payload)
    
        yield pesel
        
        requests.delete(f"{BASE_URL}/{pesel}")

    # --- TESTY ---

    def test_create_account(self, random_pesel):
        payload = {
            "name": "Jan",
            "surname": "Kowalski",
            "pesel": random_pesel
        }
        response = requests.post(BASE_URL, json=payload)
        
        assert response.status_code == 201
        assert response.json() == {"message": "Account created"}
        
        check = requests.get(f"{BASE_URL}/{random_pesel}")
        assert check.status_code == 200

    @pytest.mark.parametrize("test_data", [
        {"name": "Alice", "surname": "Smith", "pesel": "44051401359"},
        {"name": "Bob", "surname": "Johnson", "pesel": "02070803628"},
        {"name": "Charlie", "surname": "Brown", "pesel": "83010412345"},
    ])
    def test_get_account_by_pesel(self, test_data):
        requests.post(BASE_URL, json=test_data)
        response = requests.get(f"{BASE_URL}/{test_data['pesel']}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["pesel"] == test_data["pesel"]
        assert data["name"] == test_data["name"]
        assert data["surname"] == test_data["surname"]
        requests.delete(f"{BASE_URL}/{test_data['pesel']}")

    def test_get_account_not_found(self):
        non_existent_pesel = "00000000000"
        response = requests.get(f"{BASE_URL}/{non_existent_pesel}")
        
        assert response.status_code == 404
        assert response.json() == {"error": "Account not found"}

    def test_update_account(self, created_account):
        pesel = created_account
        new_surname = "Zmieniony"
        
        response = requests.patch(f"{BASE_URL}/{pesel}", json={"surname": new_surname})
        
        assert response.status_code == 200
        assert response.json() == {"message": "Account updated"}
        
        check = requests.get(f"{BASE_URL}/{pesel}")
        assert check.json()["surname"] == new_surname
        assert check.json()["name"] == "Test"

    def test_delete_account(self, random_pesel):
        requests.post(BASE_URL, json={
            "name": "To", "surname": "Delete", "pesel": random_pesel
        })
        
        response = requests.delete(f"{BASE_URL}/{random_pesel}")
        
        assert response.status_code == 200
        assert response.json() == {"message": "Account deleted"}
        
        check = requests.get(f"{BASE_URL}/{random_pesel}")
        assert check.status_code == 404

    def test_create_account_with_existing_pesel(self, created_account):
        pesel = created_account
        payload = {
            "name": "Duplicate",
            "surname": "User",
            "pesel": pesel
        }
        response = requests.post(BASE_URL, json=payload)
        
        assert response.status_code == 409