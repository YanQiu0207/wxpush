import logging
import os
import time
import sqlite3
import secrets
import asyncio
import tomllib
from pathlib import Path
from contextlib import asynccontextmanager
from datetime import datetime, timezone, timedelta
from typing import Optional

from fastapi import FastAPI, Request, Header
from fastapi.responses import HTMLResponse, JSONResponse
from dotenv import load_dotenv

from app.wx_api import get_stable_token, send_message
from app.html_pages import HOMEPAGE_HTML, MACOS_HACKER_HTML, SKIN_HTML, test_page_html

load_dotenv()

logger = logging.getLogger(__name__)

API_TOKEN = os.environ.get("API_TOKEN", "")
WX_APPID = os.environ.get("WX_APPID", "")
WX_SECRET = os.environ.get("WX_SECRET", "")
WX_TEMPLATE_ID = os.environ.get("WX_TEMPLATE_ID", "")
WX_BASE_URL = os.environ.get("WX_BASE_URL", "")

_CONFIG_PATH = Path(__file__).parent.parent / "config.toml"


def _load_users() -> dict[str, str]:
    if not _CONFIG_PATH.exists():
        return {}
    with open(_CONFIG_PATH, "rb") as f:
        cfg = tomllib.load(f)
    return cfg.get("users", {})


USERS: dict[str, str] = _load_users()

DB_PATH = Path(__file__).parent.parent / "messages.db"
_BEIJING_TZ = timezone(timedelta(hours=8))
TTL_SECONDS = 7 * 24 * 3600


# --- SQLite helpers (sync, executed in thread pool) ---

def _init_db() -> None:
    con = sqlite3.connect(DB_PATH)
    con.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at REAL NOT NULL
        )
    """)
    con.execute("DELETE FROM messages WHERE created_at < ?", (time.time() - TTL_SECONDS,))
    con.commit()
    con.close()


def _store(msg_id: str, title: str, content: str) -> None:
    con = sqlite3.connect(DB_PATH)
    con.execute(
        "INSERT INTO messages (id, title, content, created_at) VALUES (?, ?, ?, ?)",
        (msg_id, title, content, time.time()),
    )
    con.commit()
    con.close()


def _fetch(msg_id: str) -> dict | None:
    con = sqlite3.connect(DB_PATH)
    cur = con.execute(
        "SELECT title, content, created_at FROM messages WHERE id = ?", (msg_id,)
    )
    row = cur.fetchone()
    con.close()
    return {"title": row[0], "content": row[1], "created_at": row[2]} if row else None


# --- App ---

@asynccontextmanager
async def lifespan(app: FastAPI):
    await asyncio.to_thread(_init_db)
    yield


app = FastAPI(docs_url=None, redoc_url=None, lifespan=lifespan)


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


@app.get("/api/content/{msg_id}")
async def api_content(msg_id: str):
    msg = await asyncio.to_thread(_fetch, msg_id)
    if not msg:
        logger.info("content not found msg_id=%s", msg_id)
        return JSONResponse({"msg": "Not found"}, status_code=404)
    logger.info("content fetched msg_id=%s", msg_id)
    dt = datetime.fromtimestamp(msg["created_at"], tz=_BEIJING_TZ)
    return JSONResponse({
        "title": msg["title"],
        "content": msg["content"],
        "date": dt.strftime("%Y-%m-%d %H:%M:%S"),
    })


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
    template_id = params.get("template_id") or WX_TEMPLATE_ID
    base_url = params.get("base_url") or WX_BASE_URL

    shortid = params.get("shortid")
    if shortid:
        userid_str = USERS.get(shortid)
        if not userid_str:
            return JSONResponse({"msg": f"Unknown shortid: {shortid!r}"}, status_code=400)
    else:
        userid_str = params.get("userid")

    if not all([appid, secret, userid_str, template_id]):
        return JSONResponse(
            {"msg": "Missing required config: WX_APPID, WX_SECRET, WX_TEMPLATE_ID, and shortid or userid"},
            status_code=500,
        )

    msg_id = secrets.token_urlsafe(6)
    await asyncio.to_thread(_store, msg_id, title, content)
    logger.info("stored msg_id=%s title=%r", msg_id, title)

    separator = "&" if base_url and "?" in base_url else "?"
    jump_url = f"{base_url or ''}{separator}id={msg_id}"

    user_list = [u.strip() for u in userid_str.split("|") if u.strip()]

    try:
        access_token = await get_stable_token(appid, secret)
        if not access_token:
            return JSONResponse({"msg": "Failed to get access token"}, status_code=500)

        results = await asyncio.gather(
            *[send_message(access_token, uid, template_id, jump_url, title, content) for uid in user_list]
        )

        successful = [r for r in results if r.get("errmsg") == "ok"]
        if successful:
            logger.info("wx push ok msg_id=%s users=%d/%d", msg_id, len(successful), len(user_list))
            return JSONResponse({"msg": f"Successfully sent messages to {len(successful)} user(s). First response: ok"})
        else:
            first_error = results[0].get("errmsg", "Unknown error") if results else "Unknown error"
            logger.warning("wx push failed msg_id=%s error=%r", msg_id, first_error)
            return JSONResponse({"msg": f"Failed to send messages. First error: {first_error}"}, status_code=500)

    except Exception as e:
        logger.exception("wx push exception msg_id=%s", msg_id)
        return JSONResponse({"msg": f"An error occurred: {e}"}, status_code=500)


@app.get("/{token}", response_class=HTMLResponse)
async def token_test_page(token: str):
    if token != API_TOKEN:
        return JSONResponse({"msg": "Invalid token"}, status_code=403)
    return test_page_html(token)
