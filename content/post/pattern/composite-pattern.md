---
title: 组合模式, Composite Pattern
author: "-"
date: 2026-04-16T17:00:10+08:00
url: composite-pattern
categories:
  - Pattern
tags:
  - remix
  - AI-assisted
---

## 概念

组合模式（Composite Pattern）将对象组合成**树状层次结构**，使客户端对单个对象（叶子节点）和组合对象（容器节点）具有**一致的访问方式**。

核心思想：部分与整体的统一接口。

**角色：**

- **Component**：抽象组件，定义叶子和容器的公共接口
- **Leaf**：叶子节点，没有子节点，实现具体操作
- **Composite**：容器节点，包含子组件，将操作委托给子节点

## 示例：文件系统

文件系统是 Composite 模式的经典场景——文件夹可以包含文件或其他文件夹，但对外都提供统一的 `getSize()` 接口。

```java
// Component
public interface FileSystemNode {
    String getName();
    long getSize();
    void print(String indent);
}
```

```java
// Leaf
public class File implements FileSystemNode {
    private final String name;
    private final long size;

    public File(String name, long size) {
        this.name = name;
        this.size = size;
    }

    @Override
    public String getName() {
        return name;
    }

    @Override
    public long getSize() {
        return size;
    }

    @Override
    public void print(String indent) {
        System.out.println(indent + "📄 " + name + " (" + size + " bytes)");
    }
}
```

```java
// Composite
public class Directory implements FileSystemNode {
    private final String name;
    private final List<FileSystemNode> children = new ArrayList<>();

    public Directory(String name) {
        this.name = name;
    }

    public void add(FileSystemNode node) {
        children.add(node);
    }

    public void remove(FileSystemNode node) {
        children.remove(node);
    }

    @Override
    public String getName() {
        return name;
    }

    @Override
    public long getSize() {
        return children.stream()
                       .mapToLong(FileSystemNode::getSize)
                       .sum();
    }

    @Override
    public void print(String indent) {
        System.out.println(indent + "📁 " + name + "/");
        for (FileSystemNode child : children) {
            child.print(indent + "  ");
        }
    }
}
```

```java
// Client
public class Client {
    public static void main(String[] args) {
        Directory root = new Directory("root");

        Directory src = new Directory("src");
        src.add(new File("Main.java", 1200));
        src.add(new File("Utils.java", 800));

        Directory resources = new Directory("resources");
        resources.add(new File("config.yml", 300));
        resources.add(new File("banner.txt", 50));

        root.add(src);
        root.add(resources);
        root.add(new File("README.md", 500));

        root.print("");
        System.out.println("Total size: " + root.getSize() + " bytes");
    }
}
```

输出：

```text
📁 root/
  📁 src/
    📄 Main.java (1200 bytes)
    📄 Utils.java (800 bytes)
  📁 resources/
    📄 config.yml (300 bytes)
    📄 banner.txt (50 bytes)
  📄 README.md (500 bytes)
Total size: 2850 bytes
```

客户端调用 `root.getSize()` 和 `file.getSize()` 的方式完全相同，无需区分是文件夹还是文件。

## 适用场景

- **树形结构**：文件系统、组织架构、菜单、DOM 树
- **需要统一处理叶子和容器**：无论节点类型，调用方式一致
- **递归操作**：遍历、统计、渲染整棵树

## 与其他模式的关系

| 模式 | 关系 |
|------|------|
| [Builder](/builder-pattern) | Builder 有时用于构建 Composite 树结构 |
| Iterator | 可用于遍历 Composite 树 |
| Visitor | 可在不修改 Composite 结构的前提下添加新操作 |
| Decorator | 与 Composite 都依赖递归组合，但 Decorator 只有一个子节点 |

---

> 参考：[https://refactoringguru.cn/design-patterns/composite](https://refactoringguru.cn/design-patterns/composite)
