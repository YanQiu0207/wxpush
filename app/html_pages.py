"""Inline HTML pages, ported from the original Cloudflare Worker / VPS skins."""

HOMEPAGE_HTML = """\
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <title>WXPush — 微信消息推送服务</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700&display=swap" rel="stylesheet">
    <style>
      body {
        font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        display: flex; align-items: center; justify-content: center;
        min-height: 100vh; margin: 0;
        background: linear-gradient(170deg, #f3e8ff 0%, #ffffff 100%);
        color: #1f2937;
      }
      .card {
        background: rgba(255,255,255,0.85); backdrop-filter: blur(10px);
        border-radius: 24px; box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.18); padding: 40px;
        max-width: 720px; width: 90%; text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
      }
      .card:hover { transform: translateY(-8px); box-shadow: 0 16px 40px rgba(0,0,0,0.12); }
      h1 {
        margin: 0 0 12px; font-size: 32px; font-weight: 700;
        background: linear-gradient(90deg, #8b5cf6, #3b82f6);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
      }
      p { color: #4b5563; margin: 0; font-size: 16px; line-height: 1.6; }
    </style>
  </head>
  <body>
    <div class="card">
      <h1>WXPush</h1>
      <p>一个极简、可靠的微信消息推送服务，通过简单的 Webhook 请求，即可向微信用户发送模板消息。</p>
    </div>
  </body>
</html>"""


