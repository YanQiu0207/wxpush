# Sub2API API Key 使用说明总结

## 1. 核心结论

**Sub2API 后台创建的 API Key 不必须配置在 Codex 里才能使用。**

Codex 只是一个客户端。只要某个工具、脚本或程序能够按照 Sub2API 支持的 HTTP API 格式发起请求，就可以使用这个 API Key。

换句话说，Sub2API 的 API Key 是给 **Sub2API 网关鉴权** 用的，不是 Codex 专用 Key。

---

## 2. Sub2API 的整体调用链路

```text
你的客户端
  ↓ 携带 Sub2API 创建的 API Key
Sub2API 网关
  ↓ 根据分组、账号、模型、策略转发
上游 AI 服务
```

这里的“客户端”可以是：

```text
Codex CLI
Claude Code
Cursor
OpenWebUI
LobeChat
Postman
curl
Python 脚本
Node.js 程序
C++ HTTP 客户端
其他支持自定义 API Base URL 的工具
```

只要接口路径、鉴权头和请求 JSON 格式匹配，就可以使用。

---

## 3. 通用配置方式

如果 Sub2API 使用本地 Docker 部署，通常可以按下面方式理解：

```text
API Base URL: http://localhost:41550/v1
API Key:      Sub2API 后台创建的 API Key
Model:        Sub2API 后台分组/账号中可用的模型名
```

如果部署在服务器上，则可能是：

```text
API Base URL: http://服务器IP:41550/v1
```

或者经过反向代理后：

```text
API Base URL: https://你的域名/v1
```

---

## 4. 使用 curl 调用 OpenAI Responses 风格接口

如果 Sub2API 暴露的是 OpenAI 兼容接口，可以尝试：

```bash
curl http://localhost:41550/v1/responses \
  -H "Authorization: Bearer <你的_Sub2API_API_Key>" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "<你的模型名>",
    "input": "你好，简单介绍一下你自己"
  }'
```

关键点：

```text
Authorization: Bearer <Sub2API 后台创建的 API Key>
Content-Type: application/json
接口路径: /v1/responses
```

---

## 5. 使用 Python OpenAI SDK 调用

很多 OpenAI-compatible 网关都可以通过修改 `base_url` 接入。

示例：

```python
from openai import OpenAI

client = OpenAI(
    api_key="<你的_Sub2API_API_Key>",
    base_url="http://localhost:41550/v1"
)

resp = client.responses.create(
    model="<你的模型名>",
    input="你好"
)

print(resp.output_text)
```

重点是：

```text
base_url = http://localhost:41550/v1
api_key  = Sub2API 后台创建的 API Key
```

不要把 API Key 写成上游平台的 Key。客户端访问的是 Sub2API，所以这里应该填 Sub2API 生成的 Key。

---

## 6. 使用 Anthropic / Claude Messages 风格接口

如果客户端使用的是 Claude / Anthropic Messages 接口，可能会走：

```text
/v1/messages
```

示例：

```bash
curl http://localhost:41550/v1/messages \
  -H "x-api-key: <你的_Sub2API_API_Key>" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "<你的模型名>",
    "max_tokens": 100,
    "messages": [
      {
        "role": "user",
        "content": "你好"
      }
    ]
  }'
```

注意：  
不同协议的鉴权头可能不同。

OpenAI 风格通常是：

```text
Authorization: Bearer <API_KEY>
```

Anthropic 风格通常是：

```text
x-api-key: <API_KEY>
```

具体以 Sub2API 当前版本支持的接口为准。

---

## 7. Codex 只是其中一种使用方式

如果你把 API Key 配置到 Codex 里，本质上是让 Codex 这个客户端访问 Sub2API。

但你也可以自己写程序直接访问：

```text
curl
Postman
Python
Node.js
C++
Go
Java
任意 HTTP 客户端
```

所以不要把 Sub2API 理解成“只能给 Codex 用的服务”。

更准确的理解是：

```text
Sub2API 是一个 AI API 网关 / 代理服务。
Codex、Claude Code、Postman、脚本程序都只是调用它的客户端。
```

---

## 8. 推荐选择哪种接口

| 使用场景 | 推荐接口 |
|---|---|
| 新代码，想按 OpenAI 新接口调用 | `/v1/responses` |
| 老工具只支持 Chat Completions | `/v1/chat/completions` |
| Claude Code / Anthropic SDK 类工具 | `/v1/messages` |
| 自己写脚本测试 | 先用 `curl` 验证 |
| 图形化调试 | Postman / Apifox |

---

## 9. 常见注意事项

### 9.1 API Base URL 要写对

本地 Docker 部署时通常是：

```text
http://localhost:41550/v1
```

不要随意写成：

```text
http://localhost:41550/openai/v1
```

除非 Sub2API 文档或后台明确要求这样配置。

---

### 9.2 Model 名称要和后台可用模型一致

请求中的：

```json
{
  "model": "<你的模型名>"
}
```

