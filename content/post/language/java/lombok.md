---
title: Lombok
author: "-"
date: 2026-05-12T15:04:58+08:00
lastmod: 2026-05-12T15:04:58+08:00
url: lombok
categories:
  - Java
tags:
  - java
  - lombok
  - remix
  - AI-assisted
---

Lombok 是一个 Java 编译器插件，通过注解在**编译期**自动生成 getter/setter、构造器、`equals`/`hashCode`、`toString`、Builder 等样板代码，让源文件保持简洁。

**发音**：来自印度尼西亚龙目岛（Lombok Island），读作 **LOM-bok**，重音在第一个音节。

**出现时间**：2009 年首次发布，比 Spring Boot（2014 年）早了五年，与 Spring 没有直接关系，是独立的 Java 工具。

**原理**：利用 Java 编译器的注解处理器（Annotation Processing）在 `javac` 编译时修改语法树，将生成的方法直接写入 `.class` 字节码，源文件里没有这些方法但编译产物里有。IDE 需要安装 Lombok 插件才能识别生成的方法。

## 解决了什么问题

Java 要求显式写大量与业务无关的样板代码，一个普通的 JavaBean 需要：

```java
// 不用 Lombok：一个 User 类要写几十行
public class User {
    private Long id;
    private String name;
    private String email;

    public User() {}
    public User(Long id, String name, String email) { ... }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    // ... 还有 equals / hashCode / toString ...
}
```

用 Lombok：

```java
@Data                   // 生成 getter/setter/equals/hashCode/toString
@NoArgsConstructor      // 生成无参构造器
@AllArgsConstructor     // 生成全参构造器
public class User {
    private Long id;
    private String name;
    private String email;
}
```

## 常用注解

| 注解                       | 作用                                                                                           | 使用频率 |
| -------------------------- | ---------------------------------------------------------------------------------------------- | -------- |
| `@Getter` / `@Setter`      | 生成 getter / setter                                                                           | ★★★★★    |
| `@Data`                    | 相当于 `@Getter` + `@Setter` + `@ToString` + `@EqualsAndHashCode` + `@RequiredArgsConstructor` | ★★★★★    |
| `@Builder`                 | 生成 Builder 模式代码                                                                          | ★★★★★    |
| `@Slf4j` / `@Log4j2`       | 生成日志对象 `log`，省去 `private static final Logger log = ...`                               | ★★★★★    |
| `@NoArgsConstructor`       | 生成无参构造器                                                                                 | ★★★★     |
| `@AllArgsConstructor`      | 生成全参构造器                                                                                 | ★★★★     |
| `@RequiredArgsConstructor` | 生成包含 `final` 字段的构造器，配合 Spring 构造器注入                                          | ★★★★     |
| `@ToString`                | 生成 `toString`                                                                                | ★★★      |
| `@EqualsAndHashCode`       | 生成 `equals` / `hashCode`                                                                     | ★★★      |
| `@Value`                   | 不可变对象：所有字段 `final` + 只有全参构造器                                                  | ★★       |
| `@NonNull`                 | 字段/参数非空校验，自动生成 null check                                                         | ★★       |
| `@Cleanup`                 | 自动关闭资源（类似 try-with-resources）                                                        | ★        |
| `@SneakyThrows`            | 抑制受检异常，不推荐使用                                                                       | ★        |
| `@Synchronized`            | 生成同步方法                                                                                   | ★        |

实际项目中 90% 的 Lombok 使用就是 `@Data` + `@Builder` + `@Slf4j` 这三个。

## 使用策略

Lombok 是按类/按字段粒度选用的，注解加在哪里才生效，引入依赖不强制任何类使用它。同一项目里可以混用：

```java
// DTO 类：用 @Data + @Builder，字段多全是样板代码
@Data
@Builder
public class UserDTO {
    private Long id;
    private String name;
}

// JPA Entity：只用 @Getter/@Setter，避免 @Data 的 equals/hashCode 陷阱
@Entity
@Getter
@Setter
public class UserEntity {
    @Id
    private Long id;
    private String name;
}

// 复杂业务类：不用 Lombok，保留可读性和调试便利性
public class OrderProcessor {
    // 手写全部代码
}
```

常见团队规范：

- ✅ DTO / VO 类 → `@Data` + `@Builder`
- ⚠️ JPA Entity → 只用 `@Getter`/`@Setter`，不用 `@Data`（见下方陷阱）
- ❌ 禁止 `@SneakyThrows`（会隐藏受检异常）

## 常见陷阱

**1. `@Data` 在 JPA Entity 上的 `equals`/`hashCode` 问题**

`@Data` 默认用所有字段生成 `equals`/`hashCode`。Entity 在持久化前 `id` 为 `null`，持久化后有值，导致同一对象放入 `Set` 或作为 `Map` key 时哈希值变化，引发难以排查的 bug。JPA Entity 建议手写或只用 `@Getter`/`@Setter`。

**2. `@Builder` 与继承不兼容**

父类用了 `@Builder`，子类再用 `@Builder` 会冲突，需要大量手工代码绕过。

**3. `@SneakyThrows` 隐藏异常**

可以悄悄吞掉受检异常，让调用方无法感知，不推荐使用。

**4. Java 版本升级风险**

Lombok 依赖 `javac` 内部 API（非公开 API），每次 Java 大版本升级（9、11、17、21）都可能短暂不兼容，需要等 Lombok 发布兼容版本。

**5. 调试困难**

生成的方法在源码里不可见，无法在 getter/setter/Builder 内部打断点。

## 现代 Java 的替代

Java 16+ 引入的 **Record** 类型可以替代 `@Data` 用于不可变数据对象：

```java
// Java Record：语言级别，不需要任何依赖
public record User(Long id, String name, String email) {}
// 自动生成：构造器、getter、equals、hashCode、toString
```

没有 IDE 插件依赖，也没有版本升级风险。但 Record 只适合不可变场景，JPA Entity 等可变对象仍需 Lombok 或手写。
