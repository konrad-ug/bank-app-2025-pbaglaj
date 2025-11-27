import pytest
import requests
import random

BASE_URL = "http://localhost:5000/api/accounts"

@pytest.fixture
def random_pesel():
    return str(random.randint(10000000000, 99999999999))

@pytest.fixture
def created_account(random_pesel):
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

def test_create_account(random_pesel):
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

def test_get_account_by_pesel(created_account):
    pesel = created_account
    
    response = requests.get(f"{BASE_URL}/{pesel}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["pesel"] == pesel
    assert data["name"] == "Test"
    assert data["surname"] == "User"

def test_get_account_not_found():
    non_existent_pesel = "00000000000"
    response = requests.get(f"{BASE_URL}/{non_existent_pesel}")
    
    assert response.status_code == 404
    assert response.json() == {"error": "Account not found"}

def test_update_account(created_account):
    pesel = created_account
    new_surname = "Zmieniony"
    
    response = requests.patch(f"{BASE_URL}/{pesel}", json={"surname": new_surname})
    
    assert response.status_code == 200
    assert response.json() == {"message": "Account updated"}
    
    check = requests.get(f"{BASE_URL}/{pesel}")
    assert check.json()["surname"] == new_surname
    assert check.json()["name"] == "Test"

def test_delete_account(random_pesel):
    requests.post(BASE_URL, json={
        "name": "To", "surname": "Delete", "pesel": random_pesel
    })
    
    response = requests.delete(f"{BASE_URL}/{random_pesel}")
    
    assert response.status_code == 200
    assert response.json() == {"message": "Account deleted"}
    
    check = requests.get(f"{BASE_URL}/{random_pesel}")
    assert check.status_code == 404