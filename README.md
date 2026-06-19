# WXPush Python 版

基于 FastAPI + Docker 的微信公众号模板消息推送服务，是原 [Cloudflare Workers 版本](../wxpush) 的 Python 重写。

## 特性

- 与原版接口完全兼容（相同路由、相同参数、相同响应格式）
- 异步 HTTP 请求（httpx），支持并发推送多用户
- 三级配置优先级：启动参数 > 环境变量 > 配置文件
- 支持 Docker Compose 一键部署
- 支持 GET / POST（JSON、表单、裸文本）多种请求方式

## 目录结构

```
wxpush-py/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 路由入口
│   ├── wx_api.py            # 微信 API 调用
│   └── html_pages.py        # 内联 HTML 页面
├── .env.example             # 环境变量模板
├── config.toml.example      # 配置文件模板
├── run.py                   # 服务启动入口（处理三级配置优先级）
├── .gitignore
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## 配置方式

优先级：**启动参数 > 环境变量 > 配置文件**

| 优先级 | 来源 | 适用场景 |
|:---:|---|---|
| 高 | 启动参数 | 临时覆盖单项配置 |
| 中 | 环境变量 / `.env` 文件 | Docker 部署、CI/CD |
| 低 | `config.toml` | 本地开发默认配置 |

### 配置项

| 环境变量 | CLI 参数 | 必填 | 说明 |
|---|---|:---:|---|
| `API_TOKEN` | `--token` | 是 | 接口访问令牌，调用时需要携带 |
| `WX_APPID` | `--appid` | 是 | 微信公众号 AppID |
| `WX_SECRET` | `--secret` | 是 | 微信公众号 AppSecret |
| `WX_USERID` | `--userid` | 是 | 默认接收用户的 OpenID，多个用 `|` 分隔 |
| `WX_TEMPLATE_ID` | `--template-id` | 是 | 微信模板消息 ID |
| `WX_BASE_URL` | `--base-url` | 否 | 消息点击后的跳转基础 URL |
| `PORT` | `--port` | 否 | 服务端口，默认 `3939` |

### 配置文件（config.toml）

```bash
cp config.toml.example config.toml   # 填入真实配置
```

### 环境变量（.env）

```bash
cp .env.example .env   # 填入真实配置
```

## 快速启动

### Docker（推荐）

```bash
cp config.toml.example config.toml   # 填入真实配置
docker compose up -d                  # 构建并运行
```

### 本地开发

```bash
pip install -r requirements.txt
cp config.toml.example config.toml   # 填入真实配置
python run.py --reload
```

也可以通过启动参数临时覆盖配置，无需修改任何文件：

```bash
python run.py --token YOUR_TOKEN --port 4000 --reload
```

## API 路由

| 路由 | 方法 | 说明 |
|---|---|---|
| `/` | GET | 首页 |
| `/skin` | GET | 消息展示皮肤（与 `/skin/quiet-night-sky` 等价） |
| `/skin/quiet-night-sky` | GET | 深蓝渐变风格皮肤 |
| `/skin/macos-hacker` | GET | 黑客终端风格皮肤 |
| `/<token>` | GET | 交互式测试页（需 token 正确） |
| `/wxsend` | GET / POST | 发送微信模板消息 |

## 消息展示皮肤

皮肤是一个独立的 HTML 页面，通过 URL 参数接收消息内容并渲染展示。配合 `WX_BASE_URL` 使用时，用户点击微信消息卡片即可跳转到皮肤页面查看详情。

### 可用皮肤

| 路由 | 风格 |
|---|---|
| `/skin/quiet-night-sky` | 深蓝渐变 + 毛玻璃卡片，支持完整 Markdown 样式 |
| `/skin/macos-hacker` | 黑底绿字，仿 macOS 终端窗口，Matrix 风格 |

### URL 参数

| 参数 | 说明 | 默认值 |
|---|---|---|
| `title` | 消息标题 | `消息推送` |
| `message` | 消息内容，支持 Markdown | `无告警信息` |
| `date` | 时间信息 | `无时间信息` |

消息内容由客户端 JavaScript 读取并渲染，Markdown 通过 [marked.js](https://cdn.jsdelivr.net/npm/marked/lib/marked.umd.js) CDN 处理。

### 配合 WX_BASE_URL 使用

将 `WX_BASE_URL` 设为某个皮肤路由的完整 URL，发送消息时会自动在后面拼接 `?message=...&date=...&title=...`：

```toml
# config.toml
WX_BASE_URL = "https://your-domain.com/skin/quiet-night-sky"
```

发送后生成的跳转链接格式为：

```
https://your-domain.com/skin/quiet-night-sky?message=<内容>&date=<时间>&title=<标题>
```

### 直接访问示例

```
http://localhost:3939/skin/macos-hacker?title=服务器告警&message=**CPU 负载过高**，当前：95%&date=2024-01-01 12:00:00
```

## `/wxsend` 参数

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `token` | String | 是 | 访问令牌，也可通过 `Authorization` 请求头传入 |
| `title` | String | 是 | 消息标题 |
| `content` | String | 是 | 消息内容 |
| `userid` | String | 否 | 临时覆盖默认接收用户，多个用 `|` 分隔 |
| `appid` | String | 否 | 临时覆盖默认 `WX_APPID` |
| `secret` | String | 否 | 临时覆盖默认 `WX_SECRET` |
| `template_id` | String | 否 | 临时覆盖默认模板 ID |
| `base_url` | String | 否 | 临时覆盖默认跳转 URL |

### GET 示例

```
http://localhost:3939/wxsend?token=YOUR_TOKEN&title=服务器通知&content=部署完成
```

### POST 示例（JSON）

```bash
curl -X POST http://localhost:3939/wxsend \
  -H "Authorization: YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Webhook 通知", "content": "自动化任务已完成。"}'
```

> **Windows / MINGW64 用户注意**：Git Bash（MINGW64）下直接在命令行用单引号传含中文的 body，可能因终端编码问题导致服务端 JSON 解析失败，报 `Missing required parameters`。建议将请求体以 UTF-8 编码保存到文件再传入：
>
> ```bash
> # 先用文本编辑器将以下内容保存为 body.json（UTF-8 编码）
> # {"title": "Webhook 通知", "content": "自动化任务已完成。"}
> curl -X POST http://localhost:3939/wxsend \
>   -H "Authorization: YOUR_TOKEN" \
>   -H "Content-Type: application/json" \
>   -d @body.json
> ```

### 成功响应

```json
{"msg": "Successfully sent messages to 1 user(s). First response: ok"}
```

### 失败响应

```json
{"msg": "Invalid token"}
```

## 与原版对应关系

原版基于 Cloudflare Workers（JavaScript），本版在保持接口完全兼容的前提下，用 Python 重写了全部逻辑：

| 原版 | 本版 |
|---|---|
| Cloudflare Workers | FastAPI + uvicorn |
| `fetch()` | httpx 异步 HTTP |
| Worker 环境变量 `env.*` | 系统环境变量 / `.env` 文件 |
| 无状态 serverless | Docker 容器 |

## 许可证

MIT License
