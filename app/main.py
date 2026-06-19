import os
import asyncio
from typing import Optional

from fastapi import FastAPI, Request, Header
from fastapi.responses import HTMLResponse, JSONResponse
from dotenv import load_dotenv

from app.wx_api import get_stable_token, send_message
from app.html_pages import HOMEPAGE_HTML, MACOS_HACKER_HTML, SKIN_HTML, test_page_html

load_dotenv()

app = FastAPI(docs_url=None, redoc_url=None)

API_TOKEN = os.environ.get("API_TOKEN", "")
WX_APPID = os.environ.get("WX_APPID", "")
WX_SECRET = os.environ.get("WX_SECRET", "")
WX_USERID = os.environ.get("WX_USERID", "")
WX_TEMPLATE_ID = os.environ.get("WX_TEMPLATE_ID", "")
WX_BASE_URL = os.environ.get("WX_BASE_URL", "")


async def _parse_params(request: Request) -> dict:
    """Merge URL query params and request body into one dict (body wins on conflict)."""
    url_params = dict(request.query_params)
    body_params: dict = {}

    if request.method in ("POST", "PUT", "PATCH"):
        content_type = request.headers.get("content-type", "").lower()
        try:
            if "application/json" in content_type:
                raw = await request.json()
                if isinstance(raw, str):
                    body_params = {"content": raw}
                elif isinstance(raw, dict):
                    if isinstance(raw.get("params"), dict):
                        body_params = raw["params"]
                    elif isinstance(raw.get("data"), dict):
                        body_params = raw["data"]
                    else:
                        body_params = raw
            elif "application/x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type:
                form = await request.form()
                body_params = dict(form)
            else:
                text = (await request.body()).decode("utf-8", errors="replace")
                if text:
                    import json
                    try:
                        parsed = json.loads(text)
                        if isinstance(parsed, dict):
                            if isinstance(parsed.get("params"), dict):
                                body_params = parsed["params"]
                            elif isinstance(parsed.get("data"), dict):
                                body_params = parsed["data"]
                            else:
                                body_params = parsed
                        else:
                            body_params = {"content": text}
                    except json.JSONDecodeError:
                        body_params = {"content": text}
        except Exception:
            pass

    return {**url_params, **body_params}


def _extract_token(params: dict, authorization: Optional[str]) -> Optional[str]:
    token = params.get("token")
    if not token and authorization:
        parts = authorization.split()
        if len(parts) == 2 and parts[0].lower() == "bearer":
            token = parts[1]
        else:
            token = authorization
    return token


@app.get("/", response_class=HTMLResponse)
@app.get("/index.html", response_class=HTMLResponse)
async def homepage():
    return HOMEPAGE_HTML


@app.get("/skin", response_class=HTMLResponse)
@app.get("/skin/quiet-night-sky", response_class=HTMLResponse)
async def skin():
    return SKIN_HTML


@app.get("/skin/macos-hacker", response_class=HTMLResponse)
async def skin_macos_hacker():
    return MACOS_HACKER_HTML


@app.api_route("/wxsend", methods=["GET", "POST", "PUT", "PATCH"])
async def wxsend(request: Request, authorization: Optional[str] = Header(default=None)):
    params = await _parse_params(request)

    content = params.get("content")
    title = params.get("title")
    request_token = _extract_token(params, authorization)

    if not content or not title or not request_token:
        return JSONResponse({"msg": "Missing required parameters: content, title, token"}, status_code=400)

    if request_token != API_TOKEN:
        return JSONResponse({"msg": "Invalid token"}, status_code=403)

    appid = params.get("appid") or WX_APPID
    secret = params.get("secret") or WX_SECRET
    userid_str = params.get("userid") or WX_USERID
    template_id = params.get("template_id") or WX_TEMPLATE_ID
    base_url = params.get("base_url") or WX_BASE_URL

    if not all([appid, secret, userid_str, template_id]):
        return JSONResponse(
            {"msg": "Missing required environment variables: WX_APPID, WX_SECRET, WX_USERID, WX_TEMPLATE_ID"},
            status_code=500,
        )

    user_list = [u.strip() for u in userid_str.split("|") if u.strip()]

    try:
        access_token = await get_stable_token(appid, secret)
        if not access_token:
            return JSONResponse({"msg": "Failed to get access token"}, status_code=500)

        results = await asyncio.gather(
            *[send_message(access_token, uid, template_id, base_url, title, content) for uid in user_list]
        )

        successful = [r for r in results if r.get("errmsg") == "ok"]
        if successful:
            return JSONResponse({"msg": f"Successfully sent messages to {len(successful)} user(s). First response: ok"})
        else:
            first_error = results[0].get("errmsg", "Unknown error") if results else "Unknown error"
            return JSONResponse({"msg": f"Failed to send messages. First error: {first_error}"}, status_code=500)

    except Exception as e:
        return JSONResponse({"msg": f"An error occurred: {e}"}, status_code=500)


@app.get("/{token}", response_class=HTMLResponse)
async def token_test_page(token: str):
    if token != API_TOKEN:
        return JSONResponse({"msg": "Invalid token"}, status_code=403)
    return test_page_html(token)
