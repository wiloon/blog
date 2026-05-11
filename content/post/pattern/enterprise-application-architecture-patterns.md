---
title: 企业应用架构模式
author: "-"
date: 2026-05-11T16:19:04+08:00
lastmod: 2026-05-11T16:19:04+08:00
url: enterprise-application-architecture-patterns
categories:
  - pattern
tags:
  - java
  - architecture
  - remix
  - AI-assisted
---

## 什么是企业应用架构模式

**企业应用架构模式（Patterns of Enterprise Application Architecture，简称 PoEAA）** 由 Martin Fowler 在 2002 年出版的同名书中系统整理，专门解决企业级应用中反复出现的架构问题。

它与 GoF 23 种设计模式的区别：

|          | GoF 设计模式（1994）        | 企业应用架构模式（2002）                      |
| -------- | --------------------------- | --------------------------------------------- |
| 关注层面 | 对象级别，类与类之间的协作  | 应用架构级别，层与层之间的设计                |
| 典型问题 | 如何创建对象、如何解耦行为  | 如何组织 Web 层、如何访问数据库、如何处理并发 |
| 典型模式 | Factory、Observer、Strategy | Front Controller、Repository、Unit of Work    |

两套模式不冲突，可以同时使用。

---

## Web 表现层模式

### Front Controller（前端控制器）

所有 HTTP 请求通过**单一入口**，集中处理身份验证、日志、权限等横切关注点，再路由到具体处理器。

```
所有请求 → Front Controller → Dispatcher → 具体 Handler
```

**Spring MVC 实现**：`DispatcherServlet` 是标准的 Front Controller 实现，映射到 `/` 接收所有请求，通过 `HandlerMapping` 路由到对应的 `@Controller` 方法。

详见 [Front Controller Pattern](front-controller-pattern)。

### Page Controller（页面控制器）

每个页面或 URL 对应一个独立的控制器类。原始 Servlet 就是这种模式——`/users` 对应 `UsersServlet`，`/orders` 对应 `OrdersServlet`。

缺点：横切关注点（认证、日志）在每个控制器中重复，难以统一管理。Front Controller 正是为解决这个问题而生。

### Template View（模板视图）

在 HTML 模板中嵌入动态逻辑，服务端渲染后返回完整 HTML。JSP、Thymeleaf、Freemarker 都是这种模式的实现。

### Transform View（转换视图）

将领域数据转换为 HTML，逻辑与模板分离。XSLT 是典型实现，现代场景中 JSON API + 前端渲染也有这种思想。

---

## 数据源层模式

### Repository（仓储）

在领域层和数据映射层之间建立抽象，提供类似集合的接口访问领域对象。调用方只需调用 `userRepository.findById(id)`，不需要关心底层是 SQL 还是 NoSQL。

Spring Data JPA 的 `JpaRepository` 是典型实现。

### Active Record（活动记录）

领域对象自身包含数据库访问逻辑，一个对象对应数据库一行。Ruby on Rails 的 ORM 是标准实现，Java 生态中 MyBatis-Plus 的部分特性接近这种风格。

### Data Mapper（数据映射器）

领域对象与数据库完全分离，由独立的 Mapper 层负责两者之间的转换。Hibernate、MyBatis 是这种模式的实现。领域对象不知道数据库的存在，适合复杂业务模型。

### Unit of Work（工作单元）

跟踪一次业务操作中所有对象的变化，在操作结束时统一提交，避免多次单独的数据库调用。Hibernate 的 Session、JPA 的 EntityManager 内部都实现了 Unit of Work。

### Identity Map（标识映射）

在一次请求或事务范围内，保证每个数据库行只加载一次，后续访问从缓存返回相同对象实例，避免重复查询和对象不一致问题。Hibernate 的一级缓存就是 Identity Map。

---

## 业务逻辑层模式

### Transaction Script（事务脚本）

按业务操作组织逻辑，每个操作对应一个过程/方法，直接操作数据库。适合简单业务场景，CRUD 应用常见。缺点是业务复杂后代码难以复用，逻辑散落各处。

### Domain Model（领域模型）

将业务逻辑封装在领域对象内部，对象不仅有数据还有行为。适合复杂业务场景，是 DDD（领域驱动设计）的基础。缺点是与 ORM 结合有阻抗失配问题。

### Service Layer（服务层）

在领域模型之上定义应用的操作边界，协调领域对象完成用例，处理事务、安全、通知等应用级关注点。Spring 中的 `@Service` 注解标注的类就是服务层。

---

## 并发模式

### Optimistic Offline Lock（乐观离线锁）

在数据中加版本号字段，提交时检查版本是否被其他人修改，未修改则提交，已修改则拒绝并提示冲突。适合读多写少场景。JPA 的 `@Version` 注解是标准实现。

### Pessimistic Offline Lock（悲观离线锁）

操作前先加锁，阻止其他人同时修改。适合冲突频繁的场景，但吞吐量低。SQL 中的 `SELECT FOR UPDATE` 是典型实现。

---

## 参考

- Martin Fowler, *Patterns of Enterprise Application Architecture*, 2002
- [martinfowler.com/eaaCatalog](https://martinfowler.com/eaaCatalog/)