必须是 Sub2API 后台当前分组/账号支持的模型名。

如果模型名写错，可能会出现：

```text
model not found
upstream error
route not found
permission denied
```

---

### 9.3 API Key 是 Sub2API 的 Key，不是上游 Key

客户端侧应该配置：

```text
Sub2API 后台生成的 API Key
```

而不是直接配置 OpenAI、Claude、Gemini 等上游账号的 Key。

上游账号是在 Sub2API 后台“导入账号”时配置的，由 Sub2API 统一管理。

---

### 9.4 远程部署建议使用 HTTPS

如果 Sub2API 只是本机测试：

```text
http://localhost:41550/v1
```

问题不大。

如果部署在公网服务器上，不建议直接裸露 HTTP 端口，建议使用：

```text
Nginx / Caddy / Traefik + HTTPS
```

并做好：

```text
防火墙
访问控制
API Key 权限控制
日志审计
限流策略
```

---

### 9.5 Docker 部署时 localhost 的含义

如果客户端和 Sub2API 在同一台 Windows 机器上：

```text
http://localhost:41550/v1
```

通常可以访问。

如果客户端在另一台机器上，则不能写 localhost，需要写部署机器的局域网 IP 或域名，例如：

```text
http://192.168.1.100:41550/v1
```

---

## 10. 快速验证清单

部署完成后，可以按这个顺序验证：

```text
1. Docker 容器是否启动
2. 浏览器是否能打开后台页面
3. 后台是否已创建分组
4. 后台是否已导入上游账号
5. 后台是否已创建 API Key
6. API Key 是否绑定了正确分组/权限
7. curl 是否能请求成功
8. Postman / Python / Codex 等客户端再接入
```

推荐先用 `curl` 验证接口可用，再接入 Codex 或其他客户端。

---

## 11. 总结

Sub2API 的 API Key 不依赖 Codex。

你可以把 Sub2API 当成一个本地或私有化部署的 AI API 网关：

```text
客户端 → Sub2API → 上游 AI 服务
```

Codex 只是客户端之一。  
你完全可以用 curl、Postman、Python SDK、Node.js、C++ HTTP 客户端或其他支持自定义 API Base URL 的工具来调用它。

最核心的配置只有三个：

```text
API Base URL: http://localhost:41550/v1
API Key:      Sub2API 后台创建的 API Key
Model:        后台可用模型名
```

---

## 12. 本次实测补充：余额不足与管理员充值

### 12.1 当前本机部署地址

当前这台机器的 Docker Compose 端口映射是：宿主机 `41550` → 容器内 `8080`。因此在本机 Git Bash、PowerShell、Python 脚本里调用时，优先使用：

```text
http://localhost:41550/v1
```

对应环境变量示例：

```bash
export SUB2API_KEY="sk-****"
export SUB2API_BASE_URL="http://localhost:41550/v1"
```

这里的 `sk-****` 是 Sub2API 后台创建的 API Key，占位符已脱敏。不要把真实 Key 写入文档、截图或 Git 仓库。

### 12.2 `INSUFFICIENT_BALANCE` 是谁返回的

调用：

```bash
curl "$SUB2API_BASE_URL/models" \
  -H "Authorization: Bearer $SUB2API_KEY"
```

如果返回：

```json
{
  "code": "INSUFFICIENT_BALANCE",
  "message": "Insufficient account balance"
}
```

这表示 Sub2API 在网关层做余额校验时拦截了请求。请求还没有成功转发到上游 OpenAI 或其他模型服务。

判断依据：

- 请求地址是 `http://localhost:41550/v1/models`，命中的是本机 Sub2API。
- 本机日志中记录了 `/v1/models` 请求，并返回 `403`。
- 当前 `standard` 运行模式包含计费和余额校验。
- 当前默认配置里 `user_balance` 是 `0`。

### 12.3 管理员如何给用户增加余额

管理员需要给 **API Key 所属用户** 加余额，不一定是给管理员自己加余额。操作路径：

1. 打开 `http://localhost:41550/admin/users`。
2. 使用管理员账号登录。
3. 找到创建该 API Key 的用户。
4. 点击用户行右侧的更多操作。
5. 选择 `充值` / `Deposit`。
6. 填写金额，例如 `10`，确认。
7. 回到命令行重新执行 `/v1/models` 或 `/v1/responses` 测试。

后台前端资源中可以看到用户管理页包含 `deposit`、`withdraw`、`balanceHistory` 等操作，因此余额调整应优先通过后台用户管理完成。

### 12.4 充值后再次验证

```bash
curl "$SUB2API_BASE_URL/models" \
  -H "Authorization: Bearer $SUB2API_KEY"
```

如果余额、分组、账号和模型配置都正常，应该不再返回 `INSUFFICIENT_BALANCE`。

如果继续失败，再按顺序检查：

