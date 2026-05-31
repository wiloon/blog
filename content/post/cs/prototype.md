---
title: 基于原型的编程 (Prototype-based Programming)
author: "-"
date: 2017-11-13T08:47:49+00:00
lastmod: 2026-05-15T12:20:22+08:00
url: prototype
categories:
  - development
tags:
  - AI-assisted
  - remix
---

> **注意**：本文讲的是**基于原型的编程范式**，不是 GoF 设计模式中的 [Prototype 模式](../pattern/prototype-pattern.md)。两者名字相同，但概念不同。

## 基于原型的编程是什么

基于原型的编程（Prototype-based programming）是面向对象编程的一种方式。与传统的基于类（class-based）的方式不同，它**没有 class 的概念**，对象直接从其他对象继承，又称为**基于实例的编程（Instance-based programming）**。

## 与基于类的编程的区别

**基于类的编程（如 Java、C++）：**

- 先定义 class（类），class 描述对象的结构和行为
- 再通过 class 实例化出对象
- 对象的行为由其所属的 class 决定

**基于原型的编程（如 JavaScript、Lua、Self）：**

- 没有 class，只有对象
- 对象直接从另一个对象（原型）继承属性和方法
- 可以在运行时动态修改对象，甚至修改原型

## 典型例子：JavaScript

JavaScript 是最广为人知的基于原型的语言。每个对象都有一个内部指针指向它的原型对象，属性查找会沿着原型链向上查找。

```javascript
const animal = {
    speak() { console.log("..."); }
};

const dog = Object.create(animal); // dog 的原型是 animal
dog.speak(); // 继承自 animal
```

ES6 引入的 `class` 语法只是原型继承的**语法糖**，底层仍然是原型链。

