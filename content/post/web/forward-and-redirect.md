---
title: Forward 与 Redirect
author: "-"
date: 2012-09-21T07:07:03+00:00
lastmod: 2026-06-21T00:18:14+08:00
url: forward-and-redirect
categories:
  - web
tags:
  - java
  - servlet
  - spring-boot
  - remix
  - AI-assisted
aliases:
  - /p4153/
  - /p4173/
  - /jsp-forward-redirect/
---

## forward vs redirect

**forward**（请求转发）：服务器收到请求后，在**服务器内部**把请求转交给另一个资源处理，再把结果返回客户端；浏览器地址栏**不变**，客户端不知道发生了转发。

**redirect**（重定向）：服务器返回 3xx 状态码，浏览器**再次发起新请求**访问目标 URL，地址栏变为新地址；因此有两次往返，通常比 forward 开销大。

### 数据与作用域

- **forward**：同一 `HttpServletRequest` 继续传递，`request` 属性、`request` 参数可带到目标资源；常用 `request.getAttribute()` 读取上一环节放入的数据。
- **redirect**：浏览器发的是**新请求**，上一请求的 `request` 属性**不会**保留；URL 查询参数会随新请求带上。**HttpSession** 仍可通过 cookie 关联（session 级数据一般可用），但不要把「上一 request 的 attribute」误当成 redirect 后还能直接读。

效率：forward 仅在服务端处理，对客户端透明；redirect 多一次客户端往返，通常更慢。

范围：因 `request.setAttribute()` 的生命周期限于当前 request，redirect 会导致 attribute 丢失；需要跨 redirect 传值时，常用 session、URL 参数或 flash 等机制。

## 前后端分离下的表现

典型架构为 **React 前端 + Spring Boot REST API**。页面路由与组件组合由前端负责，后端主要返回 JSON；因此早年 JSP 时代「forward 到另一个 JSP 拼页面」的用法在业务层已基本消失，但两种机制仍以不同形式存在。

### redirect：仍然常见

redirect 是 HTTP 层行为，与是否使用 JSP 无关。前后端分离项目中常见场景：

- **OAuth / 第三方登录**：授权服务器回调后，后端或网关返回 302 跳转到前端路由（如 `/auth/callback`）
- **PRG（Post-Redirect-Get）**：表单或写操作后 `return "redirect:/..."`，避免刷新重复提交（多见于仍保留 `@Controller` 的服务端表单）
- **文件下载、外链跳转**：API 或网关返回 302 指向实际资源地址
- **网关 / 反向代理**：未登录时重定向到登录页（也可由前端根据 401 自行跳转）

前端日常路由切换由 **React Router** 完成，不经过 Servlet redirect；但**跨域认证、登录回调、下载**等仍会碰到 HTTP 重定向。

### forward：多为服务端内部行为

纯 API 项目里业务代码很少手写 `RequestDispatcher.forward()`，但在以下场景仍可能出现：

- **同域部署 SPA**：React 构建产物放在 Spring Boot `static/`，刷新 `/users/123` 等前端路由时，可用 `return "forward:/index.html"` 在服务端内部转给 `index.html`，再由 React Router 接管（前后端完全分开部署时，通常由 nginx `try_files` 承担同类职责）
- **Filter / 框架内部**：`DispatcherServlet`、错误页 `/error` 等可能在容器内 forward，一般无需业务代码介入

`@RestController` 返回 JSON 的主链路通常**既不 forward 也不 redirect**；理解 forward 仍有助排查 Filter 链、同包 SPA 刷新 404 等问题。更完整的 Servlet 栈说明见 [Servlet 生命周期](../other/servlet-lifecycle.md)。

### 对比小结

| 机制 | JSP 时代典型用法 | 前后端分离下的对应 |
| ---- | ---------------- | ------------------ |
| forward | 转发到另一个 JSP，共享 request 传数据 | 服务端内部转发（SPA 回退 `index.html`、框架内部）；页面间传参改由 **JSON 响应体** 或前端状态管理 |
| redirect | 跳转到另一个 JSP/URL | **OAuth 回调、PRG、下载跳转**；日常页面导航由 **React Router** 完成 |

## 相关

- API 层面：[getRequestDispatcher 与 sendRedirect](../other/getrequestdispatcher，-sendredirect.md)
- Servlet 栈与 Spring Boot：[Servlet 生命周期](../other/servlet-lifecycle.md)

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-06-20 | 补充 forward/redirect 与 session、request 作用域说明；链到 jsp-include | 承接自 java-basic 移出的 JavaEE 面试要点 |
| 2026-06-21 | 重命名为 `forward-and-redirect.md`；补充前后端分离场景；删除 jsp-include 专题 | 与 React + Spring Boot 现代架构对齐 |
