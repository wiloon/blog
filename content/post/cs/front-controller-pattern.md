---
title: Front Controller Pattern
author: "-"
date: 2017-02-12T11:45:56+00:00
lastmod: 2026-05-11T16:19:04+08:00
url: front-controller-pattern
categories:
  - pattern
tags:
  - java
  - spring
  - remix
  - AI-assisted
aliases:
  - /p9800/
---

## 概述

Front Controller Pattern（前端控制器模式）来自 Martin Fowler 的《企业应用架构模式》（Patterns of Enterprise Application Architecture，2002），属于 Web 层架构模式，**不是** GoF 23 种设计模式的一部分。

详见 [企业应用架构模式](enterprise-application-architecture-patterns)。

## 解决的问题

在原始 Servlet 时代，每个 URL 对应一个独立的 Servlet 类，这是 **Page Controller** 模式：

```
/users    → UsersServlet
/orders   → OrdersServlet
/products → ProductsServlet
```

每个 Servlet 都要自己处理身份验证、日志记录、权限检查，代码大量重复。随着 URL 增多，`web.xml` 里的注册条目也膨胀。

Front Controller 的解法是**单一入口**：

```
所有请求 → FrontController（统一处理横切关注点）→ Dispatcher → 具体处理器
```

## 三个角色

- **Front Controller**：所有请求的唯一入口，集中处理身份验证、权限验证、日志追踪等横切关注点
- **Dispatcher**：将请求路由到对应的具体处理器（View/Handler）
- **View / Handler**：真正处理业务逻辑的模块

## Spring MVC 中的实现

Spring MVC 的 `DispatcherServlet` 是 Front Controller 模式的标准实现：

```
HTTP 请求
  → DispatcherServlet（Front Controller，映射到 /）
  → HandlerMapping（查找 URL 对应的 Controller 方法）
  → Controller 方法（业务逻辑）
  → 返回响应
```

你写的每一个 `@GetMapping`、`@PostMapping` 注解，本质上是在向 `DispatcherServlet` 的路由表注册一条规则。

传统方式需要在 `web.xml` 中手动注册：

```xml
<servlet>
  <servlet-name>dispatcher</servlet-name>
  <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
</servlet>
<servlet-mapping>
  <servlet-name>dispatcher</servlet-name>
  <url-pattern>/</url-pattern>
</servlet-mapping>
```

Spring Boot 的自动配置（`DispatcherServletAutoConfiguration`）在启动时替你完成这个注册，无需任何 XML。

## 简单代码示例

`HomeView`、`StudentView` 提供真正的业务处理逻辑，`Dispatcher` 路由到对应 View，`FrontController` 作为统一入口处理横切关注点。

```java
public class HomeView {
    public void show() {
        System.out.println("show Home view");
    }
}

public class StudentView {
    public void show() {
        System.out.println("show student view");
    }
}

public class Dispatcher {
    private StudentView studentView = new StudentView();
    private HomeView homeView = new HomeView();

    public void dispatch(String viewName) {
        if ("homeView".equals(viewName)) {
            homeView.show();
        } else {
            studentView.show();
        }
    }
}

public class FrontController {
    private Dispatcher dispatcher = new Dispatcher();

    public boolean isAuthenticUser() {
        System.out.println("Authenticate user");
        return true;
    }

    public void trackRequest(String viewName) {
        System.out.println("track request: " + viewName);
    }

    public void dispatchRequest(String viewName) {
        trackRequest(viewName);
        if (isAuthenticUser()) {
            dispatcher.dispatch(viewName);
        }
    }
}

public class FrontControllerPatternDemo {
    public static void main(String[] args) {
        FrontController frontController = new FrontController();
        frontController.dispatchRequest("homeView");
        frontController.dispatchRequest("studentView");
    }
}
```
