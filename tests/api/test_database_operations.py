import pytest
import requests

class TestPersistence:
    url = "http://127.0.0.1:5000/api/accounts"
    save_url = "http://127.0.0.1:5000/api/accounts/save"
    load_url = "http://127.0.0.1:5000/api/accounts/load"

    @pytest.fixture(autouse=True)
    def clean_up(self):
      requests.get(self.url) 
      yield

    def test_save_and_load_flow(self):
      pesel = "99999999999"
      requests.post(self.url, json={
          "name": "Test", "surname": "Persist", "pesel": pesel
      })

      res_save = requests.post(self.save_url)
      assert res_save.status_code == 200

      requests.delete(f"{self.url}/{pesel}")
      
      res_check = requests.get(f"{self.url}/{pesel}")
      assert res_check.status_code == 404

      res_load = requests.post(self.load_url)
      assert res_load.status_code == 200
      assert res_load.json()["count"] >= 1

      res_check_after = requests.get(f"{self.url}/{pesel}")
      assert res_check_after.status_code == 200
      assert res_check_after.json()['name'] == "Test"