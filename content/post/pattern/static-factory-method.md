---
title: 静态工厂方法 (Static Factory Method)
author: "-"
date: 2012-03-26T03:37:05+00:00
lastmod: 2026-05-15T11:52:58+08:00
url: static-factory-method
categories:
  - development
tags:
  - Java
  - remix
  - AI-assisted

aliases:
  - /p2626/
  - /p4082/
  - /p4407/
  - /p4447/
  - /p6910/
  - /p7514/
  - /p7517/
  - /p7570/
  - /p7572/
  - /p7618/
  - /p11241/
---

## 与 GoF 工厂方法的区别

**静态工厂方法（Static Factory Method）不是 GoF 23 种设计模式之一**，容易和 GoF 的"工厂方法模式（Factory Method Pattern）"混淆，两者本质不同：

|               | GoF 工厂方法模式                           | 静态工厂方法                          |
| ------------- | ------------------------------------------ | ------------------------------------- |
| 出处          | GoF《设计模式》                            | Effective Java Item 1（Joshua Bloch） |
| 本质          | 定义创建对象的接口，由子类决定实例化哪个类 | 用静态方法代替构造器来创建对象        |
| 是否 GoF 模式 | ✅ 是                                       | ❌ 不是，是编程惯用法（idiom）         |

静态工厂方法是 Joshua Bloch 在《Effective Java》Item 1 中推荐的编程惯例：**用命名的静态方法代替构造函数**。

## 基本概念

创建类的实例的最常见方式是用 `new` 调用构造方法。每执行一条 `new` 语句，都会在堆区产生一个新对象。假如类需要封装创建实例的细节、或控制实例数量，可以改用静态工厂方法。

典型例子：`Class` 实例由 JVM 在加载类时自动创建，程序无法用 `new` 创建 `java.lang.Class` 的实例（没有 public 构造方法）。为此，`Class` 提供了静态工厂方法：

```java
Class c = Class.forName("Sample"); // 返回代表 Sample 类的实例
```

## 相比构造方法的优势

### 1. 方法名可以携带语义

构造方法名必须与类名相同，所有重载版本名字一样，难以区分。静态工厂方法可以任意命名，提高可读性：

```java
public class Gender {
    private String description;
    private static final Gender female = new Gender("女");
    private static final Gender male   = new Gender("男");

    private Gender(String description) { this.description = description; }

    public static Gender getFemale() { return female; }
    public static Gender getMale()   { return male; }

    public String getDescription() { return description; }
}
```

常见命名约定：`valueOf`（类型转换语义）、`getInstance`（获取实例语义）。

```java
Integer a  = Integer.valueOf(100);
Calendar c = Calendar.getInstance(Locale.CHINA);
```

### 2. 不必每次创建新对象

`new` 每次都产生新对象，而静态工厂方法是否创建新对象完全取决于实现。这一特点适合：

- **单例类**：只有唯一实例
- **枚举类**：实例数量有限
- **带缓存的类**：复用已创建的实例
- **不可变类**：实例一旦创建属性不再变化

### 3. 可以返回子类型

`new` 只能创建当前类的实例，静态工厂方法可以返回子类的实例，有助于构建松耦合的接口。

## 单例的两种实现方式

**方式一：public static final 字段**

```java
public class GlobalConfig {
    public static final GlobalConfig INSTANCE = new GlobalConfig();
    private GlobalConfig() { ... }
}
```

三个关键字各司其职，缺一不可：

- **`static`**：字段属于类本身而非某个实例，JVM 加载类时只初始化一次，整个程序生命周期内只有这一份。
- **`final`**：引用不可被重新赋值，防止外部执行 `GlobalConfig.INSTANCE = null` 或替换成新对象。
- **`private` 构造方法**：外部无法 `new` 出新实例，只能通过 `INSTANCE` 访问。

| 缺少什么               | 后果                                                       |
| ---------------------- | ---------------------------------------------------------- |
| 缺 `static`            | 每个实例都有自己的 `INSTANCE` 字段，没有"全局唯一"的语义   |
| 缺 `final`             | 外部可以执行 `GlobalConfig.INSTANCE = null` 或替换成新对象 |
| 构造方法不是 `private` | 外部可以直接 `new GlobalConfig()` 绕过 `INSTANCE`          |

简洁直观，成员声明直接表明是单例。

**方式二：静态工厂方法（推荐）**

```java
public class GlobalConfig {
    private static final GlobalConfig INSTANCE = new GlobalConfig();
    private GlobalConfig() { ... }
    public static GlobalConfig getInstance() { return INSTANCE; }
}
```

灵活性更高：在不改变接口的前提下可以修改内部实现，例如改为每个线程一个实例：

```java
public class GlobalConfig {
    private static final ThreadLocal<GlobalConfig> threadConfig = new ThreadLocal<>();

    private GlobalConfig() { ... }

    public static GlobalConfig getInstance() {
        GlobalConfig config = threadConfig.get();
        if (config == null) {
            config = new GlobalConfig();
            threadConfig.set(config);
        }
        return config;
    }
}
```

## 局限性

由于使用静态方法，静态工厂方法有一定局限性（如无法继承）。Java 的反射机制可以在一定程度上弥补这些不足，结合其他模式可以达到更好的构建效果。
