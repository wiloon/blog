---
title: Spring Boot 关系型数据库持久层概览
author: "-"
date: 2014-05-22T03:12:14+00:00
lastmod: 2026-05-20T09:49:47+08:00
url: spring-boot-relational-persistence
categories:
  - development
tags:
  - java
  - spring-boot
  - JPA
  - jdbc
  - mybatis
  - spring-data-jdbc
  - jooq
  - remix
  - AI-assisted

aliases:
  - /p6649/
  - jpa
---

## 概述

在 Spring Boot 里访问 MySQL、PostgreSQL、SQLite 等关系型数据库，常见有几条路线。它们最终都经过 **JDBC** 连到数据库，差别在于中间抽象层有多高、SQL 由谁写。

```text
应用代码
    │
    ├── Spring Data JDBC        ← Repository 风格，底层仍是 JDBC
    ├── Spring Data JPA         ← 对象为主，框架生成 SQL
    │       └── JPA（标准）→ Hibernate（实现）
    ├── MyBatis (+ Plus)        ← SQL 手写 + 映射
    └── JdbcTemplate / JDBI / jOOQ  ← SQL 路线（字符串或类型安全 DSL）
```

下面分别介绍 **Spring Data JDBC**、**Spring Data JPA**、**MyBatis**、**JdbcTemplate**、**JDBI**、**jOOQ**，并简要说明 **JPA** 本身是什么。

---

## Spring Data JDBC

**Spring Data JDBC** 是 Spring 官方提供的 **轻量持久化方案**，依赖 `spring-boot-starter-data-jdbc`。它提供与 Spring Data JPA 类似的 `CrudRepository` 接口风格，但 **不是 ORM**，底层仍通过 **JdbcTemplate** 访问数据库。

| 项目     | 说明                                    |
|----------|-----------------------------------------|
| 依赖     | `spring-boot-starter-data-jdbc`         |
| 是否 ORM | 否，无持久化上下文、无懒加载、无 Hibernate |
| 典型用法 | `CrudRepository` + `@Table` 实体        |

```java
@Table("users")
public class User {
    @Id
    private Long id;
    private String name;
    private String email;
}

public interface UserRepository extends CrudRepository<User, Long> {
    List<User> findByEmail(String email);
}
```

**特点**：

- 简单 CRUD 可像 JPA 一样用接口方法名派生查询，少写 Dao 实现类。
- 实体与表多为 **一对一** 映射；跨表关联不会像 JPA 那样自动维护对象图，复杂关联需手写 SQL 或拆成多次查询。
- 没有 JPA 的 `merge`/`persist`、一级缓存、懒加载等概念，行为更直观、可预测。
- 与 JdbcTemplate 共用同一套 **DataSource 自动配置**（默认 HikariCP）。

**在栈中的位置**：

```text
UserRepository extends CrudRepository<User, Long>
        ↓
Spring Data JDBC（Repository 封装）
        ↓
JdbcTemplate（执行 SQL）
        ↓
HikariCP DataSource → JDBC → 数据库
```

### 不是 ORM，但有对象—表行映射

在 Spring Data JDBC 这条路线里，**没有 JPA/Hibernate 那种意义上的 ORM**；并不是「Java 对象和数据库毫无关系」——它仍会把查询结果填进实体、把实体写成 `INSERT`/`UPDATE`，这叫 **row mapping（行映射）**，JdbcTemplate 的 `RowMapper` 也属于同一类。

两种「映射」不要混在一起：

| 能力 | 完整 ORM（JPA/Hibernate） | Spring Data JDBC |
| ---- | ------------------------- | ---------------- |
| 对象 ↔ 表行 | 有 | 有（`@Table`、`@Id` 等） |
| 持久化上下文 / 一级缓存 | 有 | **无** |
| 脏检查、自动 flush | 有 | **无** |
| 懒加载、`@OneToMany` 对象图 | 有 | **无**（关联需手写 SQL 或拆查询） |
| `merge` / `persist` 生命周期 | 有 | **无**（就是明确的 insert/update/delete） |
| 跨表级联维护对象图 | 有 | **无** |

表面上 Repository + `@Table` 实体很像 JPA，但行为不同：JPA 的 `findById` 可能带出懒加载的关联集合，改字段后提交时可能只更新脏列；Spring Data JDBC 的 `findById` 就是一次 `SELECT`，保存就是明确的写库，**没有「受管实体」概念**。Spring 官方也更强调 **Aggregate（聚合）**：以单表或简单聚合根为主，复杂多表关联不会像 ORM 那样自动维护双向关系。

