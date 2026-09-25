import pytest
import requests

BASE_URL = "http://127.0.0.1:8899"

def test_create_article_ok(auth_headers):
    payload = {
        "article": {
            "title": "自动化测试文章",
            "description": "这是自动化创建的文章描述",
            "body": "这是自动化测试的正文内容，长度足够。",
            "tagList": ["auto"],
        }
    }
    r = requests.post(f"{BASE_URL}/api/articles", json=payload, headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["article"]["title"] == "自动化测试文章"

def test_create_article_without_token():
    payload = {
        "article": {
            "title": "无鉴权文章",
            "description": "这是未登录用户的文章描述",
            "body": "这是正文内容，长度足够通过校验。",
            "tagList": [],
        }
    }
    r = requests.post(f"{BASE_URL}/api/articles", json=payload)
    assert r.status_code == 403

@pytest.mark.parametrize("limit,expected", [(0, 422), (-1, 422), ("abc", 422), (99999, 200)])
def test_article_list_limit(limit, expected):
    r = requests.get(f"{BASE_URL}/api/articles", params={"limit": limit})
    assert r.status_code == expected
@pytest.mark.parametrize("desc,expected", [
    ("一二三四五六七八九十", 200),   # 恰好 10 字符
    ("一二三四五六七八九", 422),     # 9 字符
])
def test_article_desc_length(auth_headers, desc, expected):
    payload = {
        "article": {
            "title": f"长度测试-{desc}",
            "description": desc,
            "body": "这是长度边界测试的正文内容，长度足够通过校验。",
            "tagList": [],
        }
    }
    r = requests.post(f"{BASE_URL}/api/articles", json=payload, headers=auth_headers)
    assert r.status_code == expected