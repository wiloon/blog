---
title: Java 抽象类与接口
author: "-"
date: 2012-06-03T02:35:17+00:00
lastmod: 2026-06-20T23:07:27+08:00
url: abstract-class-and-interface
aliases:
  - java-抽象类接口
categories:
  - language
tags:
  - java
  - remix
  - AI-assisted
---

> 原文参考：[abstract class 和 interface 的区别](http://dev.yesky.com/436/7581936.shtml)（天极网，约 2004）。下文在保留原意的基础上整理格式；Java 8 起接口支持 `default`/`static` 方法，见 [JDK 8](./jdk-8.md) 与文末说明。

## 概述

在 Java 中，`abstract class` 与 `interface` 都用于抽象类型定义，语法上相似，甚至有时可以互换，但二者在继承模型、默认行为与设计理念上差异明显。选型往往反映对问题领域与设计意图的理解是否到位。

## 快速对比

| 维度 | 抽象类 | 接口 |
| ---- | ------ | ---- |
| 继承 / 实现 | `extends`，单继承 | `implements`，可多实现 |
| 构造函数 | 可以有 | 不能有 |
| 实例字段 | 可以有 | 传统上仅 `public static final` 常量（一般不定义字段） |
| 方法 | 可有抽象与非抽象方法 | 传统上方法均为 `public abstract`；Java 8+ 可有 `default`/`static` |
| 访问修饰 | 方法可为任意修饰符 | 方法默认 `public` |
| 设计理念 | 常表示 **is-a**（本质同一类事物） | 常表示 **like-a** / 契约（具备某种能力） |

## 理解抽象类

`abstract class` 与 `interface` 都用于定义「抽象体」——注意此处「抽象类」是面向对象概念，不等同于关键字 `abstract class`。

在面向对象中，并非所有类都对应可实例化的具体对象。若类中信息不足以描述一个具体对象，即为抽象类。它往往表征问题领域中的抽象概念，例如图形编辑软件里的「形状」：圆、三角形是具体概念，「形状」在问题域中不存在对应实体，故抽象类不可实例化。

抽象类主要用于**类型隐藏**：固定一组行为的抽象描述，具体实现由派生类完成。模块依赖稳定的抽象体，符合开闭原则（OCP）。

## 语法层面的差异

以名为 `Demo` 的类型为例：

```java
abstract class Demo {
    abstract void method1();
    abstract void method2();
}
```

```java
interface Demo {
    void method1();
    void method2();
}
```

在 `abstract class` 中可以有数据成员和非 `abstract` 方法；在 `interface` 中（Java 7 及以前）只能有 `static final` 常量，方法均为抽象。从这个意义上说，interface 可视为一种特殊的 abstract class。

二者都可体现「design by contract」，但使用上仍有区别：

1. **继承 vs 实现**：类只能 `extends` 一个类，但可实现多个 interface（Java 对多继承的折中）。
2. **默认行为**：abstract class 可在父类中给出方法的默认实现；经典 interface 不能（Java 8 之前需委托等变通；Java 8+ 可用 `default` 方法，见下文）。

若 interface 不能提供默认实现，接口演进（新增方法）会让所有实现类必须修改，或在每个派生类重复相同逻辑，违反「one rule, one place」。因此在能否集中维护默认行为上，abstract class 往往更省事——interface 在 Java 8 后部分缓解了这一矛盾。

## 设计理念：is-a 与 like-a

语法差异相对表层。更本质的是二者反映的设计关系：

- **abstract class**：体现继承，父类与子类之间宜为 **is-a**（概念本质相同）。
- **interface**：实现类不必与接口在概念上同类，只需满足接口定义的**契约**。

### 示例：Door 与 Alarm

初始需求：`Door` 有 `open()`、`close()`。

```java
abstract class Door {
    abstract void open();
    abstract void close();
}
```

```java
interface Door {
    void open();
    void close();
}
```

子类可 `extends` 或 `implements` 上述 `Door`，表面差别不大。

若 `Door` 还需**报警**能力，常见错误是把 `alarm()` 直接加进 `Door`：

```java
abstract class Door {
    abstract void open();
    abstract void close();
    abstract void alarm();
}
```

这违反**接口隔离原则（ISP）**：把「门」与「报警器」两个概念绑在一起，仅依赖 `Door` 的模块也会因报警 API 变化而改动。

更合理的拆分：open/close 与 alarm 分属不同抽象。Java 不支持多类继承，两个概念不能都用 abstract class 表达；若都用 interface，又难以体现「AlarmDoor **是** Door」。

若领域上 AlarmDoor 本质是 Door，同时具备报警能力，可写成：

```java
abstract class Door {
    abstract void open();
    abstract void close();
}

interface Alarm {
    void alarm();
}

class AlarmDoor extends Door implements Alarm {
    void open() { /* ... */ }
    void close() { /* ... */ }
    void alarm() { /* ... */ }
}
```

这能同时表达 **is-a**（Door）与 **like-a / 能力**（Alarm）。若 AlarmDoor 本质是报警器而附带门的操作，则 abstract class 与 interface 的角色应对调。

**经验**：abstract class 偏 **is-a**；interface 偏 **like-a**（或纯契约），具体以领域建模为准。

## 小结

1. 类单继承，可多实现 interface。
2. abstract class 可有字段与非抽象方法；interface 传统上仅常量 + 抽象方法（Java 8+ 另有 `default`/`static`）。
3. 设计理念：abstract class → is-a；interface → like-a / 契约。
4. 实现类须实现所有抽象方法；abstract class 中可有非抽象方法。
5. interface 字段默认 `public static final` 且须赋初值。
6. interface 方法默认 `public abstract`（Java 8+ 的 `default`/`static` 除外）。

## Java 8 及以后

自 Java 8 起，interface 可声明：

- **`default` 方法**：带方法体的实例方法，实现类可继承或覆盖，便于接口演进而不破坏旧实现类。
- **`static` 方法**：接口上的工具方法。

因此上文关于「interface 不能有默认行为」主要针对 Java 7 及经典写法；现代代码中 interface 与 abstract class 的边界进一步模糊，选型仍应优先看 **is-a / 契约** 与 **是否需要共享状态与构造逻辑**，而非仅看语法清单。

函数式接口（Lambda 目标类型）见 [Java 8 函数式接口](../../other/functional-interface.md)。

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-06-20 | 重命名为 `abstract-class-and-interface.md`；url 改为 `abstract-class-and-interface`；保留 `java-抽象类接口` 别名；整理标题与代码块；补充 Java 8 default 说明 | 文件名英文化；格式与现行 Java 版本对齐 |
