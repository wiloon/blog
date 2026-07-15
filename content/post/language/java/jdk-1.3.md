---
title: JDK 1.3
author: "-"
date: 2026-07-14T22:48:29+08:00
lastmod: 2026-07-14T22:48:29+08:00
url: jdk-1.3
categories:
  - language
tags:
  - java
  - jdk
  - hotspot
  - remix
  - AI-assisted
---

JDK 1.3（对外称 **Java 2 Platform, Standard Edition, v1.3**，代号 **Kestrel**）于 **2000 年 5 月 8 日**发布，是 [JDK 1.2](./jdk-1.2.md) 之后又一次以**运行时**为核心的升级——最重要的变化不在语言语法，而在 JVM 本身：**HotSpot 从此成为默认 VM**。命名与后续演变见 [Java 版本历史](./java-version-history.md)。

## 版本号说明

| 维度 | JDK 1.3 |
| ---- | ------- |
| 对外名称 | Java 2 SE 1.3 / JDK 1.3 |
| 代号 | Kestrel |
| `java.version` | `1.3.x` |
| class major version | 47 |
| 上一版本 | [JDK 1.2](./jdk-1.2.md) |
| 下一版本 | [JDK 1.4](./jdk-1.4.md) |

## 概览

### JVM：HotSpot 成为默认 VM

这是 1.3 最重要的变化。HotSpot 早在 **1999 年 4 月**就以独立产品 **Java HotSpot Performance Engine** 发布，可配合 JDK 1.2 使用，但当时不是默认项；**JDK 1.3 起 HotSpot 成为默认 VM**，旧的 **Classic VM 仍可通过参数选用**，直到 [JDK 1.4](./jdk-1.4.md) 才被彻底移除。详见 [HotSpot](./hotspot.md)。

对使用者来说，这次切换意味着：

