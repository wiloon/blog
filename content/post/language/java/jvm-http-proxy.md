---
title: JVM HTTP 代理配置
author: "-"
date: 2012-07-05T06:10:33+00:00
lastmod: 2026-07-16T06:04:15+08:00
url: jvm-http-proxy
categories:
  - language
tags:
  - java
  - remix
  - AI-assisted
aliases:
  - /p3746/
---

## 概述

Java 程序访问外部 HTTP(S) 资源时，如果所在网络需要经过代理才能出网，可以通过系统属性告诉 JVM 走哪个代理，无需修改业务代码。本文整理常见的配置方式，并说明这些方式在现代 JDK（含 JDK 26）里是否依然有效。

## 经典方式：`http.proxyHost` / `http.proxyPort`

`java.net.URLConnection` 以及后来的 `java.net.http.HttpClient`（JDK 11+）在没有显式指定代理时，都会使用 `ProxySelector.getDefault()`，而默认实现会读取以下系统属性：

- `http.proxyHost` / `http.proxyPort` —— HTTP 请求走的代理
- `https.proxyHost` / `https.proxyPort` —— HTTPS 请求走的代理
- `http.nonProxyHosts` —— 不走代理的主机列表，多个主机用 `|` 分隔

这几个属性在 JDK 26 上依然是标准、有效的配置方式。

### 命令行参数

```bash
java -Dhttp.proxyHost=proxy.example.com \
     -Dhttp.proxyPort=8080 \
     -Dhttps.proxyHost=proxy.example.com \
     -Dhttps.proxyPort=8080 \
     -jar app.jar
```

### 代码里设置系统属性

```java
// Must be set before the first network call is made
System.setProperty("http.proxyHost", "proxy.example.com");
System.setProperty("http.proxyPort", "8080");
```

不要把代理地址硬编码在源码里，建议从配置文件读取。

### Tomcat：catalina.properties

追加到 `${CATALINA_HOME}/conf/catalina.properties`：

```properties
http.proxyHost=proxy.example.com
http.proxyPort=8080
```

### Tomcat：catalina.sh / catalina.bat

```bash
JAVA_OPTS="-Dhttp.proxyHost=proxy.example.com -Dhttp.proxyPort=8080"
```

多个参数之间用空格分隔。

## 代理认证：一个常见误区

设置 `http.proxyUser` / `http.proxyPassword` 即可完成代理认证是一个流传很广但从来不成立的说法——JDK 内置的 `URLConnection` 和 `HttpClient` 都不会读取这两个属性来自动做代理认证（除非应用自己读取并处理它们）。正确做法是注册一个 `Authenticator`：

```java
Authenticator.setDefault(new Authenticator() {
    @Override
    protected PasswordAuthentication getPasswordAuthentication() {
        return new PasswordAuthentication(
            "someUserName", "somePassword".toCharArray());
    }
});
```

同理，`System.getProperties().put("proxySet", "true")` 是 Java 1.3 之前遗留的属性，早已废弃，现代 JDK 既不需要也不识别，可以直接忽略。

## JDK 8u111+ 的一个安全限制

从 JDK 8u111 开始，出于安全考虑，默认**禁止**通过 HTTPS 隧道（`CONNECT`）使用 Basic 方式做代理认证。如果确实需要，要显式清空这个系统属性：

```bash
-Djdk.http.auth.tunneling.disabledSchemes=
```

这是配置代理认证时很容易踩坑的一点。

## JDK 11+：HttpClient 里显式指定代理

新的 `java.net.http.HttpClient` 除了会读取上面的系统属性外，也支持在代码里显式指定 `ProxySelector`，更适合同一进程内需要区分多套代理的场景，不依赖容易互相污染的全局系统属性：

```java
HttpClient client = HttpClient.newBuilder()
    .proxy(ProxySelector.of(new InetSocketAddress("proxy.example.com", 8080)))
    .authenticator(Authenticator.getDefault())
    .build();
```

## 小结

- `http.proxyHost` / `http.proxyPort` / `https.proxyHost` / `https.proxyPort` 这几个系统属性在 JDK 26 上依然有效，是最简单的全局配置方式。
- `http.proxyUser` / `http.proxyPassword` / `proxySet` 从一开始就不是 JDK 会自动识别的属性，代理认证要用 `Authenticator.setDefault(...)`。
- HTTPS 隧道下的 Basic 代理认证默认被禁用（JDK 8u111+），需要时要显式打开 `jdk.http.auth.tunneling.disabledSchemes`。
- 新代码优先用 `java.net.http.HttpClient` + 显式 `ProxySelector`，避免全局系统属性带来的相互干扰。

原文（2007）：<http://i4t.org/2007/05/04/java-http-proxy-settings/>

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-07-16 | 重写全文；标题改为「JVM HTTP 代理配置」；categories 由 `Java` 改为 `language`；纠正 `http.proxyUser`/`http.proxyPassword`/`proxySet` 的错误说法，补充 `https.proxyHost`、JDK 8u111+ 隧道认证限制、`HttpClient` 显式 `ProxySelector` 等现代 JDK 内容 | 原文是 2007 年的转载，部分说法在 JDK 时代已过时或本身就是误导；用户要求整理并更新为现代 Java（JDK 26）适用的内容 |