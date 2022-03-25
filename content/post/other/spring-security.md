---
title: spring security 拦截器
author: "-"
date: 2011-11-20T09:10:54+00:00
url: spring
categories:
  - spring
tags:
  - spring

---
## spring security 拦截器
1、ChannelProcessingFilter，使用它因为我们可能会指向不同的协议(如:Http,Https)

2、SecurityContextPersistenceFilter，负责从SecurityContextRepository 获取或存储 SecurityContext。SecurityContext 代表了用户安全和认证过的session

3、ConcurrentSessionFilter,使用SecurityContextHolder的功能，更新来自“安全对象”不间断的请求,进而更新SessionRegistry

4、认证进行机制，UsernamePasswordAuthenticationFilter，CasAuthenticationFilter，BasicAuthenticationFilter等等--SecurityContextHolder可能会修改含有Authentication这样认证信息的token值

5、SecurityContextHolderAwareRequestFilter,如果你想用它的话，需要初始化spring security中的HttpServletRequestWrapper到你的servlet容器中。

6、JaasApiIntegrationFilter，如果JaasAuthenticationToken在SecurityContextHolder的上下文中，在过滤器链中JaasAuthenticationToken将作为一个对象。

7. RememberMeAuthenticationFilter, 如果还没有新的认证程序机制更新SecurityContextHolder，并且请求已经被一个“记住我”的服务替代，那么将会有一个Authentication对象将存放到这 (就是 已经作为cookie请求的内容）。

8、AnonymousAuthenticationFilter，如果没有任何认证程序机制更新SecurityContextHolder，一个匿名的对象将存放到这。

9、ExceptionTranslationFilter，为了捕获spring security的错误，所以一个http响应将返回一个Exception或是触发AuthenticationEntryPoint。

10、FilterSecurityInterceptor，当连接被拒绝时，保护web URLS并且抛出异常。
