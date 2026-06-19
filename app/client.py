"""HTTP client for sending messages to the wxpush relay server."""
import logging

import httpx

logger = logging.getLogger(__name__)

_MAX_RETRIES = 3
_TIMEOUT = 15.0


async def send_wxsend(
    url: str,
    token: str,
    title: str,
    content: str,
    shortid: str | None = None,
    userid: str | None = None,
) -> dict:
    """Send a message via /wxsend with retry (up to 3 attempts, 15 s timeout each).

    Raises the last httpx exception if all attempts fail.
    """
    endpoint = url.rstrip("/") + "/wxsend"
    payload: dict = {"title": title, "content": content, "token": token}
    if shortid:
        payload["shortid"] = shortid
    if userid:
        payload["userid"] = userid

    last_exc: Exception | None = None
    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        for attempt in range(1, _MAX_RETRIES + 1):
            try:
                resp = await client.post(endpoint, json=payload)
                return resp.json()
            except (httpx.TimeoutException, httpx.NetworkError) as exc:
                last_exc = exc
                if attempt < _MAX_RETRIES:
                    logger.warning("Attempt %d/%d failed (%s), retrying…", attempt, _MAX_RETRIES, exc)
                else:
                    logger.error("All %d attempts failed. Last error: %s", _MAX_RETRIES, exc)

    raise last_exc  # type: ignore[misc]
