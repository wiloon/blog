---
title: JDK 1.1
author: "-"
date: 2026-06-20T14:50:50+08:00
lastmod: 2026-06-21T11:46:40+08:00
url: jdk-1.1
categories:
  - language
tags:
  - java
  - jdk
  - remix
  - AI-assisted
---

JDK 1.1 于 **1997 年 2 月 19 日**发布，是 [JDK 1.0](./jdk-1.0.md) 之后的首个重要更新。1.0 以 Applet 与 AWT 打开知名度，1.1 则补上了**企业开发**所需的一批基础能力：数据库、远程调用、反射、序列化、JAR 打包等。命名与后续演变见 [Java 版本历史](./java-version-history.md)。

## 版本号说明

| 维度 | JDK 1.1 |
| ---- | ------- |
| 对外名称 | Java 1.1 / JDK 1.1 |
| `java.version` | `1.1.x` |
| class major version | 45（minor 3，即 45.3） |
| 上一版本 | [JDK 1.0](./jdk-1.0.md) |
| 下一版本 | Java 1.2（1998-12，集合框架与 Swing） |

## 概览

### 语言

- **内部类**（nested classes）：成员内部类、局部内部类、匿名内部类、静态嵌套类（详见 [Java 内部类](./inner-class.md)）

### 类库与规范

- **反射**（`java.lang.reflect`）：运行时检查类、方法、字段并调用
- **JDBC**（`java.sql`）：标准数据库访问 API，Java 进入服务端开发的入口之一
- **RMI**（`java.rmi`）：远程方法调用
- **JavaBeans**（`java.beans`）：组件化与 IDE 工具链约定
- **对象序列化**（`java.io.Serializable` 等）：对象持久化与网络传输
- **JAR**（Java ARchive）：类与资源的打包格式，配套 `jar` 命令
- **国际化**（`java.util.Locale`、`ResourceBundle` 等）与 **Unicode** 文本流（`Reader` / `Writer`）
- **`java.text`**：日期、数字格式化
- **`java.math`**：`BigDecimal`、`BigInteger`

### AWT

- **委托事件模型**（delegation event model）：用监听器（如 `ActionListener`）替代 1.0 的 `handleEvent()` 继承式写法；GUI 代码结构变化较大，属于**不兼容**的 API 调整

### JVM 与性能

- 引入 **JIT 编译器**（因平台而异），热点 bytecode 可编译为本地代码，性能较 1.0 纯解释执行明显提升
- **类卸载**（class unloading）等运行时能力增强
- 仍为 Sun 早期 JVM；[HotSpot](./hotspot.md) 要到 1.3 才成为默认实现

### 工具

- **`jar`**：打包与解包 JAR
- **`serialver`**：查看序列化类的 `serialVersionUID`
- **`jdb`** 等调试工具随 JDK 增强

### 1.1 尚未具备（后续版本才加入）

| 能力 | 大致引入版本 |
| ---- | ------------ |
| Swing、集合框架（`HashMap` 等） | 1.2 |
| `java.lang.ref`（软/弱/虚引用） | 1.2 |
| HotSpot 默认 VM | 1.3（1.4 起唯一，见 [HotSpot](./hotspot.md)） |
| `assert`、NIO、标准正则 | 1.4 |
| 泛型、enum、for-each、JUC | 5 |

---

## 内部类

1.0 只有顶层类；1.1 起可在类或方法内部定义嵌套类，为回调、封装 helper、匿名监听器等场景提供语法支持：

```java
button.addActionListener(new ActionListener() {
    @Override
    public void actionPerformed(ActionEvent e) {
        // 匿名内部类，常见于 1.1 AWT/Swing 时代
    }
});
```

编译后内部类会生成 `Outer$Inner.class` 等形式。设计动机与用法见 [Java 内部类](./inner-class.md)。

---

## 反射

JDK 1.1 引入 `java.lang.reflect`，允许在运行时获取 [`Class`](./lang-class.md) 对象并调用构造器、方法、字段：

```java
Class<?> clazz = Class.forName("com.example.Foo");
Object obj = clazz.getDeclaredConstructor().newInstance();
Method m = clazz.getMethod("bar", String.class);
m.invoke(obj, "hello");
```

反射为 JavaBeans、序列化、RMI、框架与 IDE 提供了基础设施；`Class` 的含义与获取方式见 [java.lang.Class](./lang-class.md)。JDK 9 起的模块系统与后续**强封装**对深层反射做了更多限制（见 [JDK 17](./jdk-17.md) 等）。