SKIN_HTML = """\
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>消息推送</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif; }
        body {
            background: linear-gradient(135deg, #0c0c2e 0%, #1a1a3e 100%);
            color: #e0f7fa; min-height: 100vh;
            display: flex; justify-content: center; align-items: center;
            padding: 20px; overflow-x: hidden; position: relative;
        }
        body::before {
            content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: radial-gradient(circle at 20% 30%, rgba(0,150,136,0.15) 0%, transparent 50%),
                        radial-gradient(circle at 80% 70%, rgba(0,188,212,0.15) 0%, transparent 50%);
            z-index: -1;
        }
        .container {
            max-width: 800px; width: 100%;
            background: rgba(18,18,40,0.85); backdrop-filter: blur(10px);
            border-radius: 16px; padding: 40px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5), 0 0 0 1px rgba(0,150,136,0.2), 0 0 20px rgba(0,188,212,0.3);
            position: relative; overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .container:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.6), 0 0 0 1px rgba(0,150,136,0.4), 0 0 30px rgba(0,188,212,0.5);
        }
        .container::before {
            content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 4px;
            background: linear-gradient(90deg, #00bcd4, #009688);
        }
        .title {
            text-align: center; margin-bottom: 40px; font-size: 2.2rem;
            font-weight: 300; letter-spacing: 2px; color: #00bcd4;
            position: relative; padding-bottom: 15px;
        }
        .title::after {
            content: ''; position: absolute; bottom: 0; left: 50%;
            transform: translateX(-50%); width: 100px; height: 2px;
            background: linear-gradient(90deg, transparent, #00bcd4, transparent);
        }
        .info-card {
            background: rgba(30,30,60,0.7); border-radius: 12px; padding: 25px;
            margin-bottom: 25px; border-left: 4px solid #00bcd4;
            transition: all 0.3s ease; box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .info-card:hover { transform: translateX(5px); background: rgba(40,40,70,0.8); box-shadow: 0 8px 20px rgba(0,0,0,0.3); }
        .info-label { font-size: 1.3rem; color: #80deea; margin-bottom: 10px; display: flex; align-items: center; }
        .info-label::before {
            content: ''; display: inline-block; width: 8px; height: 8px;
            border-radius: 50%; background: #00bcd4; margin-right: 10px;
        }
        .info-content { font-size: 1.2rem; color: #e0f7fa; font-weight: 500; word-break: break-word; line-height: 1.6; white-space: pre-line; }
        .pulse { animation: pulse 2s infinite; }
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(0,188,212,0.4); }
            70% { box-shadow: 0 0 0 10px rgba(0,188,212,0); }
            100% { box-shadow: 0 0 0 0 rgba(0,188,212,0); }
        }
        .info-content h1,.info-content h2,.info-content h3,.info-content h4,.info-content h5,.info-content h6 { color: #00bcd4; margin-top: 1em; margin-bottom: 0.5em; font-weight: 400; }
        .info-content p { margin-bottom: 1em; line-height: 1.6; }
        .info-content strong { color: #e0f7fa; font-weight: 600; }
        .info-content em { color: #80deea; font-style: italic; }
        .info-content code { background: rgba(0,0,0,0.3); color: #00bcd4; padding: 2px 4px; border-radius: 4px; font-family: 'Courier New', monospace; }
        .info-content pre { background: rgba(0,0,0,0.4); color: #e0f7fa; padding: 1em; border-radius: 8px; overflow-x: auto; margin-bottom: 1em; }
        .info-content blockquote { border-left: 4px solid #009688; margin: 1em 0; padding-left: 1em; color: #80deea; font-style: italic; }
        .info-content ul,.info-content ol { margin-bottom: 1em; padding-left: 2em; }
        .info-content li { margin-bottom: 0.5em; }
        .info-content a { color: #00bcd4; text-decoration: none; }
        .info-content a:hover { text-decoration: underline; }
        .info-content table { width: 100%; border-collapse: collapse; margin-bottom: 1em; background: rgba(0,0,0,0.2); border-radius: 8px; overflow: hidden; }
        .info-content th,.info-content td { padding: 0.75em; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.1); }
        .info-content th { background: rgba(0,188,212,0.2); color: #00bcd4; }
        @media (max-width: 768px) { .container { padding: 25px; } .title { font-size: 1.9rem; } .info-content { font-size: 1.1rem; } .info-label { font-size: 1.2rem; } }
        @media (max-width: 480px) { .container { padding: 20px; } .title { font-size: 1.6rem; } .info-content { font-size: 1rem; } .info-card { padding: 20px; } .info-label { font-size: 1.1rem; } }
        .particles { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; overflow: hidden; }
        .particle { position: absolute; background: rgba(0,188,212,0.3); border-radius: 50%; animation: float 15s infinite linear; }
        @keyframes float {
            0% { transform: translateY(0) translateX(0); opacity: 0; }
            10% { opacity: 1; } 90% { opacity: 1; }
            100% { transform: translateY(-100vh) translateX(100px); opacity: 0; }
        }
    </style>
</head>
<body>
    <div class="particles" id="particles"></div>
    <div class="container pulse">
        <div class="title" id="title">消息推送</div>
        <div class="info-card">
            <div class="info-label">通知内容</div>
            <div class="info-content" id="message">无告警信息</div>
        </div>
        <div class="info-card">
            <div class="info-label">时间</div>
            <div class="info-content" id="date">无时间信息</div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/marked/lib/marked.umd.js"></script>
    <script>
        function getUrlParams() {
            const p = new URLSearchParams(window.location.search);
            return { title: p.get('title') || '消息推送', message: p.get('message') || '无告警信息', date: p.get('date') || '无时间信息' };
        }
        function createParticles() {
            const c = document.getElementById('particles');
            const colors = ['rgba(0,188,212,0.2)', 'rgba(0,150,136,0.2)', 'rgba(77,182,172,0.15)'];
            for (let i = 0; i < 25; i++) {
                const el = document.createElement('div'); el.classList.add('particle');
                const size = Math.random() * 3 + 1; el.style.width = el.style.height = size + 'px';
                el.style.background = colors[Math.floor(Math.random() * colors.length)];
                el.style.left = (Math.random() * 100) + '%'; el.style.top = (Math.random() * 100) + '%';
                el.style.animationDelay = (Math.random() * 20) + 's'; el.style.animationDuration = (20 + Math.random() * 15) + 's';
                c.appendChild(el);
            }
        }
        function fillContent() {
            const params = getUrlParams();
            document.getElementById('title').textContent = params.title;
            const msgEl = document.getElementById('message');
            msgEl.textContent = params.message;
            if (typeof marked !== 'undefined') msgEl.innerHTML = marked.parse(msgEl.textContent);
            document.getElementById('date').textContent = params.date;
        }
        window.onload = function() { createParticles(); fillContent(); };
    </script>
</body>
</html>"""


