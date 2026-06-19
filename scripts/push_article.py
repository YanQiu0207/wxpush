#!/usr/bin/env python3
"""Push a markdown article via the wxsend endpoint."""

# ── 配置区，按需修改 ────────────────────────────────────────────
WXSEND_URL = "https://wxpush.teslajuju.com"
API_TOKEN  = "tesla"
SHORTID    = "tesla"   # config.toml [users] 中定义的 shortid
# ───────────────────────────────────────────────────────────────

import re
import sys
from pathlib import Path

import httpx


def extract_title(content: str, filename: str) -> str:
    # YAML frontmatter: title: ...
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            frontmatter = content[3:end]
            m = re.search(r"^title:\s*['\"]?(.+?)['\"]?\s*$", frontmatter, re.MULTILINE)
            if m:
                return m.group(1).strip()
    # First H1 heading
    m = re.search(r"^#\s+(.+)", content, re.MULTILINE)
    if m:
        return m.group(1).strip()
    # Fallback to filename stem
    return Path(filename).stem


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python push_article.py <file.md>", file=sys.stderr)
        sys.exit(1)

    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"Error: file not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    content = file_path.read_text(encoding="utf-8")
    title = extract_title(content, file_path.name)

    endpoint = WXSEND_URL.rstrip("/") + "/wxsend"
    payload = {"title": title, "content": content, "token": API_TOKEN, "shortid": SHORTID}

    print(f"Pushing \"{title}\" → {endpoint}")
    resp = httpx.post(endpoint, json=payload)
    msg = resp.json().get("msg", resp.text) if resp.headers.get("content-type", "").startswith("application/json") else resp.text
    print(msg)

    if resp.status_code != 200:
        sys.exit(1)


if __name__ == "__main__":
    main()
