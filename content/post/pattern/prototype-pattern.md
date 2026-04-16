---
title: 原型模式, Prototype Pattern
author: "-"
date: 2026-04-16T18:44:26+08:00
url: prototype-pattern
categories:
  - Pattern
tags:
  - Pattern
  - remix
  - AI-assisted
---

原型模式（Prototype Pattern）是一种创建型模式，通过复制（克隆）一个已有对象来创建新对象，而不是通过 `new` 重新实例化。

## 核心思想

当创建一个对象的代价较大（如需要复杂初始化、数据库查询、网络请求等）时，可以先创建一个原型对象，后续通过克隆该原型来快速获得新对象。

## 角色

- **Prototype（抽象原型）**：声明克隆方法 `clone()`。
- **ConcretePrototype（具体原型）**：实现克隆方法，返回自身的副本。
- **Client（客户端）**：通过调用原型的克隆方法来创建新对象。

## 浅克隆与深克隆

| | 浅克隆（Shallow Clone） | 深克隆（Deep Clone） |
|--|--|--|
| 基本类型字段 | 复制值 | 复制值 |
| 引用类型字段 | 复制引用（共享对象） | 递归复制，独立对象 |
| 修改互不影响 | ❌ 引用字段会互相影响 | ✅ 完全独立 |

## 示例：细胞克隆

Java 通过实现 `Cloneable` 接口来支持浅克隆：

```java
public class Cell implements Cloneable {

    private String cellWall;       // 细胞壁
    private String cellMembrane;   // 细胞膜
    private String cellularTissue; // 细胞组织

    public String getCellWall() { return cellWall; }
    public void setCellWall(String cellWall) { this.cellWall = cellWall; }

    // 其他 getter/setter 省略

    @Override
    public Cell clone() {
        try {
            return (Cell) super.clone();
        } catch (CloneNotSupportedException e) {
            throw new InternalError(e.getMessage());
        }
    }
}
```

客户端使用：

```java
public class Client {

    public static void main(String[] args) {
        // 创建原型细胞
        Cell cell = new Cell();
        cell.setCellWall("cell wall 1");

        // 克隆原型细胞
        Cell clonedCell = cell.clone();

        System.out.println(cell == clonedCell);                    // false，是不同对象
        System.out.println(cell.getCellWall().equals(clonedCell.getCellWall())); // true，值相同
    }
}
```

## 深克隆示例

当对象包含引用类型字段时，需要手动实现深克隆：

```java
public class DeepCell implements Cloneable {

    private String name;
    private List<String> components; // 引用类型

    @Override
    public DeepCell clone() {
        try {
            DeepCell copy = (DeepCell) super.clone();
            // 手动深克隆引用类型字段
            copy.components = new ArrayList<>(this.components);
            return copy;
        } catch (CloneNotSupportedException e) {
            throw new InternalError(e.getMessage());
        }
    }
}
```

## 优点

- **性能好**：避免重复执行昂贵的初始化操作，直接克隆已有对象。
- **简化对象创建**：客户端无需知道具体类，只需调用 `clone()`。
- **动态增减产品**：运行时可以注册和取消注册原型对象。

## 缺点

- **深克隆实现复杂**：当对象结构嵌套较深时，深克隆的实现较为繁琐。
- **必须实现克隆接口**：每个需要克隆的类都要实现 `Cloneable`，侵入性较强。

## 适用场景

- 创建对象的成本很高（如从数据库加载、复杂计算）
- 需要创建大量相似对象
- 希望避免与具体类耦合，通过克隆动态获取对象
- 典型场景：游戏中的敌人生成、文档模板复制、配置对象复制
