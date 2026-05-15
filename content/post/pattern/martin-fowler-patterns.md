---
title: Martin Fowler 主要设计模式
author: "-"
date: 2026-05-15T14:40:04+08:00
lastmod: 2026-05-15T14:40:04+08:00
url: martin-fowler-patterns
categories:
  - pattern
tags:
  - pattern
  - architecture
  - remix
  - AI-assisted
---

Martin Fowler 是《重构》《企业应用架构模式》《领域特定语言》等经典书籍的作者，也是 ThoughtWorks 首席科学家。他提出或系统整理了大量在工业界广泛应用的设计模式，涵盖对象建模、企业架构和分布式系统三个层面。

本文选取其中最具代表性的几个模式进行介绍。关于企业应用架构模式中的 Repository、Unit of Work、Front Controller 等，见 [企业应用架构模式](enterprise-application-architecture-patterns)。

---

## Special Case（特殊情况）

**来源：** Patterns of Enterprise Application Architecture（2002）

### 问题

方法在遇到无法正常处理的输入时，通常有两种选择：返回 `null` 或抛出异常。两者都把处理责任推给调用方，导致 `null` 判断或 `try/catch` 散布在代码各处。

```java
// 调用方被迫到处写 null 判断
Customer customer = customerRepository.findById(id);
if (customer == null) {
    return "unknown";
}
return customer.getName();
```

### 解决方案

为"无法正常处理"的情况创建一个实现相同接口的特殊对象，让它封装默认行为。调用方无需判断，直接调用即可。

```java
public interface Customer {
    String getName();
    boolean isNull();
}

public class UnknownCustomer implements Customer {
    @Override
    public String getName() { return "Unknown"; }

    @Override
    public boolean isNull() { return true; }
}

// 仓储层返回特殊对象，而非 null
public Customer findById(long id) {
    Customer c = db.find(id);
    return c != null ? c : new UnknownCustomer();
}

// 调用方无需 null 判断
String name = customerRepository.findById(id).getName();
```

### Special Case vs Null Object

Null Object 是 Special Case 的一个特例——当特殊行为就是"什么也不做"时，就是 Null Object。Special Case 更通用：特殊对象可以有具体的默认行为，甚至代表一个有意义的领域概念（如"匿名用户""未知账户""空购物车"）。

| 模式         | 特殊行为             | 领域含义                   |
| ------------ | -------------------- | -------------------------- |
| Null Object  | 什么都不做（空操作） | 无                         |
| Special Case | 有具体的默认值或行为 | 代表一个明确的特殊领域状态 |

### 适用场景

- 某个领域概念在特定条件下存在"缺失"或"默认"状态，且这种状态有明确的业务含义
- 希望消除调用方散布的 `null` 判断，但又不想用异常处理控制流
- 典型例子：未登录用户（GuestUser）、空购物车（EmptyCart）、缺失配置（DefaultConfig）

---

## Value Object（值对象）

**来源：** Patterns of Enterprise Application Architecture（2002），后在 DDD 中进一步发展

### 问题

用基本类型（`int`、`String`）表示有意义的领域概念时，业务规则容易被绕过，类型安全缺失，相等性语义也不自然。

```java
// 金额和汇率都是 double，容易混淆
void transfer(double amount, String currency) { ... }
```

### 解决方案

将相关数据和业务规则封装为一个不可变对象，以**值相等**（所有字段相等）而非**引用相等**（内存地址相同）来判断是否相同。

```java
public final class Money {
    private final BigDecimal amount;
    private final Currency currency;

    public Money(BigDecimal amount, Currency currency) {
        this.amount = Objects.requireNonNull(amount);
        this.currency = Objects.requireNonNull(currency);
    }

    public Money add(Money other) {
        if (!this.currency.equals(other.currency)) {
            throw new IllegalArgumentException("Currency mismatch");
        }
        return new Money(this.amount.add(other.amount), this.currency);
    }

    @Override
    public boolean equals(Object o) { ... }  // 基于 amount 和 currency
}
```

### 核心特征

- **不可变**：创建后不能修改，"修改"操作返回新对象
- **值相等**：两个对象的所有字段相同则相等，不依赖引用
- **自包含业务规则**：如货币加法需要相同币种

### Value Object vs Entity

|          | Value Object               | Entity               |
| -------- | -------------------------- | -------------------- |
| 相等性   | 值相等（所有字段）         | 标识相等（ID 字段）  |
| 可变性   | 不可变                     | 可变                 |
| 典型例子 | Money、Address、Coordinate | User、Order、Product |

---

## Strangler Fig Application（绞杀者应用）

**来源：** martinfowler.com，2004 年

### 问题

遗留系统庞大、难以测试、无法整体重写。但业务无法停摆，无法一次性切换到新系统。

### 解决方案

模仿热带雨林中绞杀榕（Strangler Fig）的生长方式——榕树从宿主树的树冠开始生长，逐渐向下包裹，最终宿主树死亡后，榕树自立成树。

1. **在遗留系统旁边**构建新系统（不是替换，是并行存在）
2. 通过代理层（HTTP 网关、消息路由等）将特定功能**逐步路由**到新系统
3. 不断将旧系统的功能迁移到新系统
4. 遗留系统逐渐缩小，直到可以安全下线

```
                 ┌─────────────┐
所有请求 ──→    │  路由代理    │ ──→ 旧系统（逐渐缩小）
                 │  (Facade)   │ ──→ 新系统（逐渐增大）
                 └─────────────┘
```

### 关键要素

- **Facade（外观层）**：对外暴露统一接口，内部决定路由到新旧哪个系统
- **增量迁移**：按功能模块逐步切换，每次只迁移一小块
- **可回滚**：路由层可以随时将流量切回旧系统

