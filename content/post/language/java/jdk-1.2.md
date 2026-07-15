---
title: JDK 1.2
author: "-"
date: 2026-07-14T22:56:38+08:00
lastmod: 2026-07-15T04:28:17+08:00
url: jdk-1-2
categories:
  - language
tags:
  - java
  - jdk
  - hotspot
  - remix
  - AI-assisted
---

JDK 1.2（对外称 **Java 2 Platform, Standard Edition, v1.2**，代号 **Playground**）于 **1998 年 12 月 8 日**发布，是 [JDK 1.1](./jdk-1.1.md) 之后的一次「平台级」大版本——类库规模扩大近三倍（约 1520 个类、59 个包），并首次启用 **Java 2** 品牌。命名与后续演变见 [Java 版本历史](./java-version-history.md)。

## 版本号说明

| 维度 | JDK 1.2 |
| ---- | ------- |
| 对外名称 | Java 2 SE 1.2 / JDK 1.2 |
| 代号 | Playground |
| `java.version` | `1.2.x` |
| class major version | 46 |
| 上一版本 | [JDK 1.1](./jdk-1.1.md) |
| 下一版本 | [JDK 1.3](./jdk-1.3.md) |

「Java 2」中的 **2** 指平台代际（1.2 这次大改），并非版本号跳到了 2.0；这一代还拆出了 J2SE / J2EE / J2ME 三个平台方向。完整命名脉络见 [Java 版本历史](./java-version-history.md)。

## 概览

### 语言

- **`strictfp`** 关键字：约束浮点运算严格遵循 IEEE 754，保证跨平台一致性；这个「严格模式 vs. 默认模式」的区分后来被认为没必要，[JDK 17](./jdk-17.md) 的 JEP 306 让所有浮点运算恢复为始终严格，`strictfp` 从此变成没有实际效果的保留字（详见下文「与现代 Java 的关系」）

### 类库

- **集合框架**（`java.util.Collection` / `List` / `Set` / `Map` 等）：统一的容器体系，`ArrayList`、`HashMap`、`HashSet` 等新增实现；1.0/1.1 的 `Vector`、`Hashtable` 被改造为实现 `List` / `Map` 接口以便互操作（详见 [Collection List Set Map 区别](./collection-list-set-map-区别.md)）
- **Swing**（`javax.swing`）并入核心，与 AWT、Java 2D、Accessibility、Drag and Drop 一起构成 **JFC**（Java Foundation Classes）
- **`java.lang.ref`**：软引用（`SoftReference`）、弱引用（`WeakReference`）、虚引用（`PhantomReference`），配合 `ReferenceQueue` 提供比 `finalize()` 更可控的对象回收前/回收后通知机制
- **Java 2D API**（`java.awt.geom` 等）：矢量图形、坐标变换、复杂渲染
- **拖放 API**（`java.awt.dnd`）：跨组件、跨应用的拖放交互
- **Accessibility API**（`javax.accessibility`）：屏幕阅读器等辅助技术支持
- **Java IDL**（`org.omg.CORBA`）：内置 CORBA ORB，是后续 RMI-IIOP（[JDK 1.3](./jdk-1.3.md)）的基础
- **安全模型重写**：`java.security.Policy` / `ProtectionDomain` 引入**细粒度、可配置**的权限模型，取代 1.1「Applet 沙箱 vs. 本地代码完全信任」的二元划分
- **Java Plug-in**：让浏览器脱离自带（常常过时）的 JVM，改用独立安装、可控版本的 JRE 运行 Applet

### JVM 与性能

- 内置**改进版 JIT 编译器**——但仍是 Classic VM 自带的实现，**不是 HotSpot**（HotSpot 此时尚未发布，详见下文「与 HotSpot 的关系」）
- 默认虚拟机依旧是 Classic VM；HotSpot 要到 [JDK 1.3](./jdk-1.3.md) 才成为默认项

### 1.2 尚未具备（后续版本才加入）

| 能力 | 大致引入版本 |
| ---- | ------------ |
| HotSpot 成为默认 VM | 1.3 |
| RMI 可选兼容 CORBA IIOP | 1.3 |
| JNDI 并入核心 | 1.3 |
| `assert`、NIO、标准正则 | 1.4 |
| 泛型、enum、for-each、JUC | 5 |