和 MyBatis 的定位对比：Spring Data JDBC 几乎不算 ORM；MyBatis 常称 **半自动 ORM**（有映射、SQL 你写）；JPA/Hibernate 是 **完整 ORM**。

### 为何不需要 Hibernate 等 JPA 实现

这不是 Spring Data 对两条路线「要求不同」，而是 **中间有没有 ORM 引擎层**：

```text
Spring Data JPA
    → Spring Data JPA（Repository）
    → JPA API（规范，本身不能运行）
    → JPA 实现（Hibernate / EclipseLink 等）  ← 必须有
    → JDBC → 数据库

Spring Data JDBC
    → Spring Data JDBC（Repository + 简单 SQL 生成）
    → JdbcTemplate（Spring 自带）
    → JDBC → 数据库
```

**JPA 是规范（合同）**，只定义 `EntityManager`、注解、JPQL 等接口和约定，具体映射、SQL 生成、缓存由 **Provider** 实现。Spring Data JPA 只负责 Repository 封装，不实现 ORM 核心，因此必须再挂一个实现；Spring Boot 默认选 Hibernate，换成 EclipseLink 也可以，但要自己配依赖。

**JDBC 已是底层标准 API**（`Connection`、`PreparedStatement`…），JDK + 数据库驱动就是实现，没有「JDBC 的 Hibernate」要选。Spring Data JDBC 自己用 `JdbcTemplate` 执行 SQL，不管理对象图、持久化上下文，所以 **不需要再绑一个 ORM 引擎**。

**与其它方案对比**：

|             | JdbcTemplate | Spring Data JDBC    | Spring Data JPA    |
|-------------|--------------|---------------------|--------------------|
| Repository  | 需自己写 Dao | 有 `CrudRepository` | 有 `JpaRepository` |
| SQL         | 全手写       | 简单 CRUD 自动生成  | 多数自动生成       |
| 复杂度      | 低           | 中                  | 高（ORM 特性多）     |
| Boot 常见度 | 中等         | 较低                | 很高               |

适合：想要 Repository 风格、又不想引入 Hibernate/JPA 全套 ORM 的项目；领域模型简单、以单表 CRUD 为主。

---

## JPA 与 Spring Data JPA

### JPA 是什么

**JPA（Java Persistence API）** 是 Java 的 **持久化规范（标准）**，定义实体注解、`EntityManager`、JPQL 等约定。它本身不是可直接运行的框架，需要 **实现**，Spring Boot 默认使用 **Hibernate**。

| 层级            | 角色                                 |
|-----------------|--------------------------------------|
| JPA             | 标准（合同）                           |
| Hibernate       | 最常见的 JPA 实现（ORM 引擎）          |
| Spring Data JPA | Spring 在 JPA 之上的 Repository 封装 |

关系：

```text
CommentRepository extends JpaRepository<Comment, Long>
        ↓
Spring Data JPA（少写 Dao 实现）
        ↓
JPA API
        ↓
Hibernate（映射、SQL 生成、缓存）
        ↓
JDBC → 数据库
```

### Spring Data JPA

**Spring Data JPA** 不负责 ORM 核心逻辑，而是提供 `JpaRepository`、方法名派生查询、分页、`@Query` 等，让你少写 Repository 实现类。

```java
public interface UserRepository extends JpaRepository<User, Long> {
    List<User> findByEmail(String email);
}
```

**特点**：CRUD 和简单关联省事；复杂 SQL 仍可用 `@Query(nativeQuery = true)` 或退回 JdbcTemplate。

**常见误解**：Spring Data JPA ≠ 又一个 ORM；底层仍是 Hibernate（等）实现 JPA。

### 为何使用 ORM / JPA（简述）

相对裸 JDBC，ORM 把 Java 对象与表行建立映射，减少手写 SQL 和结果集拼装；JPA 作为标准，便于在不同实现间迁移。实际项目中需权衡：复杂查询、性能调优时往往仍要手写 SQL 或原生查询。

---

## MyBatis 与 MyBatis-Plus

**MyBatis** 是 **半自动 ORM**：表与 Java 对象有映射，但 **SQL 主要由开发者编写**（XML 或注解），框架负责执行与结果映射。

| 项目     | 说明                                |
|----------|-------------------------------------|
| 依赖     | `mybatis-spring-boot-starter`       |
| SQL      | 手写为主                            |
| 典型用法 | `UserMapper` 接口 + XML / `@Select` |

