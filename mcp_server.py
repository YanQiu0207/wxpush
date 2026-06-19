import os
import re

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from app.client import send_wxsend

load_dotenv()

WXPUSH_URL = os.environ.get("WXPUSH_URL", "").rstrip("/")
WXPUSH_TOKEN = os.environ.get("WXPUSH_TOKEN", "")

mcp = FastMCP("wxpush")

_LOCAL_PATH_RE = re.compile(r'!?\[.*?\]\((?!https?://)([^)]+)\)')


@mcp.tool()
async def send_wechat_message(title: str, content: str, shortid: str) -> str:
    """Send a WeChat message via the wxpush service.

    Args:
        title: Message title.
        content: Message body (Markdown supported). All images and links MUST use
                 publicly accessible URLs (http/https). Local file paths are not
                 supported — upload assets to a CDN or image host before calling.
        shortid: Recipient identifier defined in the server's config.toml [users] section.
    """
    if not WXPUSH_URL or not WXPUSH_TOKEN:
        return "Error: WXPUSH_URL and WXPUSH_TOKEN must be configured."

    if _LOCAL_PATH_RE.search(content):
        return "Error: content contains local file paths. Upload all images and documents to a publicly accessible URL before sending."

    try:
        data = await send_wxsend(WXPUSH_URL, WXPUSH_TOKEN, title, content, shortid=shortid)
    except (httpx.TimeoutException, httpx.NetworkError) as exc:
        return f"Error: {exc}"
    return data.get("msg", "Unknown response")


if __name__ == "__main__":
    mcp.run()
