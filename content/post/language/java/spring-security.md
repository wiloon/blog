---
title: Spring Security
author: "-"
date: 2020-12-23T20:22:56+08:00
lastmod: 2026-07-01T05:27:47+08:00
url: spring-security
categories:
  - java
tags:
  - java
  - spring
  - spring security
  - authentication
  - remix
  - AI-assisted
---

## SecurityFilterChain

`SecurityFilterChain` 是 Spring Security 的核心抽象，代表一条作用于 HTTP 请求的**安全过滤器链**。每个进入应用的请求都会依次经过链中的若干 `Filter`，完成认证（Authentication）、授权（Authorization）、CSRF 防护、会话管理等工作。

### 底层机制：从 Servlet Filter 到 Spring Security

Servlet 规范本身有 [`Filter` 接口和 `FilterChain` 接口](../../other/servlet-filter.md)。Spring Security 通过以下两层代理接入这套机制：

1. **`DelegatingFilterProxy`**：在 Servlet 容器（Tomcat）层面注册的 `Filter`，作用是把请求桥接到 Spring 容器中的 Bean。它本身不做安全逻辑，只是一个"入口代理"。
2. **`FilterChainProxy`**：Spring 容器中的真正实现，也是一个特殊的 `Filter`。它持有所有注册的 `SecurityFilterChain` Bean，收到请求后，按顺序匹配第一条能处理该 URL 的链，然后依次执行链中的每个 `Filter`。

```
HTTP 请求
  → Tomcat FilterChain
    → DelegatingFilterProxy（Servlet Filter，桥接到 Spring，Bean 名固定为 springSecurityFilterChain）
      → FilterChainProxy（Spring Bean，收集所有 SecurityFilterChain）
        → SecurityFilterChain 1（匹配 /api/**）
            UsernamePasswordAuthenticationFilter
            BearerTokenAuthenticationFilter
            ExceptionTranslationFilter
            AuthorizationFilter
            ...
        → SecurityFilterChain 2（匹配 /**）
            ...
      ← 链中最后一个 Filter 放行（chain.doFilter()），控制权交回 DelegatingFilterProxy
  → Tomcat FilterChain 继续执行其余 Filter（如果有）
    → DispatcherServlet
      → HandlerMapping 找到目标 Controller 方法
        → Controller
```

### SecurityFilterChain Bean 如何被收集并接入请求

在 `@Configuration` 类里写的 `@Bean public SecurityFilterChain filterChain(...)` 方法，只是往 IoC 容器里注册了一个数据对象——具体实现类是 `DefaultSecurityFilterChain`，内部就是一个 `Filter` 列表加一个 `RequestMatcher`。真正让这份数据接入请求处理流程，还需要另外两步：

1. Spring Boot 的自动配置（`SecurityFilterAutoConfiguration`）会创建一个 `FilterChainProxy` Bean，构造时把容器里所有 `SecurityFilterChain` 类型的 Bean 都收集起来（可以有多个，用 `@Order` 排优先级），并以固定 Bean 名 `springSecurityFilterChain` 注册。
2. `DelegatingFilterProxy` 是在 Servlet 容器层面注册的真正 `Filter`，它按名字 `springSecurityFilterChain` 到 Spring 容器里查找对应的 Bean（也就是上一步的 `FilterChainProxy`），把每个进来的请求都转发给它处理。

所以一次请求要先经过 Tomcat 的 Filter 链，被 `DelegatingFilterProxy` 接住转发给 `FilterChainProxy`；`FilterChainProxy` 用 `matches()` 找到第一条匹配的 `SecurityFilterChain`，取出这条链的 `Filter` 列表逐个执行。认证、授权都通过后，链上最后一个 `Filter` 调用 `chain.doFilter()` 放行，请求才会继续往下走，最终到达 `DispatcherServlet` 并路由到 `Controller` 方法；一旦某个 `Filter` 判定失败（比如未认证），会直接短路返回响应（401/403），请求根本不会到达 `Controller`。