### 适用场景

- 遗留单体应用向微服务架构迁移
- 大规模重写无法停机的核心系统
- 与 [Branch by Abstraction](#branch-by-abstraction抽象分支) 经常配合使用

---

## Event Sourcing（事件溯源）

**来源：** martinfowler.com，2005 年

### 问题

传统系统只保存对象的**当前状态**（最新快照），历史变化丢失。无法回答"这条订单是什么时候、由谁、为什么改变的"。

### 解决方案

不存储对象的当前状态，而是存储导致状态变化的**事件序列**。当前状态通过重放所有事件计算得出。

```
事件序列（持久化存储）：
OrderCreated { orderId: 1, items: [...], at: 10:00 }
ItemAdded    { orderId: 1, item: "book", at: 10:05 }
OrderPaid    { orderId: 1, amount: 99, at: 10:10 }

当前状态 = 重放以上所有事件
```

### 优势

- **完整审计日志**：天然记录所有历史变更，满足合规要求
- **时间旅行**：可以重建任意时间点的系统状态
- **事件驱动集成**：事件天然成为与其他系统集成的消息
- **调试能力**：生产环境问题可在测试环境完整重现

### 代价

- 读取当前状态需要重放事件（通常配合**快照**优化）
- 事件 Schema 变更（事件版本化）需要专门处理
- 系统复杂度高于 CRUD 应用

通常与 [CQRS](#cqrs-命令查询职责分离) 配合使用。

---

## CQRS（命令查询职责分离）

**来源：** martinfowler.com，基于 Bertrand Meyer 的 CQS 原则演化而来

CQRS 全称 Command Query Responsibility Segregation，将系统的**写操作（Command）**和**读操作（Query）**分离为独立的模型。

### 基本形式

```
┌──────────────────────────────────────────────────┐
│                    应用层                         │
│  Command (改变状态)  │  Query (只读，不改状态)   │
│                      │                            │
│  ┌──────────────┐    │  ┌──────────────────────┐ │
│  │  写模型       │    │  │  读模型（可独立优化） │ │
│  │  (领域对象)  │    │  │  (DTO / 投影视图)    │ │
│  └──────────────┘    │  └──────────────────────┘ │
└──────────────────────────────────────────────────┘
```

### 与 CQS 的区别

CQS（Command Query Separation）是方法级别的原则：一个方法要么修改状态（Command），要么返回数据（Query），不能两者兼顾。CQRS 将这个原则提升到**架构级别**，写模型和读模型可以使用完全不同的数据存储。

### 适用场景

- 读写比例悬殊，读写的性能需求差异大
- 读模型需要针对不同场景提供多种视图
- 与 Event Sourcing 配合时，写侧存事件，读侧维护投影（物化视图）

**注意**：Martin Fowler 本人也强调 CQRS 不应滥用——对于大多数普通 CRUD 应用，CQRS 只会增加复杂度，没有收益。

---

## Branch by Abstraction（抽象分支）

**来源：** martinfowler.com，2014 年，Paul Hammant 最先描述，Fowler 整理推广

### 问题

需要对系统中被大量代码依赖的组件进行大规模替换（如替换 ORM 框架、消息队列），但替换过程需要数周，期间代码无法合并主干。

### 解决方案

1. 在旧实现之上引入**抽象层**（接口或抽象类）
2. 让现有代码都依赖抽象层，而不是旧实现
3. 新实现与旧实现**并行开发**，都实现同一抽象
4. 逐步将调用方切换到新实现（可按模块、按比例灰度切换）
5. 旧实现全部替换完毕后，删除抽象层（如果不再需要）

```
    旧代码 ──→ 旧实现              （替换前）
    旧代码 ──→ 抽象层 ──→ 旧实现  （引入抽象）
    旧代码 ──→ 抽象层 ──→ 新实现  （切换完成）
```

### 与 Feature Toggle 的关系

Branch by Abstraction 通常配合 Feature Toggle 使用——抽象层内部根据开关决定路由到新实现还是旧实现，实现灰度切换和快速回滚。

---

## 模式关系总览

| 模式                  | 层面     | 核心思想                               | 典型场景           |
| --------------------- | -------- | -------------------------------------- | ------------------ |
| Special Case          | 对象设计 | 用特殊对象封装默认行为，消除 null 判断 | 缺失数据、默认状态 |
| Value Object          | 对象设计 | 以值相等定义对象，不可变               | 金额、地址、坐标   |
| Strangler Fig         | 架构演进 | 新旧系统并行，逐步迁移                 | 遗留系统改造       |
| Event Sourcing        | 数据存储 | 存事件而非状态，支持历史重放           | 审计、时间旅行     |
| CQRS                  | 架构设计 | 读写模型分离，各自优化                 | 高读写比差异场景   |
| Branch by Abstraction | 重构技术 | 引入抽象层，新旧实现并行替换           | 大规模组件替换     |

---

## 参考

- Martin Fowler, *Patterns of Enterprise Application Architecture*, 2002
- Martin Fowler, *Refactoring: Improving the Design of Existing Code*, 1999 / 2018
- [martinfowler.com/eaaCatalog/specialCase.html](https://martinfowler.com/eaaCatalog/specialCase.html)
- [martinfowler.com/bliki/StranglerFigApplication.html](https://martinfowler.com/bliki/StranglerFigApplication.html)
- [martinfowler.com/eaaDev/EventSourcing.html](https://martinfowler.com/eaaDev/EventSourcing.html)
- [martinfowler.com/bliki/CQRS.html](https://martinfowler.com/bliki/CQRS.html)
- [martinfowler.com/bliki/BranchByAbstraction.html](https://martinfowler.com/bliki/BranchByAbstraction.html)
