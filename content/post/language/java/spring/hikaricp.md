---
title: "HikariCP: 连接池参数与泄漏排查"
author: "-"
date: 2026-07-02T05:28:21+08:00
lastmod: 2026-07-02T05:28:21+08:00
url: hikaricp
categories:
  - Java
tags:
  - java
  - spring-boot
  - hikaricp
  - database
  - remix
  - AI-assisted
---

HikariCP 是 Spring Boot 2.x 及以上版本的默认数据库连接池，`spring-boot-starter-jdbc`／`spring-boot-starter-data-jpa` 在类路径上检测到它时会自动创建对应的 `DataSource`，见 [spring-boot-relational-persistence.md](./spring-boot-relational-persistence.md)。

## 核心设计取向

HikariCP 相比 DBCP、C3P0 等老连接池，主打「轻量、少锁竞争」：连接获取路径尽量避免同步阻塞，字节码层面做了不少微优化（如去掉不必要的包装类）。这也是它成为默认选型的主要原因——同等硬件下吞吐更高、延迟更低。

## 关键参数

| 参数                     | 作用                           | 建议                                                                                                                           |
| ------------------------ | ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| `maximumPoolSize`        | 连接池最大连接数               | 不是越大越好，经验公式 `连接数 = (核心数 * 2) + 有效磁盘数`；通常 10-20 已足够，过大会导致数据库端连接争用、上下文切换开销上升 |
| `minimumIdle`            | 最小空闲连接数                 | 建议和 `maximumPoolSize` 设成一致，避免连接数动态伸缩带来的抖动（官方推荐固定池大小）                                          |
| `connectionTimeout`      | 从池中获取连接的等待超时       | 默认 30s，业务上一般调到 3-5s，超时快速失败优于线程一直阻塞                                                                    |
| `idleTimeout`            | 空闲连接被回收前的最长空闲时间 | 默认 10 分钟，仅在 `minimumIdle < maximumPoolSize` 时生效                                                                      |
| `maxLifetime`            | 连接最大生命周期               | 默认 30 分钟，必须比数据库或负载均衡器的连接超时（如 MySQL `wait_timeout`）短，否则会用到已被服务端关闭的连接                  |
| `leakDetectionThreshold` | 连接泄漏检测阈值               | 默认 0（关闭）；生产建议设 30000-60000ms，超过该时间连接还未归还池会打印 WARN 日志和借出时的调用栈                             |

`application.yml` 配置示例：

```yaml
spring:
  datasource:
    hikari:
      maximum-pool-size: 15
      minimum-idle: 15
      connection-timeout: 3000
      max-lifetime: 1500000
      leak-detection-threshold: 60000
```

## maxLifetime 为什么防不住连接泄漏

容易有的误解是：既然配了 `maxLifetime`，超时的连接应该会被自动回收，不会一直泄漏下去。实际上 `maxLifetime` 只对**归还回池中的空闲连接**生效，对**被业务代码借出、一直没有 `close()` 的连接**不生效。

原因是 HikariCP 不会在连接**正在被使用**时强行关闭它——如果这么做，业务代码手里的 `Connection` 对象会突然失效，直接抛 `SQLException`，比泄漏本身更危险。所以 `maxLifetime` 的检查时机是"连接被归还到池的那一刻"（即 `connection.close()` 触发），不是一个后台定时器主动去清理正在使用中的连接。

如果业务代码是这样：

```java
Connection conn = dataSource.getConnection();
// exception thrown here, no finally block to close()
doSomething(conn);
conn.close(); // never reached
```

`close()` 永远不会被调用，这条连接就永远不会"归还"，`maxLifetime` 也就永远没有机会去检查、回收它——它会一直卡在"borrowed"状态，直到进程重启。表现就是池子被占满、其他线程排队等 `connectionTimeout`，但从指标上看"连接数没有超过 max"，因为泄漏的连接一直显示为"in use"。

这也是为什么 `leakDetectionThreshold` 和 `maxLifetime` 要分开配置：`maxLifetime` 解决的是"连接太老导致被数据库/负载均衡器单方面断开"的问题，`leakDetectionThreshold` 解决的是"连接被应用代码忘记归还"的问题，两者互不覆盖。而且 `leakDetectionThreshold` 本身也只是**诊断**——只打印 WARN 日志和调用栈，并不会强制关闭或回收这条连接，真正的修复还是要在代码里补上 `try-with-resources` 或 `finally` 里的 `close()`。

## 如何排查连接泄漏

1. **开启 `leak-detection-threshold`**：最直接的手段，日志会打印出借出连接时的调用栈，能直接定位到哪行代码没有关闭连接（例如 try-with-resources 漏用、异常分支没有 `finally` 释放）。
2. **监控连接池指标**：通过 Actuator + Micrometer 暴露 `hikaricp.connections.active`、`hikaricp.connections.pending`、`hikaricp.connections.idle`；如果 `active` 持续增长不回落、`pending`（等待获取连接的线程数）持续增加，说明连接没有归还。
3. **线程 dump 分析**：连接池耗尽时抓 thread dump，看有多少线程阻塞在 `HikariPool.getConnection()`，结合业务代码定位长事务或未提交/未回滚的连接。
4. **代码层面常见泄漏点**：
   - `@Transactional` 方法内部又手动调用 `DataSource.getConnection()` 却没有 close
   - 异常分支下 `Connection`／`Statement`／`ResultSet` 没有用 try-with-resources
   - 长事务（比如事务里调用外部 HTTP 接口）导致连接占用时间过长，表现类似泄漏

## 与其他连接池的关系

早期项目常见 Apache DBCP（见 [dbcp.md](../dbcp.md)）或阿里 Druid，两者都提供类似的池化参数，但 Druid 额外内置了 SQL 监控和防火墙功能，DBCP 定位更基础。HikariCP 不做 SQL 层面的功能扩展，专注做「快」，监控能力依赖 Actuator/Micrometer 这类外部组件补齐。