### 定义一个 SecurityFilterChain

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain apiSecurityChain(HttpSecurity http) throws Exception {
        http
            .securityMatcher("/api/**")           // 只匹配 /api/** 路径
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/public/**").permitAll()
                .anyRequest().authenticated()
            )
            .sessionManagement(session -> session
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS)  // 无状态，适合 JWT
            )
            .csrf(csrf -> csrf.disable());        // REST API 通常关闭 CSRF

        return http.build();
    }
}
```

`HttpSecurity` 是 `SecurityFilterChain` 的构建器，调用 `.build()` 后生成链实例并注册为 Bean。

### 多条链：按 URL 区分安全策略

可以注册多个 `SecurityFilterChain` Bean，用 `@Order` 控制优先级（数字越小越优先）。`FilterChainProxy` 会用第一条匹配的链处理请求，后续链不再参与。

```java
@Bean
@Order(1)                              // 优先级更高
public SecurityFilterChain apiChain(HttpSecurity http) throws Exception {
    http
        .securityMatcher("/api/**")
        .authorizeHttpRequests(auth -> auth.anyRequest().authenticated())
        .httpBasic(Customizer.withDefaults());
    return http.build();
}

@Bean
@Order(2)
public SecurityFilterChain webChain(HttpSecurity http) throws Exception {
    http
        .authorizeHttpRequests(auth -> auth
            .requestMatchers("/login", "/css/**").permitAll()
            .anyRequest().authenticated()
        )
        .formLogin(Customizer.withDefaults());
    return http.build();
}
```

多条 `SecurityFilterChain` 之间是**互斥的**，不是首尾相连、逐条执行：一次请求按 URL 分流，只会命中第一条 `securityMatcher` 匹配的链，其余链完全不参与这次请求。请求一旦流到某一条被选中的链上，才会依次流过这条链里的**每一个** `Filter`——只要没有 `Filter` 中途拦截（比如未认证被短路返回 401），就会在链尾放行，继续走到 `DispatcherServlet` 和 `Controller`。

### 链中的关键内置 Filter

| Filter                                 | 作用                                                   |
| -------------------------------------- | ------------------------------------------------------ |
| `SecurityContextHolderFilter`          | 加载/保存 `SecurityContext`（当前用户信息）            |
| `UsernamePasswordAuthenticationFilter` | 处理表单登录（`POST /login`）                          |
| `BearerTokenAuthenticationFilter`      | 处理 JWT/OAuth2 Bearer Token                           |
| `ExceptionTranslationFilter`           | 将认证/授权异常转换为 HTTP 401/403 响应                |
| `AuthorizationFilter`                  | 最终的权限校验（替代旧的 `FilterSecurityInterceptor`） |
| `CsrfFilter`                           | CSRF Token 校验                                        |
| `CorsFilter`                           | 处理跨域预检请求                                       |

### 与 GoF 设计模式的关系

`SecurityFilterChain`（以及底层 Servlet `Filter`/`FilterChain` 机制）最贴近 GoF 的 [责任链模式（Chain of Responsibility）](../../pattern/chain-of-responsibility-pattern.md)：

```java
public interface Filter {
    void doFilter(ServletRequest request, ServletResponse response, FilterChain chain);
}
```

- 每个 `Filter` 拿到的 `FilterChain` 就是"指向下一个处理者的引用"。
- `chain.doFilter(request, response)` 就是"转交给下一个处理者"的动作。
- 调用者（`FilterChainProxy`）不需要知道链里具体有多少个、哪些 `Filter`，只管触发第一个，后续完全由链自己传递——这正是责任链模式"发起者与处理者解耦"的意图。

不完全严格的地方在于：GoF 经典责任链通常是"某一个处理者处理后就终止"（比如异常处理链，谁能处理谁就截胡），而 Servlet Filter 更常见的用法是环绕式——`doFilter` 在调用 `chain.doFilter()` 之前和之后都能插入逻辑（比如 `ExceptionTranslationFilter` 在调用链后半段捕获异常），这种"前置 + 调用下一个 + 后置"的写法带了一点装饰器模式（Decorator）的味道。但从"谁触发下一个"这个结构本质上看，还是责任链，装饰器更多是从"层层包装、增强职责"的角度补充解释，不影响结论。

### permitAll、authenticated、hasRole

`authorizeHttpRequests` 中的规则从上到下**第一条匹配即生效**，顺序很重要：

```java
http.authorizeHttpRequests(auth -> auth
    .requestMatchers("/public/**").permitAll()          // 公开访问
    .requestMatchers("/admin/**").hasRole("ADMIN")      // 需要 ADMIN 角色
    .requestMatchers("/user/**").hasAnyRole("USER", "ADMIN")
    .anyRequest().authenticated()                       // 其余需要登录
);
```

`hasRole("ADMIN")` 等价于 `hasAuthority("ROLE_ADMIN")`——Spring Security 约定角色名在存储时带 `ROLE_` 前缀，`hasRole` 会自动补充。

---

## 认证流程：Filter、AuthenticationManager、UserDetailsService 的职责划分

一次完整的表单登录认证，会依次经过三层职责不同的组件：`Filter` 负责触发和收尾、`AuthenticationManager` 负责调度、`UserDetailsService` 负责加载用户数据。下面用 [comments-tree](https://github.com/wiloon/comments-tree) 项目里真实的 `SecurityConfig` 来说明每一层具体做了什么。

### 整体链路

```text
POST /session (nameOrEmail + password)
  -> UsernamePasswordAuthenticationFilter (generated from formLogin config)
    -> AuthenticationManager.authenticate(token)
      -> ProviderManager delegates to DaoAuthenticationProvider
        -> UserDetailsService.loadUserByUsername(nameOrEmail)
        -> PasswordEncoder.matches(rawPassword, encodedPassword)
      <- returns authenticated Authentication
  -> written into SecurityContext
  -> AuthenticationSuccessHandler / AuthenticationFailureHandler
```

### Filter：入口与出口

comments-tree 用 `formLogin` 配置表单登录，Spring Security 在背后生成 `UsernamePasswordAuthenticationFilter`，拦截 `/session` 上的 POST 请求：

```java
@Bean
public SecurityFilterChain filterChain(HttpSecurity httpSecurity) throws Exception {
    httpSecurity
            .authorizeHttpRequests(auth -> auth
                    .requestMatchers(HttpMethod.POST, "/session").permitAll()
                    .requestMatchers(HttpMethod.GET, "/session").permitAll()
                    .anyRequest().authenticated()
            )
            .exceptionHandling(ex -> ex
                    .accessDeniedHandler(restfulAccessDeniedHandler())
                    .authenticationEntryPoint(restAuthenticationEntryPoint())
            )
            .formLogin(form -> form
                    .loginProcessingUrl("/session")
                    .usernameParameter("nameOrEmail")
                    .successHandler(loginAuthenticationSuccessHandler())
                    .failureHandler(formLoginFailedHandler())
            );

    return httpSecurity.build();
}
```

Filter 层的职责有两块：

- **触发认证**：从请求里取出 `nameOrEmail` 和 `password`，封装成未认证的 `UsernamePasswordAuthenticationToken`，转交给 `AuthenticationManager`。
- **收尾与异常翻译**：认证结果出来后，Filter 决定调用 `AuthenticationSuccessHandler` 还是 `AuthenticationFailureHandler`；未登录访问受保护资源时，由 `ExceptionTranslationFilter` 调用 `AuthenticationEntryPoint`（对应 comments-tree 的 `RestAuthenticationEntryPoint`，返回 401）；已登录但权限不足时调用 `AccessDeniedHandler`（`RestfulAccessDeniedHandler`，返回 403）。

Filter 本身不做用户查找和密码比对，这部分工作全部委托出去。

### AuthenticationManager：只做调度，不做校验

```java
@Bean
public AuthenticationManager authenticationManager(AuthenticationConfiguration config) throws Exception {
    return config.getAuthenticationManager();
}
```

comments-tree 没有自定义 `AuthenticationProvider`，直接用 `AuthenticationConfiguration` 拿到 Spring Boot 组装好的 `ProviderManager`。`ProviderManager` 内部维护一组 `AuthenticationProvider`，收到 `UsernamePasswordAuthenticationToken` 后，找到能处理这个 Token 类型的 `DaoAuthenticationProvider`，把认证工作转交给它。

`AuthenticationManager` 的职责因此很单一：接收未认证的 `Authentication`，选择合适的 `Provider`，返回认证结果（成功则是已认证的 `Authentication`，失败抛 `AuthenticationException`）。它自己不知道密码是怎么存的，也不知道用户数据从哪来。

### UserDetailsService：只管加载数据，不管比对密码

```java
@Service
public class UserService implements UserDetailsService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    @Override
    public UserDetails loadUserByUsername(String nameOrEmail) throws UsernameNotFoundException {
        User user = getUserByNameOrEmail(nameOrEmail);
        if (user == null) {
            throw new UsernameNotFoundException("User not found: " + nameOrEmail);
        }
        return new CommentsTreeUserDetails(user);
    }

    public User getUserByNameOrEmail(String nameOrEmail) {
        if (Utils.isEmail(nameOrEmail)) {
            return getUserByEmail(nameOrEmail);
        }
        return getUserByName(nameOrEmail);
    }
}
```

`UserService` 同时承担业务层（注册、查询用户）和 `UserDetailsService` 两个角色。`loadUserByUsername` 支持用户名或邮箱两种方式登录，查不到人直接抛 `UsernameNotFoundException`，这是 `UserDetailsService` 唯一的契约方法。

密码比对不在这里发生。`DaoAuthenticationProvider` 拿到 `loadUserByUsername` 返回的 `UserDetails`（内部含 BCrypt 加密后的密码）后，自己调用 `PasswordEncoder.matches(rawPassword, userDetails.getPassword())` 做比对，一致才算认证通过。

### PasswordEncoder 为什么单独抽出一个 Configuration

```java
@Configuration
public class PasswordEncoderConfig {

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}
```

`UserService` 的构造函数需要注入 `PasswordEncoder`（用于注册时哈希密码），而 `PasswordEncoder` 这个 Bean 原本是在 `SecurityConfig` 里定义的。如果放在一起，会形成 `SecurityConfig -> UserService（构造参数）-> PasswordEncoder（SecurityConfig 里定义）` 的循环依赖。把 `PasswordEncoder` 单独抽成一个 `@Configuration` 类，让两边都依赖这个更小的配置类，就消掉了这个环。

### 三者职责小结

| 组件                                                         | 职责                                                         | 不做的事                             |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------ |
| `Filter`（`UsernamePasswordAuthenticationFilter`）           | 从请求提取凭证、触发认证、处理认证结果（成功/失败/异常翻译） | 不查用户、不比对密码                 |
| `AuthenticationManager`（`ProviderManager`）                 | 调度合适的 `AuthenticationProvider`，返回认证结果            | 不知道用户数据来源、不知道密码怎么存 |
| `UserDetailsService`（`UserService`）                        | 根据用户名/邮箱加载 `UserDetails`                            | 不做密码比对                         |
| `PasswordEncoder`（在 `DaoAuthenticationProvider` 内部使用） | 比对明文密码与加密密码                                       | 不参与用户查找                       |

这套划分本质上是单一职责原则的体现：账号来源变化（比如接入 LDAP）只需要换 `UserDetailsService` 的实现，认证方式变化（比如接入 OAuth2）只需要加新的 `AuthenticationProvider`，Filter 和调度逻辑都不用动。

## Remember Me

comments-tree 还开启了 `rememberMe`，用持久化令牌（`PersistentTokenRepository`）实现跨设备的登录状态失效控制，详见独立文章 [Spring Security Remember Me 实现机制](../../other/remember-me.md)。

## 维护记录

| 时间       | 修改内容                                                                                                                                                                                                                                                                                     | 原因                                                                                          |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| 2026-07-01 | 新增「认证流程：Filter、AuthenticationManager、UserDetailsService 的职责划分」章节，结合 comments-tree 项目真实的 SecurityConfig/UserService/PasswordEncoderConfig 代码说明各组件职责                                                                                                        | 面试准备时整理认证流程知识点，补充真实项目案例                                                |
| 2026-07-01 | 删除「authorizeRequests（旧 API）」「spring security」（含语法错误的 pom.xml、`.authorizeRequests()` 旧写法、过时 PlantUML 类图、掘金/简书转载内容）以及「spring security 拦截器」（含已被 6.x 替换的 `SecurityContextPersistenceFilter`、`FilterSecurityInterceptor` 等旧 Filter 列表）三节 | 内容过时、与前文已更新的 6.x 说明矛盾，且转载内容与 remix 标签定性不符                        |
| 2026-07-01 | 在「链中的关键内置 Filter」后新增「与 GoF 设计模式的关系」小节，说明 `SecurityFilterChain` 对应责任链模式，并站内链接到 [责任链模式](../../pattern/chain-of-responsibility-pattern.md)                                                                                                       | 补充设计模式视角，关联站内已有的责任链模式文章                                                |
| 2026-07-01 | 补充「SecurityFilterChain Bean 如何被收集并接入请求」小节，说明 `@Bean` 注册的 `SecurityFilterChain` 如何被 `FilterChainProxy` 收集、`DelegatingFilterProxy` 按 Bean 名桥接，并更新调用链图补充到 `DispatcherServlet`/`Controller` 的走向                                                    | 说明请求先经过 SecurityFilterChain 才到达 Controller 的完整机制                               |
| 2026-07-01 | 「底层机制」段落站内链接到 [Servlet Filter](../../other/servlet-filter.md)；「多条链」一节补充说明多个 SecurityFilterChain 互斥（按 URL 分流，只命中一条），命中的链上会依次流过每一个 Filter                                                                                                | 澄清多条 SecurityFilterChain 之间是互斥关系而非串联，避免与责任链模式内部 Filter 顺序执行混淆 |
| 2026-07-01 | 新增「Remember Me 实现机制」章节，对比简单哈希令牌与 `PersistentTokenRepository` 两种实现，结合 comments-tree 的 `JdbcTokenRepositoryImpl` 配置说明跨设备失效控制的原理                                                                                                                      | 面试准备时整理 remember-me 机制与跨设备失效控制概念                                           |
| 2026-07-01 | 「Remember Me」章节内容拆分为独立文章 [Spring Security Remember Me 实现机制](../../other/remember-me.md)，本文只保留一行引用                                                                                                                                                                 | 内容改写为独立文档，避免两篇文章重复维护同一份内容                                            |
