---
title: JDBI 使用笔记
author: "-"
date: 2019-10-29T02:20:23+00:00
lastmod: 2026-06-02T19:31:45+08:00
url: jdbi
categories:
  - language
tags:
  - java
  - remix
  - AI-assisted
---

[JDBI 官网](http://jdbi.org/)

JDBI 是一个非 ORM 的 Java 数据库访问库，特别适合数据库固定不变的场景——即不需要兼容多种数据库、也不打算更换数据库的项目。如果需要多数据库兼容，建议选择 Hibernate 等 ORM 框架。

JDBI 的优点：

- API 与 JDBC 接近，学习成本低
- jdbi3 支持流式 / 函数式编程风格
- 源码实现清晰，封装出的数据库代码可读性强

## 两种 API 风格

### Fluent API

链式调用风格，适合内联编写 SQL：

```java
handle.createUpdate("INSERT INTO user(id, name) VALUES (:id, :name)")
    .bind("id", 2)
    .bind("name", "Clarice")
    .execute();
```

### Declarative API

通过注解声明 SQL，适合面向对象风格，代码更简洁易维护：

```java
public interface UserDao {

    @SqlUpdate("CREATE TABLE user (id INTEGER PRIMARY KEY, name VARCHAR)")
    void createTable();

    @SqlUpdate("INSERT INTO user(id, name) VALUES (?, ?)")
    void insertPositional(int id, String name);

    @SqlUpdate("INSERT INTO user(id, name) VALUES (:id, :name)")
    void insertNamed(@Bind("id") int id, @Bind("name") String name);

    @SqlUpdate("INSERT INTO user(id, name) VALUES (:id, :name)")
    void insertBean(@BindBean User user);

    @SqlQuery("SELECT * FROM user ORDER BY name")
    @RegisterBeanMapper(User.class)
    List<User> listUsers();
}
```

## 参考

- <https://www.jianshu.com/p/1ee34c858cb9>