---

## JDBC

JDBC 定义统一的数据库访问接口，应用通过驱动连接不同厂商的数据库：

```java
Connection conn = DriverManager.getConnection(url, user, password);
Statement stmt = conn.createStatement();
ResultSet rs = stmt.executeQuery("SELECT id FROM users");
```

1.1 确立 `java.sql` 核心类型（`Connection`、`Statement`、`ResultSet` 等）；后续版本在连接池、批处理、`try-with-resources` 等方面演进（JDBC 4.1 的 `AutoCloseable` 见 [JDK 7](./jdk-7.md)）。

---

## RMI

RMI 使 JVM 之间可通过远程接口调用方法，典型用于早期分布式 Java 应用：

```java
// 服务端导出远程对象，客户端通过 Registry 查找 stub 并调用
MyRemote stub = (MyRemote) Naming.lookup("//host/MyService");
stub.doWork();
```

RMI 在微服务与 HTTP/gRPC 普及后使用减少；JDK 17 移除了 RMI Activation（见 [JDK 17](./jdk-17.md)）。

---

## 序列化与 JAR

**序列化**让对象可写入字节流并在另一 JVM 还原：

```java
ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("data.ser"));
out.writeObject(myObject);
```

类需实现 `Serializable`；`serialver` 工具可查看编译器生成的 `serialVersionUID`。

**JAR** 将 `.class`、资源与 `META-INF/MANIFEST.MF` 打成一个文件，便于 Applet 下载、类路径分发与（后来的）签名：

```bash
jar cvf myapp.jar com/example/*.class
```

1.1 起 JAR 成为 Java 生态的标准分发单元；Applet 与早期 Web 应用广泛依赖。

---

## 国际化与 Unicode

1.1 加强了对多语言的支持：

- **`Locale`**、**`ResourceBundle`**：按语言/地区加载属性文件中的文案
- **`Reader` / `Writer`**：基于字符的 I/O，配合 Unicode，弥补 1.0 `InputStream` / `OutputStream` 按字节处理的不足
- **`java.text.DateFormat` / `NumberFormat`**：按区域格式化日期与数字

---

## AWT 委托事件模型

1.0 通过继承 `Component` 并重写 `handleEvent()` 处理 GUI 事件；1.1 改为**监听器**注册：

```java
button.addActionListener(new ActionListener() {
    public void actionPerformed(ActionEvent e) {
        System.out.println("clicked");
    }
});
```

旧代码需迁移；Swing（1.2）沿用同一套监听器思路。1.0 的 Applet/AWT 程序升级 1.1 时常需改事件处理代码。

---

## 历史背景（简述）

1997 年距 1.0 发布约 **21 个月**。浏览器里的 Applet 仍带热度，但 JDBC 与 RMI 让 Java 开始被服务端与中间件场景认真采用——为 1998 年 **Java 1.2**（Swing、集合框架、「Java 2 Platform」品牌）铺路。平台命名、发布节奏见 [Java 版本历史](./java-version-history.md)。

---

## 与 JDK 1.0 的衔接

| 主题 | JDK 1.0 | JDK 1.1 |
| ---- | ------- | ------- |
| 嵌套类型 | 仅顶层类 | 内部类 |
| 运行时自省 | 无标准反射 API | `java.lang.reflect` |
| 数据库 / 远程调用 | 无 | JDBC、RMI |
| 打包 | 松散 `.class` | JAR |
| GUI 事件 | `handleEvent()` | 监听器模型 |
| JVM | 以解释为主 | 引入 JIT |

更完整的 1.0 基线见 [JDK 1.0](./jdk-1.0.md)。

---

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-06-21 | 反射章节链至 `java-lang-class.md` | Class 概念独立成文 |
| 2026-06-21 | 修正 HotSpot 引入版本表述 | 与 hotspot.md 时间线对齐 |

---

## 参考

- [Java version history（Wikipedia）](https://en.wikipedia.org/wiki/Java_version_history)
- [JDK 1.1 Documentation（Oracle 归档）](https://docs.oracle.com/javase/1.5.0/docs/guide/jdk/1.1.html)
- [Java Class File Version Numbers（Wikipedia）](https://en.wikipedia.org/wiki/Java_class_file#General_layout)