**MyBatis-Plus** 在 MyBatis **之上**做增强，**不能脱离 MyBatis 单独使用**。提供 `BaseMapper`（内置 `insert`/`selectById` 等）、`QueryWrapper` 条件构造、分页、逻辑删除、代码生成器等，减少简单 CRUD 的 XML。

```java
public interface UserMapper extends BaseMapper<User> {}

// 条件查询
userMapper.selectList(
    new LambdaQueryWrapper<User>().eq(User::getEmail, email));
```

**与 JPA 对比**：

|            | MyBatis / Plus | Spring Data JPA |
|------------|----------------|-----------------|
| 思路       | SQL 优先       | 对象优先        |
| SQL 可见性 | 高             | 多数自动生成    |
| 国内常见度 | 很高           | 很高            |

复杂多表 JOIN 仍常用 MyBatis 原生 XML 写法。

---

## JdbcTemplate

**JdbcTemplate** 是 **Spring Framework** 提供的工具类（`org.springframework.jdbc.core.JdbcTemplate`），**不是 JDK 原生 API**。JDK 提供的是 `Connection`、`PreparedStatement`、`ResultSet` 等 JDBC 接口；JdbcTemplate 在其上封装了连接获取、参数绑定、异常转换和 `RowMapper` 结果映射。

| 项目     | 说明                                                  |
|----------|-------------------------------------------------------|
| 依赖     | `spring-boot-starter-jdbc`                            |
| 是否 ORM | 否，需手写 SQL                                         |
| 典型用法 | `jdbcTemplate.query(...)`、`update(...)` + `RowMapper` |

示例：

```java
@Repository
public class UserDao {
    private final JdbcTemplate jdbcTemplate;

    public User findByName(String name) {
        return jdbcTemplate.queryForObject(
            "SELECT * FROM users WHERE name = ?",
            new UserRowMapper(),
            name);
    }
}
```

**特点**：SQL 完全可控，适合简单 CRUD、复杂 JOIN、报表；样板代码比裸 JDBC 少，但比 JPA/MyBatis-Plus 多。

**与 JPA 对比**：JdbcTemplate 是「SQL 优先」；JPA 是「对象优先」，由框架生成 SQL。

**连接池**：项目里通常只配 `spring.datasource.url` 等少量属性；`spring-boot-starter-jdbc` 会由 Spring Boot 自动创建 **HikariCP** 连接池和 `DataSource`，再注入到 `JdbcTemplate`（约定优于配置）。

---

## JDBI

**JDBI**（Java Database Interface，现多为 **JDBI 3**）是 **第三方**轻量级 JDBC 封装库，**不属于 Spring 或 JDK**。定位与 JdbcTemplate 接近：**SQL 优先、非 ORM**，API 更现代。

| 风格       | 说明                                 |
|------------|--------------------------------------|
| Fluent API | 链式拼 SQL、绑参数、映射 Bean          |
| SqlObject  | 接口 + 注解声明 SQL（类似极简 Mapper） |

```java
public interface UserDao {
    @SqlQuery("SELECT * FROM users WHERE id = :id")
    User findById(@Bind("id") String id);
}
```

可通过 `jdbi3-spring-boot-starter` 等接入 Spring Boot。

**在生态中的位置**：与 JdbcTemplate 同属「手写 SQL」路线，但在 Spring Boot 项目中 **使用率较低**（小众）；求职与日常项目里 JPA、MyBatis、JdbcTemplate 更常见。

|              | JdbcTemplate      | JDBI           |
|--------------|-------------------|----------------|
| 归属         | Spring 官方       | 第三方         |
| Spring 集成  | 原生 starter-jdbc | 需额外 starter |
| 常见度（Boot） | 中等              | 较低           |

---

## jOOQ

**jOOQ**（jOOQ Object Oriented Querying）是 **第三方**库（Data Geekery），在 JDBC 之上提供 **类型安全的 SQL DSL**。它 **不是 ORM**：不管理实体生命周期、不做对象图关联，核心仍是 **SQL 优先**，但用 Java 代码拼查询，并在编译期检查表名、列名。

| 项目     | 说明                                      |
|----------|-------------------------------------------|
| 依赖     | `spring-boot-starter-jooq`                |
| 是否 ORM | 否                                        |
| 典型用法 | 代码生成器产出表/列常量 + `DSLContext` 查询 |

