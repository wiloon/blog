---
title: Builder 模式与 Factory Method 模式的对比
author: "-"
date: 2012-10-12T08:26:55+00:00
lastmod: 2026-05-15T11:58:08+08:00
url: builder-factory
categories:
  - development
tags:
  - Pattern
  - remix
  - AI-assisted

aliases:
  - /p4449/
---

> 原文：<http://www.cnblogs.com/shenfx318/archive/2007/01/28/632724.html>
> 代码示例为 C#。

Builder 与 Factory Method 同属 GoF 创建型模式，初学者容易混淆。本文通过将 Builder 模式一步步演化为 Factory Method，探讨两者的本质关系。

> 注：本文讨论的 Factory 指**工厂方法（Factory Method）**，不是抽象工厂（Abstract Factory）。

## Builder 模式的标准结构

Builder 模式由四个角色构成：抽象 Builder、具体 Builder、Director（指导者）、Product。

```csharp
public interface IBuilder
{
    void BuildPart1();
    void BuildPart2();
    Product GetResult();
}

public class BuilderA : IBuilder
{
    private Product product;

    public void BuildPart1()
    {
        product = new Product();
        product.Add("Part1 build by BuilderA");
    }

    public void BuildPart2()
    {
        product.Add("Part2 build by BuilderA");
    }

    public Product GetResult() { return product; }
}

// Director 封装构建顺序
public class Director
{
    public void Construct(IBuilder builder)
    {
        builder.BuildPart1();
        builder.BuildPart2();
    }
}
```

客户端调用：

```csharp
Director director = new Director();
IBuilder builder = new BuilderB();
director.Construct(builder);
Product product = builder.GetResult();
```

## 逐步演化为 Factory Method

### 第一步：合并 Director 到 Builder

Director 只是按固定顺序调用 Builder 的方法，如果构建顺序稳定，这个独立类显得多余。把 `Construct()` 合并进 Builder：

```csharp
// 客户端
IBuilder builder = new BuilderB();
builder.Construct();          // 合并前需要显式调用
Product product = builder.GetResult();
```

### 第二步：合并 Construct 与 GetResult

客户实例化 Builder 就是为了得到产品，`Construct` 与 `GetResult` 可以合并：

```csharp
public class BuilderA : IBuilder
{
    private Product product;

    private void BuildPart1() { ... }
    private void BuildPart2() { ... }

    public Product GetResult()
    {
        BuildPart1();   // 构建顺序内聚在此
        BuildPart2();
        return product;
    }
}
```

构建步骤对客户不可见，改为 `private`。

### 第三步：结果

```csharp
public Product Create()
{
    BuildPart1();
    BuildPart2();
    return product;
}
```

此时类图与 Factory Method **几乎完全相同**，仅名称不同。

## 两者的本质关系

通过以上演化可以看出：

- Builder 的核心价值在于**多步骤构建复杂对象，且构建步骤本身面临变化**。当构建步骤稳定、且客户不关心构建过程时，Builder 与 Factory Method 并无本质区别。
- `StringBuilder` 是实际中省略 Director 的典型例子。
- 应对"部件变化"时，两种模式都可以通过**扩展子类**来遵循 OCP，没有谁更具优势。

**真正的区别**在于使用场景的侧重：

|          | Builder                      | Factory Method       |
| -------- | ---------------------------- | -------------------- |
| 侧重点   | 复杂对象的**分步骤构建过程** | 决定**创建哪种产品** |
| Director | 可选，封装构建顺序           | 无                   |
| 适用场景 | 构建步骤本身需要变化或复用   | 产品类型需要变化     |