---

## 集合框架

1.0/1.1 只有 `Vector`、`Hashtable`、`Stack` 等各自为政的容器类，缺少统一抽象。1.2 引入的集合框架用一组接口（`Collection`、`List`、`Set`、`Map`）加多种实现（`ArrayList`、`LinkedList`、`HashSet`、`TreeSet`、`HashMap`、`TreeMap`）统一了这块：

```java
List<String> names = new ArrayList<>();
names.add("alice");

Map<String, Integer> ages = new HashMap<>();
ages.put("alice", 30);
```

`Vector` 和 `Hashtable` 被保留并改造为实现 `List` / `Map`，新旧代码可以互相传递；但新代码此后基本改用 `ArrayList` / `HashMap` 等非同步实现以换取性能。接口与实现的对比见 [Collection List Set Map 区别](./collection-list-set-map-区别.md)。

---

## Swing 与 JFC

1.1 的 AWT 是**重量级**组件，依赖操作系统原生 peer，观感因平台而异。1.2 引入的 **Swing**（`javax.swing`）改为**轻量级**组件，自行绘制外观，支持可插拔观感（Pluggable Look and Feel）：

```java
JFrame frame = new JFrame("Demo");
frame.add(new JButton("Click me"));
frame.pack();
frame.setVisible(true);
```