- **JIT 编译**从「因平台而异」的早期实现，变为 HotSpot 统一的 **C1 / C2** 编译体系（详见 [HotSpot](./hotspot.md)）
- **垃圾回收从非分代切换为分代**：Classic VM 的固定标记-清除收集器被 HotSpot 的分代模型取代，[Serial 收集器](./gc.md#新生代收集器)（新生代）+ Serial Old（老年代）成为此时事实上**唯一**的组合，直到 JDK 1.4 才出现 Parallel Scavenge（详见下文「垃圾回收」）
- 提供 **Client** 与 **Server** 两种模式（`-client` / `-server`），分别面向启动速度/内存占用和峰值吞吐

### 类库

- **JNDI**（`javax.naming`）从可选扩展**并入核心 JDK**，提供统一的命名与目录服务访问（LDAP、CORBA Naming、RMI Registry 等）
- **动态代理**（`java.lang.reflect.Proxy`）：运行时生成实现指定接口的代理类，是后续 AOP、RPC 框架的基础设施之一
- **RMI-IIOP**：RMI 新增对 **CORBA IIOP** 协议的可选兼容，Java 对象可与 CORBA 客户端互通
- **Java Sound API**（`javax.sound`）：音频采集、处理、回放与 MIDI 合成
- **`java.awt.Robot`**：生成原生鼠标/键盘事件，主要用于 GUI 自动化测试

### 工具与诊断

- **JPDA**（Java Platform Debugger Architecture）从 1.3.x 起由 JDK **直接支持**（此前的 1.2.2 只是先推出工具集），详见 [Java 调试与 JPDA](./java-debug-JPDA.md)

### 1.3 尚未具备（后续版本才加入）

| 能力 | 大致引入版本 |
| ---- | ------------ |
| Classic VM 彻底移除，HotSpot 成为唯一实现 | 1.4 |
| `assert`、NIO、标准正则、Parallel Scavenge | 1.4 |
| 泛型、enum、for-each、JUC | 5 |
| Parallel Old、CMS 正式支持 | 1.5 / 1.6（见 [Java GC](./gc.md#收集器发展时间线)） |

---

## HotSpot 成为默认 VM

1.3 之前的 JDK（1.0～1.2）默认使用 Sun 自研的 **Classic VM**：以解释执行为主，各平台 JIT 实现不统一，GC 是固定的单线程标记-清除、不分代。HotSpot 首次发布于 1999 年 4 月，作为可选组件配合 JDK 1.2 使用；到了 1.3，Sun 直接把它设为**默认** VM：

```bash
# JDK 1.3 起，不加参数默认走 HotSpot
java -version

# 仍可显式切回 Classic VM（1.4 起该参数被移除）
java -classic -version
```

HotSpot 带来的核心能力是**自适应优化**：解释执行起步，运行时持续探测热点方法，用 C1/C2 编译为本地代码，比 Classic VM「一刀切」的早期 JIT 更接近真实负载。完整历史见 [HotSpot](./hotspot.md#历史)。

---

## 垃圾回收

HotSpot 取代 Classic VM，对 GC 是一次根本性的变化——不只是速度提升，而是**分代模型第一次出现**：

| 维度 | JDK 1.0～1.2（Classic VM） | JDK 1.3（HotSpot 默认） |
| ---- | --------------------------- | ------------------------ |
| 是否分代 | 否，整堆扫描 | 是，新生代 / 老年代 |
| 收集算法 | 固定标记-清除，不压缩 | 新生代复制算法 + 老年代标记-整理 |
| 可选收集器 | 0（无参数可切换） | Serial（新生代）+ Serial Old（老年代），此时无其他选择 |
| 执行方式 | 单线程、Stop-The-World | 单线程、Stop-The-World（Serial 本身仍是单线程收集器） |

也就是说，1.3 虽然让 GC「分代」了，但**收集器本身依然只有一种组合**——直到 JDK 1.4.1 才出现 Parallel Scavenge，JDK 1.4.2 才有 CMS。完整的收集器演进时间线见 [Java GC](./gc.md#收集器发展时间线)（该表格「JDK 1.3.1 及以前」这一档，指的正是 HotSpot 默认化之后、Parallel Scavenge 出现之前的这段时期）。

---

## JNDI 并入核心

1.3 之前 JNDI 是需要单独下载的扩展包；1.3 起 `javax.naming` 成为 JDK 标准库的一部分，为访问 LDAP、CORBA 命名服务、RMI Registry 等提供统一 API：

```java
Context ctx = new InitialContext();
Object obj = ctx.lookup("java:comp/env/jdbc/myDataSource");
```

企业级应用（尤其后续 J2EE/EJB 场景）用它做资源查找，是这一时期「Java 走向服务端」的又一块拼图，与 [JDK 1.1](./jdk-1.1.md) 引入的 JDBC、RMI 属于同一条线。

---

## 动态代理

`java.lang.reflect.Proxy` 允许运行时为一组接口生成代理类，方法调用统一转发给 `InvocationHandler`：

```java
Object proxy = Proxy.newProxyInstance(
    MyService.class.getClassLoader(),
    new Class<?>[] { MyService.class },
    (proxyObj, method, args) -> {
        System.out.println("before: " + method.getName());
        return method.invoke(target, args);
    }
);
```

这是后续 AOP 框架（如 Spring 的 JDK 动态代理）、RPC 客户端 stub 生成的基础能力之一；只能代理接口，代理具体类需要 CGLIB 等字节码生成方案。

---

## 历史背景（简述）

2000 年距 [JDK 1.2](./jdk-1.2.md)（1998 年底，集合框架、Swing、「Java 2」品牌）约一年半。1.3 没有语法层面的大动作，重心全部放在**运行时质量**上——HotSpot 默认化、JNDI 并入核心，都是为随后几年 J2EE、Spring 等服务端生态的爆发做准备。平台命名、发布节奏见 [Java 版本历史](./java-version-history.md)。

---

## 与上一版本的衔接

| 主题 | JDK 1.2 | JDK 1.3 |
| ---- | ------- | ------- |
| 默认 VM | Classic VM（HotSpot 发布 4 个月后可选配，但非默认） | HotSpot（Classic 仍可选） |
| GC 模型 | 不分代，固定标记-清除 | 分代，Serial + Serial Old |
| 命名服务 | 无标准 API | JNDI（并入核心） |
| 代理/AOP 基础 | 无 | `java.lang.reflect.Proxy` |
| RMI / CORBA | Java IDL（ORB），尚无 RMI-IIOP | RMI 可选兼容 CORBA IIOP |
| GUI 自动化 | 无标准 API | `java.awt.Robot` |

更完整的 1.2 基线见 [JDK 1.2](./jdk-1.2.md)；下一版本见 [JDK 1.4](./jdk-1.4.md)。

---

## 参考

- [Java version history（Wikipedia）](https://en.wikipedia.org/wiki/Java_version_history)
- [HotSpot JVM 简介](./hotspot.md)
- [Java GC](./gc.md)
