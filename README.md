# AIGC Image Generator

基于 Stable Diffusion WebUI API 的图片批量生成工具，并提供 Flask Web 服务。

## 功能

- 单张/批量生成图片（Python 脚本）
- HTTP API 接口（`/generate`, `/batch_generate`）
- 支持自定义生成参数（steps, width, height, cfg_scale, negative_prompt 等）

## 技术栈

- Python 3.8+
- Stable Diffusion WebUI (API)
- Flask
- requests, Pillow

## 快速开始

1. **启动 Stable Diffusion WebUI**，并确保开启 API（启动参数 `--api`）。
2. **安装依赖**：
   ```bash
   pip install requests flask pillow