Swing 与 AWT 事件模型（[JDK 1.1](./jdk-1.1.md#awt-委托事件模型) 引入的监听器机制）保持一致，加上 Java 2D、Drag and Drop、Accessibility，一起构成 **JFC**（Java Foundation Classes）。

---

## java.lang.ref：软/弱/虚引用

1.2 之前，唯一影响回收时机的钩子只有已经声名狼藉的 `finalize()`。`java.lang.ref` 提供三种强度递减的引用，让程序能感知、甚至部分参与对象的回收过程：

| 引用类型 | 回收时机 | 典型用途 |
| ---- | ---- | ---- |
| `SoftReference` | 内存不足时才回收 | 内存敏感的缓存 |
| `WeakReference` | 下一次 GC 即可回收，不管内存是否紧张 | `WeakHashMap`、监听器注册表，避免内存泄漏 |
| `PhantomReference` | 对象已被回收，仅用于收到通知 | 比 `finalize()` 更可控的清理钩子，配合 `ReferenceQueue` |

这套机制本身不属于任何一种收集器算法，是**收集器之上**的一层通用回收通知接口——无论 Classic VM 的固定标记-清除，还是后来 HotSpot 的分代收集器，都要支持这三种引用语义。

---

## 与 HotSpot 的关系

容易搞混的一点：**JDK 1.2 发布时并没有 HotSpot。**

| 时间 | 事件 |
| ---- | ---- |
| 1998-12 | JDK 1.2 发布，默认（且唯一）VM 仍是 **Classic VM**，内置一个改进过的 JIT |
| 1999-04 | **HotSpot** 以独立产品 **Java HotSpot Performance Engine** 首次发布，可选配合 JDK 1.2 使用（需额外下载安装，不改变 1.2 的默认 VM） |
| 2000-05 | [JDK 1.3](./jdk-1.3.md) 发布，HotSpot 才成为**默认** VM |

也就是说，1.2 与 HotSpot 的关系仅仅是「**发布 4 个月后，可以选配**」，而不是「1.2 自带 HotSpot」。1.2 本身的 GC 依旧是 Classic VM 那套固定的单线程、非分代标记-清除收集器，跟 [JDK 1.0](./jdk-1.0.md#垃圾回收gc)、[JDK 1.1](./jdk-1.1.md#垃圾回收gc) 相比没有变化；GC 真正的转折点（分代模型、Serial 收集器）要到 JDK 1.3 默认切换到 HotSpot 之后才发生，详见 [JDK 1.3](./jdk-1.3.md#垃圾回收) 与 [HotSpot](./hotspot.md#历史)。

---

## 安全模型重写

1.1 的安全模型比较粗糙：本地代码完全信任，Applet 代码强制关进沙箱，两者之间没有过渡地带。1.2 引入 `java.security.Policy` 与 `ProtectionDomain`，允许按**代码来源 + 签名者**配置细粒度权限（读写指定文件、连接指定主机等），不再是非黑即白：

```java
// policy 文件片段：授予来自指定 codebase 的代码读某个属性的权限
grant codeBase "file:${java.home}/lib/ext/*" {
    permission java.util.PropertyPermission "user.home", "read";
};
```

这套基于 Policy 的安全架构一直延续到今天的 HotSpot（`SecurityManager` 本身在 [JDK 17](./jdk-17.md) 起被标记废弃，此后版本陆续移除，但 Policy/Permission 的设计思路正是从 1.2 开始的）。

---

## strictfp 与现代 Java 的关系

1.2 之前，Java 的浮点运算允许某些平台使用比 IEEE 754 更宽的中间精度（`double extended`，常见于 x86 的 `x87` 浮点单元），同一段代码在不同 CPU 上算出的结果可能有细微差异。`strictfp` 关键字（可加在类、接口、方法上）就是为了解决这个问题：加了它，浮点运算强制严格遵循 IEEE 754，跨平台结果完全一致；不加则由 JVM 自行决定精度。

这个「严格模式 / 默认模式」二选一的设计，多年后被认为没有必要——**JDK 17（JEP 306，Restore Always-Strict Floating-Point Semantics）把它彻底反过来**：不再区分两种模式，所有浮点运算**始终**严格遵循 IEEE 754。也就是说：

- `strictfp` 关键字在语法上**仍然存在**（Java 26 等现代版本一样能写、能编译），是保留字，不会报错
- 但从 JDK 17 起，它**不再有任何实际效果**——不写这个关键字，浮点运算也已经是严格模式了
- 保留关键字本身是为了不破坏已经写了 `strictfp` 的旧代码（源码兼容），纯粹的历史遗留

这也是 Java 版本演进里比较少见的例子：一个关键字没有被移除或废弃（deprecated），而是**功能被「追平」到默认行为，关键字本身变成没用但合法的写法**。详见 [JDK 17](./jdk-17.md)（JEP 306 一节）。

---

## 历史背景（简述）

1998 年底距 1997 年的 1.1 约一年半。1.2 是 Java 从「Applet 语言」向「通用应用平台」转型的关键一步：集合框架、Swing、细粒度安全模型，都是企业级和桌面应用真正需要的基础设施。也正是从这一版起，Sun 用「**Java 2**」品牌与「**J2SE / J2EE / J2ME**」三分天下的叙事，替代了此前简单的版本号递增。平台命名、发布节奏见 [Java 版本历史](./java-version-history.md)。

---

## 与上一版本的衔接

| 主题 | JDK 1.1 | JDK 1.2 |
| ---- | ------- | ------- |
| 容器 | `Vector`、`Hashtable`、`Stack` | 集合框架（`List`/`Set`/`Map` + 新实现） |
| GUI 组件 | 重量级 AWT | 轻量级 Swing（JFC） |
| 引用语义 | 仅 `finalize()` | 软/弱/虚引用（`java.lang.ref`） |
| 安全模型 | 沙箱 vs. 完全信任二元制 | 基于 Policy 的细粒度权限 |
| CORBA 互操作 | 无 | Java IDL（ORB），为 1.3 的 RMI-IIOP 打基础 |
| 默认 VM | Classic VM | 仍是 Classic VM（HotSpot 4 个月后才可选配） |

更完整的 1.1 基线见 [JDK 1.1](./jdk-1.1.md)；下一版本见 [JDK 1.3](./jdk-1.3.md)。

---

## 参考

- [Java version history（Wikipedia）](https://en.wikipedia.org/wiki/Java_version_history)
- [HotSpot JVM 简介](./hotspot.md)
- [Collection List Set Map 区别](./collection-list-set-map-区别.md)

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-07-15 | url 改为 `jdk-1-2` | URL 含 `.` 时 Cloudflare 误判 MIME，页面无法打开 |
