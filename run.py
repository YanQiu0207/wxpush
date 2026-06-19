import argparse
import os
import tomllib
import uvicorn
from pathlib import Path
from dotenv import dotenv_values

# TOML [app] 键名 → 环境变量名
_APP_KEYS: dict[str, str] = {
    "api_token":      "API_TOKEN",
    "wx_appid":       "WX_APPID",
    "wx_secret":      "WX_SECRET",
    "wx_userid":      "WX_USERID",
    "wx_template_id": "WX_TEMPLATE_ID",
    "wx_base_url":    "WX_BASE_URL",
}

# CLI 参数名 → 环境变量名
_CLI_ENV_KEYS: dict[str, str] = {
    "token":       "API_TOKEN",
    "appid":       "WX_APPID",
    "secret":      "WX_SECRET",
    "userid":      "WX_USERID",
    "template_id": "WX_TEMPLATE_ID",
    "base_url":    "WX_BASE_URL",
    "port":        "PORT",
}


def _build_config(args: argparse.Namespace) -> dict[str, str]:
    cfg: dict[str, str] = {}

    # 1. 配置文件（最低优先级）
    config_path = Path("config.toml")
    if config_path.exists():
        with open(config_path, "rb") as f:
            data = tomllib.load(f)
        for toml_key, env_key in _APP_KEYS.items():
            if val := data.get("app", {}).get(toml_key, ""):
                cfg[env_key] = str(val)
        if port := data.get("server", {}).get("port"):
            cfg["PORT"] = str(port)

    # 2. .env 文件，再覆盖为系统环境变量
    for k, v in dotenv_values(".env").items():
        if v:
            cfg[k] = v
    for env_key in _CLI_ENV_KEYS.values():
        if val := os.environ.get(env_key):
            cfg[env_key] = val

    # 3. CLI 参数（最高优先级）
    for arg_name, env_key in _CLI_ENV_KEYS.items():
        if (val := getattr(args, arg_name, None)) is not None:
            cfg[env_key] = val

    return cfg


def main() -> None:
    parser = argparse.ArgumentParser(description="WXPush service launcher")
    for arg_name in _CLI_ENV_KEYS:
        parser.add_argument(f"--{arg_name.replace('_', '-')}", default=None)
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload (development only)")
    args = parser.parse_args()

    cfg = _build_config(args)
    os.environ.update(cfg)
    uvicorn.run(
        "app.main:app",
        host=args.host,
        port=int(cfg.get("PORT", 40001)),
        reload=args.reload,
    )


if __name__ == "__main__":
    main()
