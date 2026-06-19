# WXPush Python 版

基于 FastAPI + Docker 的微信公众号模板消息推送服务，是原 [Cloudflare Workers 版本](../wxpush) 的 Python 重写。

## 特性

- 与原版接口完全兼容（相同路由、相同参数、相同响应格式）
- 异步 HTTP 请求（httpx），支持并发推送多用户
- 三级配置优先级：启动参数 > 环境变量 > 配置文件
- 支持 Docker Compose 一键部署
- 支持 GET / POST（JSON、表单、裸文本）多种请求方式
- 消息内容服务端存储（SQLite），跳转 URL 仅携带短 ID，无内容长度限制，7 天后自动清理

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
├── messages.db          # 消息存储（运行时自动创建，已加入 .gitignore）
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
| `PORT` | `--port` | 否 | 服务端口，默认 `40001` |

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

**前置条件**：VPS 已安装 Docker（20.10+）和 Docker Compose v2。

```bash
# 1. 克隆代码
git clone https://github.com/YanQiu0207/wxpush.git
cd wxpush/wxpush-py

# 2. 填写配置
cp config.toml.example config.toml
nano config.toml   # 填入 AppID、Secret、OpenID、Token 等

# 3. 构建并后台运行
docker compose up -d

# 4. 验证
docker compose ps        # State 应为 running
docker compose logs -f   # 查看实时日志
curl http://localhost:40001/
```

> **注意**：Docker 模式下端口通过 `PORT` 环境变量控制，`config.toml` 的 `[server] port` 不生效。如需改端口，在 `docker-compose.yml` 同级目录新建 `.env` 文件写入 `PORT=40001`，然后重新执行 `docker compose up -d`。

常用管理命令：

```bash
docker compose stop          # 停止（保留容器）
docker compose down          # 停止并删除容器
docker compose restart       # 重启
docker compose up -d --build # 重新构建镜像并启动（更新代码后使用）
```

**更新已部署版本：**

```bash
git pull
docker compose up -d --build

# 验证
docker compose ps        # State 应为 running
docker compose logs -f   # 确认启动日志正常
```

如果 VPS 开了防火墙，需要放行端口：

```bash
ufw allow 40001
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
| `/api/content/{id}` | GET | 获取已存储消息的内容（供皮肤页面调用） |
| `/wxsend` | GET / POST | 发送微信模板消息 |

## 消息展示皮肤

皮肤是独立的 HTML 页面，用于展示微信消息点击后的详情。消息内容存储在服务端 SQLite 数据库中，跳转 URL 仅携带 8 字符短 ID，无内容长度限制，7 天后自动清理。

### 可用皮肤

| 路由 | 风格 |
|---|---|
| `/skin/quiet-night-sky` | 深蓝渐变 + 毛玻璃卡片，支持完整 Markdown |
| `/skin/macos-hacker` | 黑底绿字，仿 macOS 终端窗口，Matrix 风格 |

### 配合 WX_BASE_URL 使用

将 `WX_BASE_URL` 设为某个皮肤路由的完整 URL：

```toml
# config.toml
wx_base_url = "https://your-domain.com/skin/quiet-night-sky"
```

发送消息时，服务端将内容存入数据库并生成短 ID，跳转链接格式为：

```
https://your-domain.com/skin/quiet-night-sky?id=abc12345
```

页面加载后通过 `/api/content/{id}` 从服务端拉取内容，并通过 [marked.js](https://cdn.jsdelivr.net/npm/marked/lib/marked.umd.js) 渲染 Markdown。

### 直接访问（兼容旧格式）

皮肤页面仍支持通过 URL 参数直接传入内容：

| 参数 | 说明 | 默认值 |
|---|---|---|
| `title` | 消息标题 | `消息推送` |
| `message` | 消息内容，支持 Markdown | `无告警信息` |
| `date` | 时间信息 | `无时间信息` |

```
http://localhost:40001/skin/macos-hacker?title=服务器告警&message=**CPU 负载过高**&date=2024-01-01 12:00:00
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
http://localhost:40001/wxsend?token=YOUR_TOKEN&title=服务器通知&content=部署完成
```

### POST 示例（JSON）

```bash
curl -X POST http://localhost:40001/wxsend \
  -H "Authorization: YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Webhook 通知", "content": "自动化任务已完成。"}'
```

> **Windows / MINGW64 用户注意**：Git Bash（MINGW64）下直接在命令行用单引号传含中文的 body，可能因终端编码问题导致服务端 JSON 解析失败，报 `Missing required parameters`。建议将请求体以 UTF-8 编码保存到文件再传入：
>
> ```bash
> # 先用文本编辑器将以下内容保存为 body.json（UTF-8 编码）
> # {"title": "Webhook 通知", "content": "自动化任务已完成。"}
> curl -X POST http://localhost:40001/wxsend \
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