**代码生成（Codegen）**：可根据数据库 schema 生成 `USERS`、`USERS.ID` 等 Java 类，避免手写 SQL 字符串时的拼写错误。

```java
// 类型安全 DSL，编译期可检查列名
List<UserRecord> users = dsl
    .selectFrom(USERS)
    .where(USERS.EMAIL.eq(email))
    .fetchInto(UserRecord.class);
```

也可执行原生 SQL，或与生成类混用。

**在栈中的位置**：

```text
@Service
    ↓
DSLContext（jOOQ 入口）
    ↓
生成 SQL + 绑定参数
    ↓
JDBC（共用 Spring Boot 的 DataSource / HikariCP）
    ↓
数据库
```

**与其它「SQL 路线」对比**：

|              | JdbcTemplate   | JDBI           | jOOQ                    |
|--------------|----------------|----------------|-------------------------|
| SQL 形式     | 字符串         | 字符串 / 注解  | Java DSL（类型安全）    |
| 表结构校验   | 运行时         | 运行时         | 编译期（配合 codegen）  |
| 学习成本     | 低             | 中             | 中高（需熟悉 DSL/codegen） |
| Boot 常见度  | 中等           | 较低           | 较低                    |

**特点**：

- 复杂查询、动态条件、多表 JOIN、报表类 SQL 表达力强，且比纯字符串 SQL 更易重构。
- 切换数据库方言时，DSL 可适配不同 SQL 方言（仍要测试）。
- 引入 codegen 后构建链略复杂（需连库或离线 schema 生成代码）。

**适合**：团队重视 SQL 可控与类型安全；查询复杂、字段多，希望减少 `"SELECT ..."` 字符串错误。不适合只想快速 CRUD、不愿维护生成代码的小项目。

---

## 方案选型简表

| 方案                        | 类型                     | SQL 谁写      | Spring Boot 常见度 |
|-----------------------------|--------------------------|---------------|--------------------|
| Spring Data JDBC            | JDBC + Repository 封装   | 你 + 部分自动 | 较低               |
| Spring Data JPA + Hibernate | 标准 + ORM + Spring 封装 | 框架为主      | 很高               |
| MyBatis / MyBatis-Plus      | 半自动 ORM + 增强        | 你为主        | 很高               |
| JdbcTemplate                | Spring JDBC 工具         | 你            | 中等               |
| JDBI                        | 第三方 JDBC 封装         | 你            | 较低               |
| jOOQ                        | 类型安全 SQL DSL         | 你（DSL 生成） | 较低               |

- **要 Repository 风格、但不想上 JPA/Hibernate**：Spring Data JDBC
- **CRUD 多、实体关联多、团队熟悉 ORM**：Spring Data JPA
- **复杂 SQL 多、习惯写 SQL、国内传统项目**：MyBatis / MyBatis-Plus
- **要完全掌控 SQL、项目简单**：JdbcTemplate 或 JDBI
- **复杂 SQL 多、又要编译期类型安全**：jOOQ

---

## JPA 的 merge 与 persist

`persist` 把实体放入持久化上下文；若上下文中已有该实体，会抛出 `EntityExistsException`。事务提交时若数据库中已存在对应行，可能抛出完整性约束异常。

`merge` 在持久化上下文中生成或更新**受管版本**：若已有受管实体则更新，否则复制一份并返回受管对象。事务提交时，数据库无对应行则插入，有则更新。`merge` 一般不会因「对象重复」像 `persist` 那样在调用时立刻抛 `EntityExistsException`。

**persist 行为摘要**：

1. 若 persist 的是**受管实体**（已在上下文中），不抛异常。
2. 若是**游离实体**且上下文中无受管版本、数据库也无记录，写入数据库，不抛异常。
3. 若是游离实体且上下文中无受管版本、但**数据库已有**该行，persist 时不一定抛异常，**事务提交时**可能抛出 `MySQLIntegrityConstraintViolationException`（重复键）。
4. 若是游离实体且上下文中**已有受管版本**、数据库无记录，实际持久化的是受管版本，persist 与未 persist 效果类似。
5. 若是游离实体且上下文中已有受管版本、数据库也有记录，persist 时抛出 `EntityExistsException`。

**merge**：通常不抛出上述「对象重复」类异常，按「有则更新、无则插入」合并状态。

---

## 参考

- [JPA merge 与 persist 原文](http://pz0513.blog.51cto.com/443986/113098)（辽源大火的奋斗历程）
