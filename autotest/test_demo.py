import requests
import uuid

BASE_URL="http://127.0.0.1:8899"

def test_get_tags():
    r=requests.get(f"{BASE_URL}/api/tags")
    assert r.status_code==200
    assert "tags" in r.json()

def test_register_success():
    suffix = uuid.uuid4().hex[:8]
    payload={
        "user":{
        "username":f"auto_{suffix}",
        "email":f"auto_{suffix}@test.com",
        "password":"abcd1234"
        }
    }
    r=requests.post(f"{BASE_URL}/api/users",json=payload)
    assert r.status_code==200
    assert "token" in r.json()["user"]