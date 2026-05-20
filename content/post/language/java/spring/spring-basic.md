---
title: spring basic
author: "-"
date: 2026-01-05T16:30:00+08:00
lastmod: 2026-05-20T10:49:27+08:00
url: spring-basic
categories:
  - language
tags:
  - java
  - spring
  - http
  - remix
  - AI-assisted
---
## spring basic

## @RestController

`@RestController` 是 `@Controller` 与 `@ResponseBody` 的组合注解，用于编写 **RESTful API**：控制器方法的返回值会直接写入 HTTP 响应体（通常是 JSON），而不是交给视图解析器去渲染页面。

```java
@RestController
@RequestMapping("/api/comments")
public class CommentController {

    @GetMapping("/{id}")
    public Comment get(@PathVariable long id) {
        return commentService.findById(id);
    }
}
```

上例中，`Comment` 对象会被 `HttpMessageConverter`（如 Jackson）序列化为 JSON 返回给客户端。

**适用场景：**

- 前后端分离：Vue、React、移动端等通过 HTTP 调用后端接口
- 微服务之间的 HTTP 调用
- 任何「请求数据 → 返回 JSON/XML」的 API

**不适用场景：**

- 传统的服务端渲染 Web 应用（JSP、Thymeleaf 等）：这类应用需要 `@Controller` 返回**视图名**或 `ModelAndView`，由视图解析器渲染 HTML 页面

```java
@Controller
public class PageController {

    @GetMapping("/home")
    public String home(Model model) {
        model.addAttribute("title", "Home");
        return "home";  // 解析为 home.jsp 或 templates/home.html
    }
}
```

若把 JSP/Thymeleaf 页面控制器写成 `@RestController`，返回值会被当作响应体内容（例如字符串 `"home"` 会原样输出），而不会走视图解析，页面无法正常渲染。

| 注解 | 返回值处理 | 典型用途 |
| ---- | ---------- | -------- |
| `@Controller` | 默认解析为视图名；方法上加 `@ResponseBody` 时才写入响应体 | MVC 页面、混合应用 |
| `@RestController` | 每个方法等价于带 `@ResponseBody` | RESTful API |

### 同样是 GET，浏览器和 fetch 怎么处理？

RESTful API 与传统 Web 应用的区别，**不是靠浏览器识别服务端用了哪种注解**，而是靠 **URL 路径、谁在发请求、响应的 `Content-Type`**。

| 场景 | 典型 URL | 谁发请求 | 服务器返回 |
| ---- | -------- | -------- | ---------- |
| 传统 Web | `GET /home` | 地址栏、`<a href>` 跳转 | 整页 HTML |
| RESTful API | `GET /api/users/1` | 页面内 `fetch` / axios | JSON body |

实践中通常用不同路径和不同控制器分开，而不是让前端在同一个 URL 上「猜」返回的是页面还是数据。

**地址栏 / 链接（整页导航）**

- 浏览器发 GET，默认 `Accept` 里会带 `text/html`，表示偏好 HTML 页面
- 收到响应后，**按响应的 `Content-Type` 决定如何展示**，不关心服务端是 `@RestController` 还是 JSP
- `Content-Type: text/html` → 解析并渲染网页
- `Content-Type: application/json` → 不渲染成页面，通常把 JSON 当文本显示

**页面内的 `fetch` / AJAX**

- 由 JS 代码决定如何解析，浏览器不会自动「知道这是 API」
- 返回 JSON 且调用 `response.json()` → 正常提取数据
- 返回 HTML（例如误请求了页面 URL，或未登录被重定向到登录页）→ HTTP 可能仍是 200，但 `response.json()` 会在**解析阶段**报错（`SyntaxError`）
- 生产代码应检查 `res.ok` 和 `Content-Type`，再选择 `.json()` 或 `.text()`

### Accept 与 Content-Type

| Header | 方向 | 含义 |
| ------ | ---- | ---- |
| `Accept` | 客户端 → 服务端 | 客户端声明能接受 / 更希望收到哪些类型的响应（偏好，服务端可参考也可不采纳） |
| `Content-Type` | 服务端 → 客户端 | 服务端声明响应体实际是什么类型（事实，客户端应按此解析和展示） |

可以记成：一个说「我想要什么」，一个说「我给你的是什么」。理想情况下两者匹配；不匹配时，客户端仍以 **`Content-Type` + body** 为准。

```http
# 浏览器打开页面
Accept: text/html,application/xhtml+xml,...

# JS 调 API
Accept: application/json

# 服务端响应
Content-Type: application/json;charset=UTF-8
Content-Type: text/html;charset=UTF-8
```

Spring 中 `@RestController` 通常配合 Jackson 返回 `application/json`；`@Controller` + 视图解析器通常返回 `text/html`。这是服务端的实现约定，浏览器只看到 HTTP 响应头与 body。

### Content-Type 与 body 不一致时

地址栏整页访问时，浏览器**优先相信 `Content-Type`**，不会根据服务端实现方式改变行为：

| Content-Type | 实际 body | 地址栏典型结果 |
| ------------ | --------- | -------------- |
| `application/json` | HTML | 不渲染成网页，多半当文本/源码显示 |
| `text/html` | JSON | 一般不报错，把 JSON 当页面文字显示 |
| `text/html` | HTML | 正常渲染网页 |
| `application/json` | JSON | 格式化或原文显示 JSON |

`fetch` 场景下，若代码假定 JSON 却收到 HTML，会在 `response.json()` 阶段失败，而不是浏览器拒绝显示。

## Spring Shell

Spring Shell 是一个用于构建**交互式命令行应用程序**的 Spring 框架，让开发者能够快速创建功能丰富的 CLI 工具。

**核心特性：**

- **注解驱动** - 使用 `@ShellComponent` 和 `@ShellMethod` 定义命令
- **自动补全** - Tab 键补全命令和参数
- **命令历史** - 支持历史命令记录和回溯
- **内置帮助** - 自动生成帮助文档
- **Spring Boot 集成** - 无缝集成 Spring Boot 生态

**典型使用场景：**

- 管理工具（部署、监控）
- 数据库客户端
- DevOps 工具
- 微服务管理控制台

**简单示例：**

```java
@ShellComponent
public class MyCommands {
    
    @ShellMethod("Say hello")
    public String hello(@ShellOption String name) {
        return "Hello " + name + "!";
    }
}
```

运行后可在交互式 shell 中执行：

```bash
shell:> hello --name World
Hello World!
```
