---
title: 责任链模式, Chain of Responsibility Pattern
author: "-"
date: 2026-04-16T18:27:55+08:00
lastmod: 2026-05-15T13:51:47+08:00
url: chain-of-responsibility
categories:
  - Pattern
tags:
  - Pattern
  - remix
  - AI-assisted
---
## 责任链模式, Chain of Responsibility Pattern

责任链模式（Chain of Responsibility）将请求沿着一条处理者链传递，每个处理者决定是否处理该请求，或将其传递给链上的下一个处理者。请求的发送者无需知道最终由哪个处理者来处理，从而实现了发送者与接收者的解耦。

## 核心思想

不使用责任链时，请求方往往需要硬编码逻辑来判断应该由哪个对象处理，导致紧耦合和大量条件判断。责任链将这些处理者串联起来，请求沿链传递，直到被某个处理者处理（或到达链尾）。

## 角色

- **Handler（抽象处理者）**：定义处理请求的接口，通常包含设置下一个处理者的方法。
- **ConcreteHandler（具体处理者）**：实现处理逻辑，决定自己是否处理请求，如果不处理则转发给下一个处理者。
- **Client（客户端）**：构建责任链并向链头发起请求。

## 示例：Java Servlet Filter 链

Servlet 规范中，请求在到达 Servlet 之前会依次经过一组 Filter，每个 Filter 可以对请求/响应做处理，然后调用 `chain.doFilter()` 继续传递，或直接中断返回响应。

```
Request → LogFilter → AuthFilter → Servlet
                                      ↓
Response ←         ←              ←
```

抽象处理者（Servlet 规范定义，无需自己写）：

```java
public interface Filter {
    void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException;
}
```

具体处理者：

```java
public class LogFilter implements Filter {

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {
        System.out.println("→ 请求到达：" + ((HttpServletRequest) request).getRequestURI());
        chain.doFilter(request, response);  // 继续传递给下一个 Filter
        System.out.println("← 响应返回");   // 响应回传时也会经过这里
    }
}
```

```java
public class AuthFilter implements Filter {

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {
        String token = ((HttpServletRequest) request).getHeader("Authorization");
        if (token == null || !isValid(token)) {
            ((HttpServletResponse) response).sendError(401, "Unauthorized");
            return;  // 中断链，不调用 chain.doFilter()
        }
        chain.doFilter(request, response);  // 鉴权通过，继续传递
    }

    private boolean isValid(String token) {
        return token.startsWith("Bearer ");
    }
}
```

`FilterChain` 的内部实现（容器负责构建，这里展示其原理）：

```java
public class ApplicationFilterChain implements FilterChain {

    private final List<Filter> filters;
    private final Servlet servlet;
    private int index = 0;

    public ApplicationFilterChain(List<Filter> filters, Servlet servlet) {
        this.filters = filters;
        this.servlet = servlet;
    }

    @Override
    public void doFilter(ServletRequest request, ServletResponse response)
            throws IOException, ServletException {
        if (index < filters.size()) {
            // 取出下一个 Filter 并调用，index 自增
            filters.get(index++).doFilter(request, response, this);
        } else {
            // 所有 Filter 执行完毕，到达 Servlet
            servlet.service(request, response);
        }
    }
}
```

Servlet Filter 链的特别之处在于，每个 Filter 既可以在请求进入时处理（`chain.doFilter()` 之前），也可以在响应返回时处理（`chain.doFilter()` 之后），形成双向包裹。

## 两种变体

**纯责任链**：请求必须被链上某个处理者处理，且只被处理一次。

**不纯责任链**：处理者处理后请求仍可继续向下传递。上面的 Servlet Filter 链就是典型——每个 Filter 都处理请求，然后调用 `chain.doFilter()` 传递给下一个。日志框架的 Appender 链也是同理。

## 优点

- **解耦发送者与接收者**：客户端只需向链头提交请求，无需知道由谁处理。
- **灵活组合处理链**：可以在运行时动态增删处理者、调整顺序。
- **符合单一职责原则**：每个处理者只关注自己负责的那一段逻辑。

## 缺点

- **请求可能不被处理**：如果链上没有合适的处理者，请求会到达链尾后被丢弃，需要额外处理。
- **调试较困难**：请求沿链传递，出现问题时需要逐个检查处理者。
- **性能影响**：链过长时，每个请求都需要遍历较长的链。

## 适用场景

- 有多个对象可以处理同一请求，且处理者在运行时才确定
- 需要在不明确指定接收者的情况下向多个对象发出请求
- 典型场景：审批流程、HTTP 中间件/Filter、日志级别过滤、事件冒泡机制

---

> 参考：<https://refactoringguru.cn/design-patterns/chain-of-responsibility>
