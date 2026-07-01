---
title: "Make Illegal States Unrepresentable：让非法状态不可表达"
author: "-"
date: 2026-07-01T02:20:08+08:00
lastmod: 2026-07-01T02:20:08+08:00
url: make-illegal-states-unrepresentable
categories:
  - development
tags:
  - pattern
  - java
  - remix
  - AI-assisted
---

"Make illegal states unrepresentable"（让非法状态不可表达）是一句常被引用的设计口号，出自 Yaron Minsky（Jane Street）2011 年的博客文章 [Effective ML Revisited](https://blog.janestreet.com/effective-ml-revisited/)，文中专门有一节就叫「Make illegal states unrepresentable」，用一个 OCaml 的 `connection_state` 类型做 before/after 对比。核心主张是：与其允许构造出错误的状态、再靠运行时检查去堵漏洞，不如设计数据结构本身，让错误状态压根**编译不过、或者根本没有对应的值可以构造**。

## 它要解决的问题

一个常见的反模式：用一个共享结构 + 若干标志位/可空字段，去表达"实际上互斥的几种状态"。

```java
// 反例：一个类硬塞下多种状态，靠字段组合和约定表达"当前是哪种情况"
public class Order {
    private String status;       // "CREATED" / "PAID" / "SHIPPED" / "CANCELLED"
    private String paymentId;    // 只有 status = PAID 之后才该有值
    private String trackingNo;   // 只有 status = SHIPPED 之后才该有值
    private String cancelReason; // 只有 status = CANCELLED 才该有值
}
```

这段代码里，"没付款却有 `trackingNo`""状态是 `CANCELLED` 但 `paymentId` 和 `cancelReason` 同时非空"这些**本不该存在**的组合，在类型系统眼里都是合法值——编译器完全放行，只能靠人读代码、写注释、加运行时校验去维持"约定"。约定总有被忘记、被破坏的一天：少写一个 if、漏掉一次校验，非法组合就悄悄溜进了生产数据。

## 换一种设计：让非法组合无法被构造

用判别联合（sum type / discriminated union）把互斥状态拆成结构不同的类型，而不是同一个类型里的字段组合：

```java
// Java 17+：sealed + record，穷尽状态，非法组合无法构造
public sealed interface Order permits Created, Paid, Shipped, Cancelled {}

public record Created(String orderId) implements Order {}
public record Paid(String orderId, String paymentId) implements Order {}
public record Shipped(String orderId, String paymentId, String trackingNo) implements Order {}
public record Cancelled(String orderId, String cancelReason) implements Order {}
```

`Created` 这个类型上根本没有 `trackingNo` 字段可以填——不是"运行时校验它必须为空"，而是"这个状态的类型里压根没有这个位置"。配合穷尽 `switch`，编译器还会在你漏处理某个分支时报错：

```java
String describe(Order order) {
    return switch (order) {
        case Created c -> "created: " + c.orderId();
        case Paid p -> "paid: " + p.paymentId();
        case Shipped s -> "shipped: " + s.trackingNo();
        case Cancelled c -> "cancelled: " + c.cancelReason();
        // 少写一个 case，编译不通过——不会等到运行时才发现漏了分支
    };
}
```

这就是"让非法状态不可表达"：把校验的责任从"程序员记得写 if"转移到"类型系统/ 编译器帮你挡住"。

## 常见的具体落地手段

这不是单一语言特性，而是一类做法，在不同语言里有不同的实现：

- **判别联合 / Sum Type**：Rust 的 `enum`、TypeScript 的联合类型、Java 的 `sealed` 接口 + `record`（见 [JDK 17](../language/java/jdk-17.md) 中 `sealed` 小节的 `PaymentResult` 例子）。
- **[Parse, don't validate](https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/)**（Alexis King，2019）：更进一步的说法——不要在多处反复"校验"同一份数据，而是"解析"一次，把校验结果编码进类型里（比如把 `String` 解析成 `NonEmptyString` 类型），之后类型系统会替你记住"这份数据已经校验过"，不需要再校验第二次。
- **类型状态模式（Typestate pattern）**：让对象在不同生命周期阶段拥有不同的类型，编译期阻止"在错误阶段调用方法"（比如一个未 `connect()` 的连接对象，类型上就没有 `send()` 方法）。
- **`Optional` / 可空类型**：用类型强制调用方处理"值可能不存在"，而不是允许 `null` 悄悄流过几层调用才在某处炸出 `NullPointerException`。

## 和相关概念的关系

- **[Fail-fast](./fail-fast.md)**：两者都关心"非法状态"，但作用的阶段不同。fail-fast 是**运行时**策略——非法状态一旦出现，尽早、显眼地报错；"让非法状态不可表达"是**设计期**策略——从类型结构上让非法状态压根不存在，无需等到运行时才检测。二者互补：能在类型层面挡住的，优先用类型挡；类型挡不住的（比如跨系统边界的输入），退而求其次用 fail-fast 在运行时尽早拦截。
- **[Fault-tolerance](./fault-tolerance.md)**：关注系统边界之外如何容错、降级，与本文讨论的"内部数据建模"是不同层面的问题。
- **契约式设计（Design by Contract）**：前置/后置条件是运行时校验，"让非法状态不可表达"是把尽可能多的契约提前编码进类型，减少需要运行时校验的契约数量。

一句话总结：能用类型系统挡住的错误，就不要留到运行时靠人记住的约定去挡。
