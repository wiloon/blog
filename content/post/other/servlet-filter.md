---
title: Servlet Filter
author: "-"
date: 2012-06-10T09:53:07+00:00
lastmod: 2026-07-01T05:27:47+08:00
url: servlet-filter
categories:
  - Java
  - Web
tags:
  - Servlet
  - java
  - remix
  - AI-assisted

aliases:
  - /p3500/
---
## Servlet Filter

`Filter` 是 Servlet 规范里的一种组件，位于容器和目标资源（Servlet/JSP）之间，可以在请求到达目标资源之前、响应离开目标资源之后做统一处理。`Filter` 本身不产生响应内容，只负责预处理和后处理，典型用途包括：

- 身份校验、权限校验
- 请求/响应日志记录
- 请求头、响应头改写
- 内容压缩、编码转换

多个 `Filter` 可以按声明顺序串成一条链（Filter Chain），这也是 [责任链模式（Chain of Responsibility）](../pattern/chain-of-responsibility-pattern.md) 在 Servlet 规范里的经典实现；Spring Security 的 [SecurityFilterChain](../language/java/spring-security.md) 就是在这套机制上封装出来的应用。

### Filter 接口

```java
public interface Filter {
    default void init(FilterConfig filterConfig) throws ServletException {
    }

    void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException;

    default void destroy() {
    }
}
```

- `init(FilterConfig)`：容器创建 `Filter` 实例后调用一次，用于读取初始化参数、保存 `FilterConfig`。
- `doFilter(request, response, chain)`：每次请求都会调用，是 `Filter` 的核心方法。
- `destroy()`：容器销毁 `Filter` 前调用一次，用于释放资源。

`FilterConfig` 提供访问 `Filter` 名称、初始化参数、`ServletContext` 的方法。

### doFilter：处理请求 + 放行链

`doFilter` 方法里可以在调用 `chain.doFilter(request, response)` 之前和之后分别插入逻辑，形成"环绕"式处理：

```java
public class LogFilter implements Filter {

    private FilterConfig filterConfig;

    @Override
    public void init(FilterConfig filterConfig) {
        this.filterConfig = filterConfig;
    }

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {
        long start = System.currentTimeMillis();

        chain.doFilter(request, response); // pass control to the next filter or target resource

        long cost = System.currentTimeMillis() - start;
        filterConfig.getServletContext()
                .log("Request to " + request.getRemoteAddr() + ": " + cost + "ms");
    }

    @Override
    public void destroy() {
    }
}
```

如果 `Filter` 想中断请求、不再往下传递（比如认证失败直接返回错误响应），只要不调用 `chain.doFilter()` 即可；这也是 Spring Security 里 `ExceptionTranslationFilter` 拦截未认证请求、直接返回 401/403 的原理。

### 请求/响应包装（Wrapper）

如果需要修改请求或响应的内容（比如统一编码、压缩响应体），可以用 `HttpServletRequestWrapper` / `HttpServletResponseWrapper` 包装原始对象，重写需要改变行为的方法，再把包装后的对象传给 `chain.doFilter()`，链上后续的 `Filter` 和目标资源拿到的就是包装后的版本。

### 配置 Filter：web.xml

传统 Servlet 应用通过 `web.xml` 声明 `Filter` 和它拦截的 URL：

```xml
<filter>
    <filter-name>logFilter</filter-name>
    <filter-class>com.example.LogFilter</filter-class>
</filter>
<filter-mapping>
    <filter-name>logFilter</filter-name>
    <url-pattern>/*</url-pattern>
</filter-mapping>
```

`filter-mapping` 决定了这个 `Filter` 拦截哪些 URL；一次请求可能匹配多个 `filter-mapping`，这些 `Filter` 会按声明顺序串成一条链，依次执行 `doFilter()`，最后才到达 `url-pattern` 对应的 Servlet。

### 现代写法：@WebFilter 与 Spring Boot

Servlet 3.0 之后可以用 `@WebFilter` 注解代替 `web.xml` 声明：

```java
@WebFilter(urlPatterns = "/*")
public class LogFilter implements Filter {
    // ...
}
```

Spring Boot 应用里更常见的做法是注册一个 `FilterRegistrationBean`：

```java
@Bean
public FilterRegistrationBean<LogFilter> logFilterRegistration() {
    FilterRegistrationBean<LogFilter> registration = new FilterRegistrationBean<>(new LogFilter());
    registration.addUrlPatterns("/*");
    return registration;
}
```

Spring Security 的 `SecurityFilterChain` 走的是另一条路径：由 `DelegatingFilterProxy` 把请求桥接到 Spring 容器管理的 `FilterChainProxy`，再由它执行一组 `Filter`，具体机制见 [Spring Security](../language/java/spring-security.md)。

## 维护记录

| 时间       | 修改内容                                                                                                                                                                                                                                                                                                                                     | 原因                                                                                                |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| 2026-07-01 | 整体重写：修正 Filter 接口方法说明（原文误写为 setFilterConfig/getFilterConfig，实际应为 init/doFilter/destroy）；修复示例 web.xml 中错误的标签闭合；补充 @WebFilter 与 Spring Boot FilterRegistrationBean 现代写法；站内链接到责任链模式与 Spring Security 文章；标题由 "Servlet.Filter" 改为 "Servlet Filter"；添加 remix/AI-assisted 标签 | 原内容存在事实错误、XML 语法错误、格式混乱（大量多余空行），且缺少现代 Servlet/Spring Boot 场景说明 |