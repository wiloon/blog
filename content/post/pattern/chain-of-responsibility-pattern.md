---
title: 责任链模式, Chain of Responsibility Pattern
author: "-"
date: 2026-04-16T18:27:55+08:00
url: chain-of-responsibility
categories:
  - Pattern
tags:
  - Pattern
  - remix
  - AI-assisted
---

责任链模式（Chain of Responsibility）将请求沿着一条处理者链传递，每个处理者决定是否处理该请求，或将其传递给链上的下一个处理者。请求的发送者无需知道最终由哪个处理者来处理，从而实现了发送者与接收者的解耦。

## 核心思想

不使用责任链时，请求方往往需要硬编码逻辑来判断应该由哪个对象处理，导致紧耦合和大量条件判断。责任链将这些处理者串联起来，请求沿链传递，直到被某个处理者处理（或到达链尾）。

## 角色

- **Handler（抽象处理者）**：定义处理请求的接口，通常包含设置下一个处理者的方法。
- **ConcreteHandler（具体处理者）**：实现处理逻辑，决定自己是否处理请求，如果不处理则转发给下一个处理者。
- **Client（客户端）**：构建责任链并向链头发起请求。

## 示例：请假审批

不同级别的请假天数由不同层级的领导审批：组长审批 1 天以内，经理审批 3 天以内，总监审批 7 天以内，超过 7 天不予批准。

抽象处理者：

```java
public abstract class Approver {

    protected Approver next;

    public Approver setNext(Approver next) {
        this.next = next;
        return next;
    }

    public abstract void approve(int days);
}
```

具体处理者：

```java
public class TeamLeader extends Approver {

    @Override
    public void approve(int days) {
        if (days <= 1) {
            System.out.println("组长批准了 " + days + " 天假。");
        } else if (next != null) {
            next.approve(days);
        }
    }
}
```

```java
public class Manager extends Approver {

    @Override
    public void approve(int days) {
        if (days <= 3) {
            System.out.println("经理批准了 " + days + " 天假。");
        } else if (next != null) {
            next.approve(days);
        }
    }
}
```

```java
public class Director extends Approver {

    @Override
    public void approve(int days) {
        if (days <= 7) {
            System.out.println("总监批准了 " + days + " 天假。");
        } else {
            System.out.println("请假 " + days + " 天，超出审批权限，不予批准。");
        }
    }
}
```

客户端构建链并发起请求：

```java
public class Client {

    public static void main(String[] args) {
        TeamLeader leader = new TeamLeader();
        Manager manager = new Manager();
        Director director = new Director();

        // 构建责任链：组长 → 经理 → 总监
        leader.setNext(manager).setNext(director);

        leader.approve(1);   // 组长批准
        leader.approve(3);   // 经理批准
        leader.approve(7);   // 总监批准
        leader.approve(10);  // 超出权限
    }
}
```

输出：

```text
组长批准了 1 天假。
经理批准了 3 天假。
总监批准了 7 天假。
请假 10 天，超出审批权限，不予批准。
```

## 两种变体

**纯责任链**：请求必须被链上某个处理者处理，且只被处理一次。

**不纯责任链**：处理者处理后请求仍可继续向下传递（如 Java Servlet 的 Filter 链、日志框架的 Appender 链）。

## 优点

- **解耦发送者与接收者**：客户端只需向链头提交请求，无需知道由谁处理。
- **灵活组合处理链**：可以在运行时动态增删处理者、调整顺序。
- **符合单一职责原则**：每个处理者只关注自己负责的那一段逻辑。

## 缺点

- **请求可能不被处理**：如果链上没有合适的处理者，请求会到达链尾后被丢弃，需要额外处理。
- **调试较困难**：请求沿链传递，出现问题时需要逐个检查处理者。
- **性能影响**：链过长时，每个请求都需要遍历较长的链。

## 适用场景

- 有多个对象可以处理同一请求，且处理者在运行时才确定
- 需要在不明确指定接收者的情况下向多个对象发出请求
- 典型场景：审批流程、HTTP 中间件/Filter、日志级别过滤、事件冒泡机制

---

> 参考：<https://refactoringguru.cn/design-patterns/chain-of-responsibility>
