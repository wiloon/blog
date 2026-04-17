---
title: 适配器模式, Adapter Pattern
author: "-"
date: 2026-04-16T17:21:48+08:00
url: Adapter
categories:
  - Pattern
tags:
  - remix
  - AI-assisted
---

## 概念

通常，客户类通过类的接口访问它提供的服务。有时，现有的类可以提供客户类需要的功能，但它所提供的接口不一定是客户类所期望的——可能接口过于详细、缺少细节，或者名称不匹配。

在这种情况下，需要将现有接口转化为客户类期望的接口，从而保证对现有类的重用。适配器模式（Adapter Pattern）通过定义一个**包装类**来完成这种转化：

- **Target**：客户类期望的接口
- **Adaptee**：现有的、接口不兼容的类
- **Adapter**：包装 Adaptee，实现 Target 接口

当客户类调用 Adapter 的方法时，Adapter 内部转而调用 Adaptee 的对应方法，这个过程对客户类透明。

## 类适配器 vs 对象适配器

| | 类适配器 | 对象适配器 |
|--|--|--|
| 实现方式 | 继承 Adaptee | 组合 Adaptee |
| 灵活性 | 静态绑定，无法适配 Adaptee 子类 | 可适配 Adaptee 及其所有子类 |
| 方法重载 | 可重载 Adaptee 的方法 | 不能直接重载，但可在包装方法中修改行为 |
| 可见性 | 客户类可见 Adaptee 的 public 方法 | 客户类与 Adaptee 完全解耦 |
| Java 限制 | 仅适用于 Target 是接口（Java 单继承） | Target 可以是接口或抽象类 |

## 类适配器示例

Adapter 通过**继承** Adaptee 来复用其接口：

```java
// Target：客户类期望的接口
public interface Target {
    void sampleOperation1();
}

// Adaptee：现有的第三方类，接口不兼容
public class Adaptee {
    public void sampleOperation2() {
        System.out.println("Adaptee.sampleOperation2()");
    }
}

// Adapter：继承 Adaptee，实现 Target
public class Adapter extends Adaptee implements Target {
    @Override
    public void sampleOperation1() {
        this.sampleOperation2();
    }
}

// Client
public class Client {
    public static void main(String[] args) {
        Target target = new Adapter();
        target.sampleOperation1();
    }
}
```

## 对象适配器示例

Adapter 通过**组合** Adaptee 来复用其接口：

```java
// Target：客户类期望的接口
public interface Target {
    void sampleOperation1();
}

// Adaptee：现有的第三方类，接口不兼容
public class Adaptee {
    public void sampleOperation2() {
        System.out.println("Adaptee.sampleOperation2()");
    }
}

// Adapter：持有 Adaptee 引用，实现 Target
public class Adapter implements Target {
    private final Adaptee adaptee;

    public Adapter(Adaptee adaptee) {
        this.adaptee = adaptee;
    }

    @Override
    public void sampleOperation1() {
        adaptee.sampleOperation2();
    }
}

// Client
public class Client {
    public static void main(String[] args) {
        Adaptee adaptee = new Adaptee();
        Target target = new Adapter(adaptee);
        target.sampleOperation1();
    }
}
```
