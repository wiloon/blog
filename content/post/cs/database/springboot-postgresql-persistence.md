---
title: Spring Boot + PostgreSQL 持久层框架
author: "-"
date: 2026-04-25T11:12:01+08:00
url: springboot-postgresql-persistence
categories:
  - development
tags:
  - java
  - spring-boot
  - postgresql
  - jpa
  - mybatis
  - remix
  - AI-assisted
---

## 主流持久层框架

### Spring Data JPA + Hibernate

- Spring Boot 默认推荐，依赖 `spring-boot-starter-data-jpa`
- ORM 框架，用注解映射对象和表
- 自动生成 SQL，支持 JPQL / Criteria API
- 适合领域模型复杂的场景

### MyBatis / MyBatis-Plus

- 半自动 ORM，SQL 写在 XML 或注解中
- 对 SQL 控制力强，适合复杂查询
- MyBatis-Plus 提供代码生成、分页等增强功能

### JOOQ

- 类型安全的 SQL DSL，SQL 风格写法
- 编译期检查 SQL，适合喜欢写 SQL 的团队
- 商业数据库需付费版

### Spring Data JDBC

- 比 JPA 更轻量，无懒加载、缓存等复杂特性
- SQL 更透明，适合简单 CRUD

### R2DBC（响应式）

- 非阻塞响应式驱动，配合 WebFlux 使用
- 依赖 `spring-boot-starter-data-r2dbc`

## 选型建议

| 场景 | 推荐 |
|------|------|
| 快速开发，标准 CRUD | Spring Data JPA |
| 复杂 SQL，精细控制 | MyBatis-Plus |
| 强类型 SQL，重查询业务 | JOOQ |
| 响应式架构 | R2DBC |

---

## 连接池

Spring Boot 默认使用 **HikariCP** 作为连接池。

### 技术层次

```
Spring Data JPA
    └── Hibernate (ORM)
        └── JDBC DataSource
            └── HikariCP (连接池)
                └── PostgreSQL JDBC Driver (pgjdbc)
```

### 依赖说明

`spring-boot-starter-data-jpa` 会自动引入 `spring-boot-starter-jdbc`，后者包含 HikariCP。

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>
<dependency>
    <groupId>org.postgresql</groupId>
    <artifactId>postgresql</artifactId>
</dependency>
```

HikariCP 由 `com.zaxxer:HikariCP` 提供，Spring Boot 2.x 起设为默认连接池，以高性能著称。

### 常用配置

```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/mydb
    username: user
    password: pass
    hikari:
      maximum-pool-size: 10
      minimum-idle: 5
      connection-timeout: 30000
      idle-timeout: 600000
