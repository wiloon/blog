---
title: SOLID 面向对象设计原则
author: "-"
date: 2026-04-16T12:49:29+08:00
url: solid-principles
categories:
  - Java
tags:
  - Pattern
  - remix
  - AI-assisted
---

SOLID 是面向对象设计的五大基本原则的首字母缩写，由 Robert C. Martin（Uncle Bob）整理归纳。这五个原则是编写可维护、可扩展代码的基础。

## S — 单一职责原则 (Single Responsibility Principle, SRP)

> 一个类应该只有一个引起它变化的原因。

一个类只做一件事。如果一个类承担了多个职责，那么每个职责的变化都可能影响这个类，导致它越来越难以维护。

**反例：** 简单工厂模式中的工厂类 `Driver` 同时负责判断车型和创建所有车对象，违反了单一职责。

## O — 开闭原则 (Open-Closed Principle, OCP)

> 软件实体应该对扩展开放，对修改封闭。

添加新功能时，应该通过新增代码实现，而不是修改已有代码。详见[开闭原则](/open-closed-principle)。

**反例：** 简单工厂的 `if/else` 判断链，每新增一种产品都要修改工厂方法。

## L — 里氏替换原则 (Liskov Substitution Principle, LSP)

> 子类必须能够替换其父类，且程序行为不变。

任何使用父类的地方，换成子类后程序应该仍然正确运行。子类不应该破坏父类的契约。

**示例：** `Benze` 和 `Bmw` 都实现了 `Car` 接口，客户端代码使用 `Car` 类型，无论实际是哪种车，`drive()` 都能正确调用。

## I — 接口隔离原则 (Interface Segregation Principle, ISP)

> 客户端不应该被迫依赖它不使用的方法。

接口应该尽量细化，不要把不相关的方法放在同一个接口里。大接口应该拆分成多个小接口，让实现类只需要关心自己用到的方法。

**反例：** 一个包含 `fly()`、`swim()`、`run()` 的 `Animal` 接口，鱼类被迫实现 `fly()` 和 `run()`。

## D — 依赖倒置原则 (Dependency Inversion Principle, DIP)

> 高层模块不应该依赖低层模块，两者都应该依赖抽象；抽象不应该依赖细节，细节应该依赖抽象。

面向接口编程，而不是面向实现编程。

**示例：** 工厂模式中客户端 `Magnate` 依赖 `Car` 接口，而不是直接依赖 `Benze` 或 `Bmw`，这就是依赖倒置的体现。

---

这五个原则相互关联，共同指向同一个目标：**写出低耦合、高内聚、易于扩展和维护的代码**。
