# 使用 Caddy 配置反向代理

Caddy 会自动申请和续签 HTTPS 证书，无需额外配置。

## 前置条件

- VPS 已运行 wxpush 容器
- 域名 DNS 已解析到该 VPS 的 IP

## 安装 Caddy

```bash
apt install -y debian-keyring debian-archive-keyring apt-transport-https curl
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | tee /etc/apt/sources.list.d/caddy-stable.list
apt update && apt install caddy
```

## 配置

编辑 `/etc/caddy/Caddyfile`，添加：

```
your-domain.com {
    reverse_proxy localhost:40001
}
```

将 `your-domain.com` 替换为你的域名，端口与 `docker-compose.yml` 中 `PORT` 保持一致。

## 启动

```bash
systemctl reload caddy
```

## 验证

```bash
systemctl status caddy          # 确认 Caddy 运行正常
curl https://your-domain.com/   # 测试 HTTPS 是否通
```

访问 `https://your-domain.com` 即可使用 wxpush 服务。