```

也可以替换为 **Druid**、**c3p0** 等其他连接池，但通常 HikariCP 已满足需求。

---

## HikariCP 详解

**HikariCP**（Hikari = 日语"光"）是目前 Java 生态中性能最好的 JDBC 连接池，由 Brett Wooldridge 开发，2012 年开源。

### 核心特点

- **极致性能**：基准测试中比 c3p0、DBCP、Tomcat Pool、Druid 快数倍，延迟极低
- **轻量**：JAR 包约 150KB，代码量极少
- **零开销设计**：使用 `FastList` 替代 `ArrayList`，字节码级别优化，避免反射
- **稳定可靠**：Spring Boot 2.x 起设为默认连接池，经过大规模生产验证
- **连接健康检查**：自动剔除失效连接，支持 `connectionTestQuery` 或 JDBC4 的 `isValid()`

### 关键配置参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `maximum-pool-size` | 10 | 连接池最大连接数 |
| `minimum-idle` | 同 maximum | 最小空闲连接数 |
| `connection-timeout` | 30000ms | 获取连接的最大等待时间 |
| `idle-timeout` | 600000ms | 空闲连接的最长存活时间 |
| `max-lifetime` | 1800000ms | 连接的最长生命周期（必须小于数据库超时时间） |
| `keepalive-time` | 0（禁用） | 心跳检测间隔，防止连接被防火墙断开 |

### 与其他连接池对比

| 连接池 | 性能 | 功能 | 常见场景 |
|--------|------|------|----------|
| **HikariCP** | ⭐⭐⭐⭐⭐ | 简洁 | Spring Boot 默认 |
| **Druid** | ⭐⭐⭐⭐ | 丰富（监控、SQL 拦截） | 国内企业项目 |
| **c3p0** | ⭐⭐ | 一般 | 老项目遗留 |
| **DBCP2** | ⭐⭐⭐ | 一般 | Apache 项目 |

Druid 在国内使用广泛，主要因为它提供了内置的 SQL 监控面板和慢查询统计功能，HikariCP 则在纯性能上更优。

---

## max-lifetime：连接的定期轮换机制

`max-lifetime` 设置连接池中**每个连接从创建起能存活的最长时间**（默认 30 分钟），到期后无论是否空闲都会被强制关闭并替换为新连接。

### 为什么需要它

数据库和网络设备通常会主动断开长时间存在的连接：

- PostgreSQL 的 `tcp_keepalives_idle` 或防火墙会静默断开长连接
- 云数据库（RDS、Cloud SQL 等）一般有连接最大存活时间限制
- 数据库重启后，连接池里的老连接已失效但应用侧不知道

如果不设置 `max-lifetime`，连接可能在"看起来正常"的状态下实际已被数据库端断开，导致执行 SQL 时报 **broken pipe** 或 **connection reset** 错误。

### 工作方式

HikariCP 会在后台跟踪每个连接的创建时间，当某个连接的年龄接近 `max-lifetime` 时：

- **连接空闲中**：立即关闭，补充新连接
- **连接正在被使用**：等它执行完 SQL 归还到池后，再关闭并补充新连接

为避免所有连接同时到期（雪崩），HikariCP 会在 `max-lifetime` 基础上加一个随机偏移（±2.5%），让各连接的到期时间错开。

```
t=0       连接 A、B、C 全部创建
t=30min   连接 A 到期（空闲）→ 立即关闭，新建连接 A'
t=30.5min 连接 B 到期（使用中）→ 等 SQL 完成后关闭，新建 B'
t=31min   连接 C 到期 → 关闭，新建 C'
...（循环往复）
```

即使**完全没有业务请求**，只要连接池在运行，`max-lifetime` 就会驱动连接定期轮换，保持连接池中的连接始终是"新鲜"的。

### 关键建议

`max-lifetime` **必须小于数据库的连接超时时间**，否则数据库先断开连接，应用拿到的是一个死连接。

例如 PostgreSQL 服务端配置了 `idle_in_transaction_session_timeout = 1800000ms`，则 `max-lifetime` 应设为约 `1750000ms`，留出余量。

## 多服务共用同一数据库，只有一个服务报连接 timeout

> 其它服务业务正常，只有一个服务日志里大量 connection timeout，可能是什么问题，怎么排查？

**可能原因**：

1. **连接池耗尽**：该服务的连接池 `maximumPoolSize` 配置过小，或存在连接泄漏（Connection Leak），连接没有被正确归还，导致后续请求无法获取连接而超时
2. **慢查询/长事务占用连接**：该服务存在执行时间很长的 SQL 或未提交的事务，连接长时间被占用，新请求排队等待超时
3. **线程池与连接池不匹配**：业务线程数远大于连接池大小，高并发时大量线程争抢连接
4. **连接泄漏**：代码里 `Connection` / `ResultSet` / `Statement` 没有在 finally 块或 try-with-resources 中关闭

**排查步骤**：

1. **查连接池监控指标**：观察 `activeConnections`、`pendingThreads`、`idleConnections`，判断是否池满
2. **查数据库侧**：`SHOW PROCESSLIST`（MySQL）查看该服务来源的连接数及是否有大量 Sleep/长时间运行的查询
3. **查慢查询日志**：确认是否有特定 SQL 执行时间异常
4. **排查连接泄漏**：开启连接池的 `leakDetectionThreshold`（HikariCP），超时未归还的连接会打印堆栈
5. **对比配置**：对比该服务与正常服务的连接池参数（`maximumPoolSize`、`connectionTimeout`）是否有差异
6. **查应用日志**：确认 timeout 发生的时间规律，是否与某个定时任务或流量高峰吻合