MACOS_HACKER_HTML = """\
<!DOCTYPE html>
<html lang="zh-CN" dir="ltr">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>消息推送</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: "Courier New", monospace;
            background: #000; color: #00ff00; min-height: 100vh;
            overflow-x: hidden; position: relative;
            display: flex; justify-content: center; align-items: center;
        }
        .matrix-bg { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #000; z-index: -1; }
        .matrix-text { position: fixed; top: 20px; right: 20px; color: #00ff00; font-family: "Courier New", monospace; font-size: 0.8rem; opacity: 0.6; }
        .terminal {
            width: 90%; max-width: 800px; height: 500px;
            background: rgba(0, 0, 0, 0.9); border: 2px solid #00ff00;
            border-radius: 8px; box-shadow: 0 0 30px rgba(0, 255, 0, 0.5);
            position: relative; z-index: 1; overflow: hidden;
        }
        .terminal-header {
            background: rgba(0, 20, 0, 0.8); padding: 10px 15px;
            border-bottom: 1px solid #00ff00; display: flex; align-items: center;
        }
        .terminal-buttons { display: flex; gap: 8px; }
        .terminal-button { width: 12px; height: 12px; border-radius: 50%; background: #ff5f57; border: none; }
        .terminal-button:nth-child(2) { background: #ffbd2e; }
        .terminal-button:nth-child(3) { background: #28ca42; }
        .terminal-title { margin-left: 15px; color: #00ff00; font-size: 14px; font-weight: bold; }
        .terminal-body { padding: 20px; height: calc(100% - 50px); overflow-y: auto; font-size: 14px; line-height: 1.4; }
        .info-card {
            background: rgba(0, 30, 30, 0.85); border-radius: 12px; padding: 25px;
            margin-bottom: 25px; border-left: 4px solid #00ff00;
            transition: all 0.3s ease; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }
        .info-card:hover { transform: translateX(5px); background: rgba(0, 128, 0, 0.9); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3); }
        .info-label { font-size: 1.3rem; color: #80deea; margin-bottom: 10px; display: flex; align-items: center; }
        .info-label::before { content: ''; display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #00bcd4; margin-right: 10px; }
        .info-content { font-size: 1.2rem; color: #e0f7fa; font-weight: 500; word-break: break-word; line-height: 1.6; }
        .info-content h1,.info-content h2,.info-content h3 { color: #00ff00; margin-top: 1em; margin-bottom: 0.5em; }
        .info-content p { margin-bottom: 1em; line-height: 1.6; }
        .info-content code { background: rgba(0, 255, 0, 0.1); color: #00ff00; padding: 2px 4px; border-radius: 4px; font-family: "Courier New", monospace; }
        .info-content pre { background: rgba(0, 0, 0, 0.6); color: #00ff00; padding: 1em; border-radius: 8px; overflow-x: auto; margin-bottom: 1em; }
        .info-content blockquote { border-left: 4px solid #00aa00; margin: 1em 0; padding-left: 1em; color: #00cc00; }
        .info-content ul,.info-content ol { margin-bottom: 1em; padding-left: 2em; }
        .info-content li { margin-bottom: 0.5em; }
        .info-content a { color: #00ff00; }
        @media (max-width: 768px) { .terminal { width: 100%; max-width: 100%; height: auto; } }
    </style>
</head>
<body>
    <div class="matrix-bg"></div>
    <div class="matrix-text">WeiXin</div>
    <div class="terminal">
        <div class="terminal-header">
            <div class="terminal-buttons">
                <div class="terminal-button"></div>
                <div class="terminal-button"></div>
                <div class="terminal-button"></div>
            </div>
            <div class="terminal-title" id="title">消息推送</div>
        </div>
        <div class="terminal-body">
            <div class="info-card">
                <div class="info-label">通知内容</div>
                <div class="info-content" id="message">无告警信息</div>
            </div>
            <div class="info-card">
                <div class="info-label">时间</div>
                <div class="info-content" id="date">无时间信息</div>
            </div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/marked/lib/marked.umd.js"></script>
    <script>
        function getUrlParams() {
            const p = new URLSearchParams(window.location.search);
            return { title: p.get('title') || '消息推送', message: p.get('message') || '无告警信息', date: p.get('date') || '无时间信息' };
        }
        function fillContent() {
            const params = getUrlParams();
            document.getElementById('title').textContent = params.title;
            const msgEl = document.getElementById('message');
            msgEl.textContent = params.message;
            if (typeof marked !== 'undefined') msgEl.innerHTML = marked.parse(msgEl.textContent);
            document.getElementById('date').textContent = params.date;
        }
        window.onload = function() { fillContent(); };
    </script>
</body>
</html>"""


