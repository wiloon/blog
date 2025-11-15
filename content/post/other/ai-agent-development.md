---
title: AI agent development
author: "-"
date: 2025-11-15T11:00:00+08:00
url: /?p=4058
categories:
  - Java
  - Web
tags:
  - reprint
  - remix
  - AI-assisted
---

# AI agent development

## 常用技术栈

1. 编程语言

- Python（主流，生态丰富）
- JavaScript/TypeScript（Web/Node.js Agent）
- Go、Java（高性能/企业级）

1. 大语言模型与 API

- OpenAI GPT-4/3.5、Claude、Llama
- Hugging Face Transformers
- LangChain、LlamaIndex（Agent 框架）

1. Web 框架与服务

- FastAPI、Flask（Python）
- Express.js（Node.js）
- Django

1. 数据存储

- Redis、MongoDB、PostgreSQL、SQLite
- 向量数据库：Milvus、Pinecone、Weaviate

1. 消息队列与异步任务

- Celery、RabbitMQ、Kafka

1. 容器与部署

- Docker、Kubernetes
- 云服务：AWS、Azure、GCP

1. 前端交互

- React、Vue.js
- WebSocket、RESTful API

1. 其他

- Prompt 工程、工具插件系统
- OAuth2、JWT（安全认证）
- 日志与监控：Prometheus、Grafana

## Python 调用模型方式

AI Agent 用 Python 开发时，可以调用本地模型或云端模型：

- 本地模型：如 Llama、GPT、transformers，可用 Hugging Face Transformers、llama.cpp 等库加载。
- 云端模型：如 OpenAI、Azure、百度文心、阿里通义，通过 HTTP API 或官方 SDK 远程调用。

选择本地或云端，取决于算力、数据安全、成本和功能需求。两者都支持 Python 调用，代码实现也很方便。

> 本文内容由 AI 辅助编辑

## AI Agent 外层代码与模型调用说明

AI Agent 通常用一种编程语言（如 Python、JavaScript、Go 等）编写外层逻辑代码，负责任务编排、数据处理、接口交互等。
最终核心智能部分是通过调用大语言模型（本地或云端）来实现推理、生成、理解等能力。

外层代码负责“连接”和“控制”，模型负责“智能”。两者结合，才能实现完整的 AI Agent。
## AI agent development
### 常用技术栈

- 1. 编程语言
- Python（主流，生态丰富）
- JavaScript/TypeScript（Web/Node.js Agent）
- Go、Java（高性能/企业级）
- Python（主流，生态丰富）
- JavaScript/TypeScript（Web/Node.js Agent）
- Go、Java（高性能/企业级）
@@

- 1. 大语言模型与 API
- OpenAI GPT-4/3.5、Claude、Llama
- Hugging Face Transformers
- LangChain、LlamaIndex（Agent 框架）
- OpenAI GPT-4/3.5、Claude、Llama
- Hugging Face Transformers
- LangChain、LlamaIndex（Agent 框架）
@@

- 1. Web 框架与服务
- FastAPI、Flask（Python）
- Express.js（Node.js）
- Django
- FastAPI、Flask（Python）
- Express.js（Node.js）
- Django
@@

- 1. 数据存储
- Redis、MongoDB、PostgreSQL、SQLite
- 向量数据库：Milvus、Pinecone、Weaviate
- Redis、MongoDB、PostgreSQL、SQLite
- 向量数据库：Milvus、Pinecone、Weaviate
@@

- 1. 消息队列与异步任务
- Celery、RabbitMQ、Kafka
- Celery、RabbitMQ、Kafka
@@

- 1. 容器与部署
- Docker、Kubernetes
- 云服务：AWS、Azure、GCP
- Docker、Kubernetes
- 云服务：AWS、Azure、GCP
@@

- 1. 前端交互
- React、Vue.js
- WebSocket、RESTful API
- React、Vue.js
- WebSocket、RESTful API
@@

- 1. 其他
- Prompt 工程、工具插件系统
- OAuth2、JWT（安全认证）
- 日志与监控：Prometheus、Grafana
- Prompt 工程、工具插件系统
- OAuth2、JWT（安全认证）
- 日志与监控：Prometheus、Grafana