1. API Key 是否仍有效。
2. API Key 所属用户余额是否大于 `0`。
3. 用户是否绑定正确分组。
4. 分组是否有可用账号。
5. 模型名称是否在该分组和账号中可用。
6. 上游账号是否可用。

---

## 13. Windows 自动保活：每分钟检查 Sub2API

### 13.1 目标

当前 Docker Compose 已经为 `sub2api`、`sub2api-postgres`、`sub2api-redis` 配置了 `restart: unless-stopped`。这能让 Docker 启动后自动恢复容器，但如果实际环境中出现 Docker 已启动而 `sub2api` 没有运行的情况，可以额外使用 Windows 计划任务做兜底保活。

本机已新增一个 watchdog 脚本：

```text
E:\work\sub2api-deploy\scripts\ensure_sub2api.py
```

它的行为是：

1. 检查 Docker 是否可用。
2. 如果 Docker 没启动，直接跳过，不弹错。
3. 如果 Docker 已启动，检查 `sub2api` 容器状态。
4. 如果 `sub2api` 已经是 `running`，安静退出。
5. 如果 `sub2api` 不存在或不是 `running`，执行 `docker compose up -d` 拉起整个 Sub2API Compose 栈。

### 13.2 后台运行方式

为了避免每分钟弹出控制台窗口，计划任务使用的是 `pythonw.exe`，不是 `python.exe`。

当前计划任务执行命令为：

```text
"C:\msys64\mingw64\bin\pythonw.exe" "E:\work\sub2api-deploy\scripts\ensure_sub2api.py"
```

脚本内部调用 Docker 子进程时，也使用了 Windows 的 `CREATE_NO_WINDOW` 标志，避免 `docker` 命令弹出窗口。

### 13.3 Windows 计划任务配置

当前已注册的任务：

```text
任务名：Sub2API Watchdog
执行频率：每 1 分钟
执行用户：YanQi
Logon Mode：Interactive only
Last Result：0
```

`Interactive only` 表示该任务在当前 Windows 用户登录后运行。这与 Docker Desktop 常见的「用户登录后自动启动 Docker」模式匹配。

### 13.4 验证结果

已做过关键路径验证：

1. 手动停止 `sub2api` 容器。
2. 执行 `ensure_sub2api.py`。
3. 脚本检测到 `sub2api` 状态为 `exited`。
4. 脚本执行 `docker compose up -d`。
5. `sub2api` 恢复为 `healthy`。

watchdog 日志路径：

```text
E:\work\sub2api-deploy\data\logs\sub2api-watchdog.log
```

日志中可以看到类似记录：

```text
sub2api is not running. status=exited
Started Sub2API compose stack.
```

### 13.5 常用管理命令

查询计划任务：

```powershell
schtasks /Query /TN "Sub2API Watchdog" /V /FO LIST
```

手动触发一次：

```powershell
schtasks /Run /TN "Sub2API Watchdog"
```

删除计划任务：

```powershell
schtasks /Delete /TN "Sub2API Watchdog" /F
```

查看 watchdog 日志：

```powershell
Get-Content E:\work\sub2api-deploy\data\logs\sub2api-watchdog.log -Tail 20
```

### 13.6 注意事项

- 不要使用 `python.exe` 注册该计划任务，否则可能每分钟弹出控制台窗口。
- 不要频繁执行 `docker compose down`，它会删除容器；watchdog 虽然可以重新创建，但恢复时间会更长。
- 如果只是临时停止 Sub2API，计划任务会在下一分钟把它拉起来；要长期停用，请先禁用或删除 `Sub2API Watchdog` 计划任务。
- 当前脚本不包含任何 API Key，也不会读取、记录或输出密钥。

---

## 14. 参考链接

- 本机 Sub2API Docker Compose 配置：[docker-compose.yml](E:/work/sub2api-deploy/docker-compose.yml)
- 本机 Sub2API 环境变量示例：[.env.example](E:/work/sub2api-deploy/.env.example)
- 本机 Sub2API 运行配置：[data/config.yaml](E:/work/sub2api-deploy/data/config.yaml)
- 本机 Sub2API 访问日志：[data/logs/sub2api.log](E:/work/sub2api-deploy/data/logs/sub2api.log)
- 本机 Sub2API Watchdog 脚本：[scripts/ensure_sub2api.py](E:/work/sub2api-deploy/scripts/ensure_sub2api.py)
- 本机 Sub2API Watchdog 日志：[data/logs/sub2api-watchdog.log](E:/work/sub2api-deploy/data/logs/sub2api-watchdog.log)
- Sub2API README_CN: https://github.com/Wei-Shaw/sub2api/blob/main/README_CN.md
- Sub2API Docker Compose 示例: https://github.com/Wei-Shaw/sub2api/blob/main/deploy/docker-compose.local.yml
- OpenAI API 认证说明：https://developers.openai.com/api/reference/overview#authentication
- OpenAI Python SDK：https://github.com/openai/openai-python
- OpenAI Responses API 说明：https://developers.openai.com/api/docs/guides/migrate-to-responses



