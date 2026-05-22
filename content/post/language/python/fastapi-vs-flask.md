---
title: FastAPI 与 Flask 对比
author: "-"
date: 2026-05-21T20:41:50+08:00
lastmod: 2026-05-21T20:41:50+08:00
url: fastapi-vs-flask
categories:
  - Python
tags:
  - python
  - flask
  - fastapi
  - web
  - remix
  - AI-assisted
---

## 概述

Flask 和 FastAPI 都是 Python 生态里常用的 Web 框架，适合写 REST API 和小型后端服务。Flask 出现更早、生态成熟；FastAPI 更年轻，主打类型注解、自动文档和高性能。两者都不是「全栈 MVC 框架」（那是 Django 的领域），选型时往往是在「轻量 API 框架」之间做取舍。

## 核心对比

| 维度 | Flask | FastAPI |
| ---- | ----- | ------- |
| 首发年份 | 2010 | 2018 |
| 维护方 | Pallets | Sebastián Ramírez 及社区 |
| 核心定位 | 微框架，灵活可扩展 | 现代 API 框架，开箱即用 |
| 路由与视图 | 装饰器 `@app.route` | 装饰器 `@app.get` 等，按 HTTP 方法拆分 |
| 请求/响应校验 | 需自行集成（如 Marshmallow、Pydantic） | 内置 Pydantic，类型即契约 |
| OpenAPI / Swagger | 需扩展（flask-smorest、apispec 等） | 内置，访问 `/docs`、`/redoc` |
| 异步支持 | 2.0+ 支持 `async def`，但生态仍以同步为主 | 原生 `async`，基于 ASGI |
| 默认服务器 | Werkzeug（开发），生产常用 Gunicorn + WSGI | Uvicorn / Hypercorn（ASGI） |
| 性能（粗略） | 中等，够用 | 通常更高（尤其 I/O 密集、高并发） |
| 学习曲线 | 平缓，文档与示例极多 | 需熟悉类型注解和 Pydantic |
| 生态与插件 | 非常丰富（登录、ORM、Admin 等） | 增长快，常与 SQLAlchemy、SQLModel 搭配 |

## Flask 简介

Flask 是「微框架」：只提供路由、请求上下文、模板（Jinja2）等核心能力，数据库、认证、序列化都靠扩展拼装。这种设计让项目可以极简起步，也适合已有架构的团队按需引入组件。

特点概括：

- **简单直观**：一个文件就能跑起一个 HTTP 服务
- **扩展多**：Flask-SQLAlchemy、Flask-Login、Blueprint 模块化等成熟方案多
- **同步思维为主**：大量教程和第三方库按 WSGI + 阻塞 I/O 编写；要用好异步需额外注意

最小示例：

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/items/<int:item_id>")
def get_item(item_id: int):
    return jsonify({"id": item_id, "name": "example"})

if __name__ == "__main__":
    app.run(debug=True)
```

运行：`flask run` 或 `python app.py`（开发环境）。

## FastAPI 简介

FastAPI 构建在 Starlette（ASGI）和 Pydantic 之上，面向需要**清晰 API 契约**和**较好并发**的场景。函数参数和返回值用 Python 类型标注，框架自动校验、序列化，并生成 OpenAPI 文档。

特点概括：

- **类型驱动**：路径参数、查询参数、Body 都有明确类型和校验错误信息
- **依赖注入**：`Depends()` 便于复用数据库会话、当前用户等
- **异步友好**：路由可写 `async def`，适合调用外部 HTTP、数据库连接池等

最小示例：

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    return {"id": item_id, "name": "example"}
```

运行：`uvicorn main:app --reload`。

访问 `http://127.0.0.1:8000/docs` 可看到自动生成的交互式 API 文档。

## 同一接口的写法对比

下面用「按 ID 查询资源」对比常见写法（FastAPI 侧校验由框架完成；Flask 侧需自己保证类型或引入扩展）。

**Flask：**

```python
from flask import Flask, jsonify, abort

app = Flask(__name__)

@app.route("/users/<int:user_id>")
def get_user(user_id):
    user = find_user(user_id)  # 业务逻辑
    if user is None:
        abort(404)
    return jsonify(user)
```

**FastAPI：**

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = await find_user(user_id)
    if user is None:
        raise HTTPException(status_code=404)
    return user
```

若要在 Flask 里做请求体校验，通常会再加一层 schema（例如 Pydantic 模型 + 手动 `model_validate`），而 FastAPI 把这一步内建在参数声明里。

## 性能与部署

- **Flask**：经典 **WSGI** 栈（Gunicorn、uWSGI + Nginx）。对 CPU 不重、并发中等的 API 完全够用。
- **FastAPI**：走 **ASGI**（Uvicorn、Gunicorn + Uvicorn worker）。在大量等待 I/O（调用下游 API、数据库）时，异步路由能更好利用连接；纯 CPU 密集任务两者都要靠多进程/任务队列，不能单靠框架「变快」。

实际性能还取决于 ORM、中间件和业务逻辑；不应只凭 benchmark 选型。

## 如何选型

| 场景 | 更倾向 |
| ---- | ------ |
| 团队已大量用 Flask，项目以维护为主 | Flask |
| 需要快速对外提供带文档的 REST API | FastAPI |
| 强依赖 Flask 特有扩展（某些 Admin、旧插件） | Flask |
| 新项目、重视类型提示与 OpenAPI | FastAPI |
| 以服务端渲染 HTML 为主的小站 | Flask（模板集成更常见） |
| 高并发 I/O、微服务网关式 API | FastAPI（或 Starlette） |

两者也可以共存于同一组织：例如边缘网关或新服务用 FastAPI，老服务继续 Flask，通过 HTTP 或消息队列集成。

## 小结

- **Flask**：老牌、灵活、资料多，适合「要什么自己装」和遗留项目。
- **FastAPI**：现代 API 优先，类型 + 文档 + 异步一体，适合新 API 和契约清晰的微服务。

没有绝对优劣；小项目用哪一个都能做好，关键是团队熟悉度、是否要内置 OpenAPI/校验，以及同步与异步模型是否与现有代码一致。

## 参考

- [Flask 官方文档](https://flask.palletsprojects.com/)
- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [Pydantic 文档](https://docs.pydantic.dev/)
