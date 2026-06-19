import httpx
from datetime import datetime, timezone, timedelta


WECHAT_TOKEN_URL = "https://api.weixin.qq.com/cgi-bin/stable_token"
WECHAT_SEND_URL = "https://api.weixin.qq.com/cgi-bin/message/template/send"

_BEIJING_TZ = timezone(timedelta(hours=8))


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
    base_url: str | None,
    title: str,
    content: str,
) -> dict:
    now = datetime.now(_BEIJING_TZ)
    date_str = now.strftime("%Y-%m-%d %H:%M:%S")

    from urllib.parse import quote
    encoded_message = quote(content)
    encoded_date = quote(date_str)
    encoded_title = quote(title)

    separator = "&" if base_url and "?" in base_url else "?"
    jump_url = f"{base_url or ''}{separator}message={encoded_message}&date={encoded_date}&title={encoded_title}"

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
