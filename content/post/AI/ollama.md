---
title: "Ollama - 本地大语言模型运行工具"
author: "-"
date: 2025-11-14T18:52:00+08:00
url: ollama
categories:
  - AI
tags:
  - AI
  - LLM
---

## Ollama 简介

Ollama 是一个开源的本地大语言模型运行工具，可以让你在本地轻松运行 Llama 2、Mistral、Qwen 等多种开源大语言模型。

## 安装 Ollama

### Linux 安装

```bash
# 使用官方安装脚本
curl -fsSL https://ollama.com/install.sh | sh
```

**安装记录 (2025-11-14)**：
- 安装版本：v0.12.11
- 安装位置：`/usr/local/bin/ollama`
- 服务配置：已创建 systemd 服务 `ollama.service`
- 默认监听：`127.0.0.1:11434`
- GPU 支持：检测到 AMD GPU，安装了 ROCm 支持
- 用户组：创建了 ollama 用户，并加入 render 和 video 组
- 自动启动：服务已启用并自动运行

### 手动安装

```bash
# 下载二进制文件
curl -L https://ollama.com/download/ollama-linux-amd64 -o ollama
chmod +x ollama
sudo mv ollama /usr/local/bin/
```

### 验证安装

```bash
# 检查版本
ollama --version
# 输出: ollama version is 0.12.11

# 检查服务状态
systemctl status ollama

# 测试 API 是否可用
curl http://127.0.0.1:11434/api/version
# 输出: {"version":"0.12.11"}
```

## 基本使用

### 启动 Ollama 服务

```bash
# 启动服务
ollama serve
```

### 拉取模型

```bash
# 拉取 Llama 2 模型（7B 参数版本）
ollama pull llama2

# 拉取 Mistral 模型
ollama pull mistral

# 拉取 Qwen 模型
ollama pull qwen

# 拉取 Phi 模型（推荐入门）
ollama pull phi
```

**本地已安装模型 (2025-11-14)**：
- `phi:latest` - 1.6 GB，微软 Phi-3 模型（3.8B 参数）

### 运行模型

```bash
# 运行对话
ollama run phi

# 命令行快速测试
echo "Hello! Please introduce yourself." | ollama run phi

# 退出对话（交互模式下）
/bye
```

**Phi 模型测试记录 (2025-11-14)**：

1. **英文对话测试**：
```bash
echo "Hello! Please introduce yourself in English briefly." | ollama run phi
# 输出: Greetings! My name is AI-Assist, and I'm here to assist you 
# with any queries or tasks you may have. How can I help you today?
```

2. **代码生成测试**：
```bash
echo "Write a simple Python function to calculate fibonacci numbers" | ollama run phi
# 成功生成了正确的斐波那契数列函数
```

3. **中文支持**：Phi 模型对中文支持较弱，建议使用 Qwen 系列模型处理中文任务

### 列出已安装的模型

```bash
ollama list
```

### 删除模型

```bash
ollama rm llama2
```

## API 使用

Ollama 提供了 REST API 接口，默认监听在 `http://localhost:11434`。

### 生成文本

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama2",
  "prompt": "Why is the sky blue?"
}'
```

### 对话模式

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "llama2",
  "messages": [
    { "role": "user", "content": "Why is the sky blue?" }
  ]
}'
```

## 常用模型

- **llama2**: Meta 的开源模型，7B/13B/70B 参数版本
- **llama3.2**: Meta 最新的 Llama 3.2 模型，1B/3B 参数版本（轻量级）
- **mistral**: Mistral AI 的高性能模型，7B 参数
- **qwen**: 阿里巴巴的千问模型，支持中文
- **qwen2.5**: 千问 2.5 版本，0.5B/1.5B/3B/7B/14B/32B/72B 多种规格
- **codellama**: Meta 专门用于编程的 Code Llama 模型
- **phi**: 微软（Microsoft）的小型高效模型，Phi-3 系列包含 3.8B 参数
- **phi4**: 微软最新的 Phi-4 模型，14B 参数，性能优异
- **gemma2**: Google 的 Gemma 2 模型，2B/9B/27B 参数版本
- **deepseek-r1**: DeepSeek 的推理模型，具有强大的推理能力

### 推荐入门模型

对于首次使用，推荐以下轻量级模型（内存占用较小）：
- **qwen2.5:0.5b** - 仅 0.5B 参数，约 400MB
- **qwen2.5:1.5b** - 1.5B 参数，约 1GB
- **phi** - 3.8B 参数，约 2.3GB
- **gemma2:2b** - 2B 参数，约 1.6GB

## 系统要求

- **内存**: 至少 8GB RAM（推荐 16GB+）
- **存储**: 根据模型大小，一般 4-40GB
- **GPU**: 可选，支持 NVIDIA GPU 加速

## 配置

### 环境变量

```bash
# 设置模型存储路径
export OLLAMA_MODELS=/path/to/models

# 设置服务监听地址
export OLLAMA_HOST=0.0.0.0:11434
```

### Systemd 服务管理

Ollama 安装后会自动创建并启动 systemd 服务：

```bash
# 查看服务状态
systemctl status ollama

# 启动服务
sudo systemctl start ollama

# 停止服务
sudo systemctl stop ollama

# 重启服务
sudo systemctl restart ollama

# 禁用开机自启
sudo systemctl disable ollama

# 启用开机自启
sudo systemctl enable ollama

# 查看服务日志
journalctl -u ollama -f
```

### 模型存储位置

默认模型存储在：`~/.ollama/models/`

## 参考链接

- [Ollama 官网](https://ollama.com/)
- [Ollama GitHub](https://github.com/ollama/ollama)
- [模型库](https://ollama.com/library)
