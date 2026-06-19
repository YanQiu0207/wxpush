import httpx


WECHAT_TOKEN_URL = "https://api.weixin.qq.com/cgi-bin/stable_token"
WECHAT_SEND_URL = "https://api.weixin.qq.com/cgi-bin/message/template/send"


async def get_stable_token(appid: str, secret: str) -> str | None:
    payload = {
        "grant_type": "client_credential",
        "appid": appid,
        "secret": secret,
        "force_refresh": False,
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(WECHAT_TOKEN_URL, json=payload)
        data = resp.json()
    return data.get("access_token")


async def send_message(
    access_token: str,
    userid: str,
    template_id: str,
    jump_url: str,
    title: str,
    content: str,
) -> dict:
    payload = {
        "touser": userid,
        "template_id": template_id,
        "url": jump_url,
        "data": {
            "title": {"value": title},
            "content": {"value": content},
        },
    }

    url = f"{WECHAT_SEND_URL}?access_token={access_token}"
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload)
    return resp.json()
