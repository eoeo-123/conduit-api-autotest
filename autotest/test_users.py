import uuid
import requests

BASE_URL = "http://127.0.0.1:8899"

def _register(email, username=None, password="abcd1234"):
    """小工具函数：注册的代码只写一遍，多个用例复用（和 fixture 的思想一样）"""
    suffix = uuid.uuid4().hex[:8]
    return requests.post(f"{BASE_URL}/api/users", json={
        "user": {
            "username": username or f"auto_{suffix}",
            "email": email,
            "password": password,
        }
    })

def test_duplicate_email_rejected():
    # 业务冲突：同一邮箱注册两次，第二次必须拒绝
    email = f"{uuid.uuid4().hex[:8]}@test.com"
    r1 = _register(email)
    r2 = _register(email)
    assert r1.status_code == 200
    assert r2.status_code == 400

def test_register_missing_password():
    # 必填缺失：不传 password，预期 422
    suffix = uuid.uuid4().hex[:8]
    r = requests.post(f"{BASE_URL}/api/users", json={
        "user": {"username": f"auto_{suffix}", "email": f"{suffix}@test.com"}
    })
    assert r.status_code == 422

def test_login_wrong_password():
    email = f"{uuid.uuid4().hex[:8]}@test.com"
    _register(email)
    r = requests.post(f"{BASE_URL}/api/users/login", json={
        "user": {"email": email, "password": "wrongpass99"}
    })
    assert r.status_code in (400, 401, 403)