def test_page_html(token: str) -> str:
    """Render the interactive test page with the token embedded."""
    safe_token = (
        token
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
    return f"""\
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <title>WXPush 测试页面</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700&display=swap" rel="stylesheet">
    <style>
      body {{
        font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        display: flex; align-items: center; justify-content: center;
        min-height: 100vh; margin: 0; padding: 24px;
        background: linear-gradient(170deg, #f3e8ff 0%, #ffffff 100%);
        color: #1f2937; box-sizing: border-box;
      }}
      .container {{
        background: rgba(255,255,255,0.85); backdrop-filter: blur(10px);
        border-radius: 24px; box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.18); padding: 40px;
        max-width: 720px; width: 100%; text-align: left;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
      }}
      .container:hover {{ transform: translateY(-8px); box-shadow: 0 16px 40px rgba(0,0,0,0.12); }}
      h1 {{
        margin: 0 0 12px; font-size: 32px; font-weight: 700; text-align: center;
        background: linear-gradient(90deg, #8b5cf6, #3b82f6);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
      }}
      .hint {{ color: #4b5563; margin: 0 0 24px; font-size: 16px; line-height: 1.6; text-align: center; }}
      label {{ display: block; margin: 16px 0 8px; font-weight: 700; color: #374151; }}
      input[type=text], textarea {{
        width: 100%; padding: 12px; border: 1px solid #d4d4d8; border-radius: 12px;
        background: #f4f4f5; transition: all 0.2s ease; box-sizing: border-box;
        font-family: inherit; font-size: 14px;
      }}
      input[type=text]:focus, textarea:focus {{ outline: none; border-color: #8b5cf6; background: #fff; box-shadow: 0 0 0 2px #c4b5fd; }}
      button {{
        margin-top: 24px; padding: 12px 20px; border-radius: 12px; border: 0;
        background: #8b5cf6; color: #fff; cursor: pointer; font-weight: 700; transition: all 0.2s ease;
      }}
      button:hover {{ background: #7c3aed; transform: translateY(-2px); }}
      button#clearBtn {{ background: #f4f4f5; color: #374151; border: 1px solid #e4e4e7; }}
      button#clearBtn:hover {{ background: #fff; border-color: #d4d4d8; color: #1f2937; }}
      pre {{ background: #1f2937; color: #e5e7eb; padding: 16px; border-radius: 12px; white-space: pre-wrap; word-break: break-all; }}
    </style>
  </head>
  <body>
    <div class="container">
      <h1>WXPush 测试页面</h1>
      <p class="hint">当前 token (来自路径)：<strong>{safe_token}</strong></p>
      <form id="testForm" method="POST" action="/wxsend">
        <label for="title">标题 (title)</label>
        <input id="title" name="title" type="text" value="测试标题" />
        <label for="content">内容 (content)</label>
        <textarea id="content" name="content" rows="4">这是测试内容</textarea>
        <label for="userid">用户 ID (userid，可选，多用户用 | 分隔)</label>
        <input id="userid" name="userid" type="text" placeholder="例如: OPENID1|OPENID2" />
        <label for="appid">WX_APPID (可选，留空使用环境变量)</label>
        <input id="appid" name="appid" type="text" />
        <label for="secret">WX_SECRET (可选，留空使用环境变量)</label>
        <input id="secret" name="secret" type="text" />
        <label for="template_id">模板 ID (template_id，可选)</label>
        <input id="template_id" name="template_id" type="text" />
        <label for="base_url">跳转链接 base_url (可选)</label>
        <input id="base_url" name="base_url" type="text" />
        <input type="hidden" name="token" id="hiddenToken" value="{safe_token}" />
        <div style="display:flex;gap:12px;align-items:center">
          <button id="sendBtn" type="submit">发送测试请求</button>
          <button type="button" id="clearBtn">清空</button>
        </div>
      </form>
      <div id="responseCard" style="display:none; margin-top: 20px;">
        <label for="responseArea">响应</label>
        <pre id="responseArea"></pre>
      </div>
    </div>
    <script>
      const form = document.getElementById('testForm');
      const sendBtn = document.getElementById('sendBtn');
      const clearBtn = document.getElementById('clearBtn');
      const responseArea = document.getElementById('responseArea');
      const responseCard = document.getElementById('responseCard');

      clearBtn.addEventListener('click', () => {{
        ['title','content','userid','appid','secret','template_id','base_url'].forEach(id => {{
          const el = document.getElementById(id); if (el) el.value = '';
        }});
        responseArea.textContent = ''; responseCard.style.display = 'none';
      }});

      form.addEventListener('submit', async (event) => {{
        event.preventDefault();
        sendBtn.disabled = true;
        const originalText = sendBtn.textContent;
        sendBtn.textContent = '发送中...';
        responseCard.style.display = 'none';

        const formData = new FormData(form);
        const payload = {{}};
        for (const [k, v] of formData.entries()) {{
          if (k !== 'token' && v) payload[k] = v;
        }}

        try {{
          const token = document.getElementById('hiddenToken').value;
          const resp = await fetch('/wxsend', {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json', 'Authorization': token }},
            body: JSON.stringify(payload)
          }});
          const text = await resp.text();
          responseArea.textContent = 'Status: ' + resp.status + '\\n\\n' + text;
          responseCard.style.display = 'block';
        }} catch (err) {{
          responseArea.textContent = 'Fetch error: ' + err.message;
          responseCard.style.display = 'block';
        }} finally {{
          sendBtn.disabled = false; sendBtn.textContent = originalText;
        }}
      }});
    </script>
  </body>
</html>"""
