import base64
import requests
from urllib.parse import urlencode


AUTH_URL = "https://dida365.com/oauth/authorize"
TOKEN_URL = "https://dida365.com/oauth/token"


def build_authorize_url(client_id, redirect_uri, scope="tasks:read tasks:write", state="demo_state"):
    """
    第一步：生成用户授权链接
    用户访问这个链接并同意授权后，Dida365 会重定向到 redirect_uri?code=xxx&state=xxx
    """
    params = {
        "client_id": client_id,
        "scope": scope,
        "state": state,
        "redirect_uri": redirect_uri,
        "response_type": "code",
    }
    return f"{AUTH_URL}?{urlencode(params)}"


def exchange_code_for_token(client_id, client_secret, code, redirect_uri, scope="tasks:read tasks:write"):
    """
    第三步：用 code 换 access_token
    Dida365 文档要求：
    - POST https://dida365.com/oauth/token
    - Content-Type: application/x-www-form-urlencoded
    - client_id / client_secret 放在 Basic Auth 头里
    """
    basic_auth = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("utf-8")

    headers = {
        "Authorization": f"Basic {basic_auth}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "code": code,
        "grant_type": "authorization_code",
        "scope": scope,
        "redirect_uri": redirect_uri,
    }

    response = requests.post(TOKEN_URL, headers=headers, data=data, timeout=20)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    CLIENT_ID = "your_client_id"
    CLIENT_SECRET = "your_client_secret"
    # remember to register redirect_url in the https://developer.dida365.com/manage->Your App->OAuth redirect URL 
    REDIRECT_URI = "http://localhost:8080/callback"
    SCOPE = "tasks:read tasks:write"

    # 1. 先生成授权链接
    auth_link = build_authorize_url(
        client_id=CLIENT_ID,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        state="abc123"
    )
    print("请先在浏览器打开这个链接进行授权：")
    print(auth_link)
    print()

    # 2. 用户授权后，Dida365 会跳转到 redirect_uri，并带上 ?code=xxxx
    code = input("请输入回调得到的 code: ").strip()

    # 3. 用 code 换 access_token
    token_data = exchange_code_for_token(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        code=code,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    )

    print("获取 token 成功：")
    print(token_data)

    access_token = token_data.get("access_token")
    if access_token:
        print("\naccess_token =", access_token)