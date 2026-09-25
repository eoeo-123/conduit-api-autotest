import pytest
import requests
import uuid

BASE_URL = "http://127.0.0.1:8899"

@pytest.fixture
def auth_headers():    
    suffix = uuid.uuid4().hex[:8]
    payload = {
        "user": {
            "username": f"auto_{suffix}",
            "email": f"auto_{suffix}@test.com",
            "password": "abcd1234",
        }
    }
    r = requests.post(f"{BASE_URL}/api/users", json=payload)
    token = r.json()["user"]["token"]
    return {"Authorization": f"Token {token}"}