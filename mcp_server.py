import os

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

WXPUSH_URL = os.environ.get("WXPUSH_URL", "").rstrip("/")
WXPUSH_TOKEN = os.environ.get("WXPUSH_TOKEN", "")

mcp = FastMCP("wxpush")


@mcp.tool()
async def send_wechat_message(title: str, content: str, shortid: str) -> str:
    """Send a WeChat message via the wxpush service.

    Args:
        title: Message title.
        content: Message body text.
        shortid: Recipient identifier defined in the server's config.toml [users] section.
    """
    if not WXPUSH_URL or not WXPUSH_TOKEN:
        return "Error: WXPUSH_URL and WXPUSH_TOKEN must be configured."

    payload = {"title": title, "content": content, "token": WXPUSH_TOKEN, "shortid": shortid}
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{WXPUSH_URL}/wxsend", json=payload)
    data = resp.json()
    return data.get("msg", "Unknown response")


if __name__ == "__main__":
    mcp.run()
