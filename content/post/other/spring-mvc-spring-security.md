---
title: spring security
author: "-"
date: 2014-04-29T03:45:23+00:00
url: /?p=6567
categories:
  - inbox
tags:
  - reprint
---
## spring security

### spring-security-jwt-guide

[https://github.com/Snailclimb/spring-security-jwt-guide](https://github.com/Snailclimb/spring-security-jwt-guide)

spring-boot-starter-data-redis
基础依赖，其他依赖根据使用不同的缓存技术选择加入，默认情况下使用 ConcurrentMapCache不需要引用任何依赖

spring-boot-starter-data-redis
spring-boot-starter-data-redis依赖于spring-data-redis 和 lettuce 。Spring Boot 1.0 默认使用的是 Jedis 客户端，2.0 替换成 Lettuce，但如果你从 Spring Boot 1.5.X 切换过来，几乎感受不大差异，这是因为 spring-boot-starter-data-redis 为我们隔离了其中的差异性。

spring-boot-starter-thymeleaf
Thymeleaf 是新一代的模板引擎，在 Spring4.0 中推荐使用 Thymeleaf 来做前端模版引擎。

add maven dependancy

HttpSessionSecurityContextRepository.loadContext

### spring security session serialize json redis

[https://github.com/spring-projects/spring-session/issues/933](https://github.com/spring-projects/spring-session/issues/933)
[https://github.com/spring-projects/spring-session/blob/2.3.1.RELEASE/spring-session-samples/spring-session-sample-boot-redis-json/src/main/java/sample/config/SessionConfig.java](https://github.com/spring-projects/spring-session/blob/2.3.1.RELEASE/spring-session-samples/spring-session-sample-boot-redis-json/src/main/java/sample/config/SessionConfig.java)
---

[https://my.oschina.net/u/3669799/blog/4282404](https://my.oschina.net/u/3669799/blog/4282404)
[https://blog.csdn.net/wamr_o/article/details/99634226](https://blog.csdn.net/wamr_o/article/details/99634226)
[https://github.com/Ceruleans/ssdemo](https://github.com/Ceruleans/ssdemo)
[https://my.oschina.net/u/4257408/blog/3662569](https://my.oschina.net/u/4257408/blog/3662569)

---

```xml

<dependency>
  
<groupId>org.springframework</groupId>
  
spring-core</artifactId>
  
<version>3.2.8.RELEASE</version>
  
</dependency>

<dependency>
  
<groupId>org.springframework</groupId>
  
spring-context</artifactId>
  
<version>3.2.8.RELEASE</version>
  
</dependency>
  
<dependency>
  
<groupId>org.springframework</groupId>
  
spring-web</artifactId>
  
<version>3.2.8.RELEASE</version>
  
</dependency>

```

add dispatcher servlet in web.xml

```xml

<servlet>
  
<servlet-name>springDispatcherServlet</servlet-name>
  
<servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
  
<init-param>
  
<param-name>contextConfigLocation</param-name>
  
<param-value>classpath:spring-servlet.xml</param-value>
  
</init-param>
  
<load-on-startup>1</load-on-startup>
  
</servlet>
  
<servlet-mapping>
  
<servlet-name>springDispatcherServlet</servlet-name>
  
<url-pattern>/</url-pattern>
  
</servlet-mapping>

```

---

[http://www.cnblogs.com/Beyond-bit/p/SpringMVC_And_SpringSecurity.html](http://www.cnblogs.com/Beyond-bit/p/SpringMVC_And_SpringSecurity.html)
>[https://mp.weixin.qq.com/s/z6GeR5O-vBzY3SHehmccVA](https://mp.weixin.qq.com/s/z6GeR5O-vBzY3SHehmccVA)
