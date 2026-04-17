---
title: 策略模式, Strategy Pattern
author: "-"
date: 2026-04-16T17:48:38+08:00
url: strategy-pattern
categories:
  - Pattern
tags:
  - Pattern
  - remix
  - AI-assisted
---

策略模式（Strategy Pattern）定义了一系列算法，把这些算法一个个封装成单独的类，使它们可以相互替换，且算法的改变不会影响使用算法的客户。

策略模式重点是封装不同的算法和行为，不同的场景下可以相互替换。策略模式是开闭原则的体现——对扩展开放，对修改关闭：新增策略时不影响其他类，且场景类只依赖抽象而不依赖具体实现。

## 示例：字符串替换策略

这里以字符串替换为例：读取一个文件后，需要替换其中的变量再输出。替换方式可能有多种，我们用策略模式来支持运行时切换。

首先，建立抽象策略类 `RepTempRule`，定义公用变量和方法：

```java
public abstract class RepTempRule {

    protected String oldString = "";

    public void setOldString(String oldString) {
        this.oldString = oldString;
    }

    protected String newString = "";

    public String getNewString() {
        return newString;
    }

    public abstract void replace() throws Exception;
}
```

现在有两个具体策略：将文本中的 `aaa` 替换成 `bbbb`，或替换成 `ccc`：

```java
public class RepTempRuleOne extends RepTempRule {

    @Override
    public void replace() throws Exception {
        newString = oldString.replaceFirst("aaa", "bbbb");
        System.out.println("this is replace one");
    }
}
```

```java
public class RepTempRuleTwo extends RepTempRule {

    @Override
    public void replace() throws Exception {
        newString = oldString.replaceFirst("aaa", "ccc");
        System.out.println("this is replace two");
    }
}
```

算法解决类，提供运行时自由选择和切换算法的能力：

```java
public class RepTempRuleSolve {

    private RepTempRule strategy;

    public RepTempRuleSolve(RepTempRule rule) {
        this.strategy = rule;
    }

    public String getNewContext(String oldString) throws Exception {
        strategy.setOldString(oldString);
        strategy.replace();
        return strategy.getNewString();
    }

    public void changeAlgorithm(RepTempRule newAlgorithm) {
        strategy = newAlgorithm;
    }
}
```

客户端调用：

```java
public class Client {

    public void testReplace() throws Exception {
        String context = "aaa is a placeholder";

        // 使用第一套替代方案
        RepTempRuleSolve solver = new RepTempRuleSolve(new RepTempRuleOne());
        System.out.println(solver.getNewContext(context));

        // 运行时切换到第二套方案
        solver.changeAlgorithm(new RepTempRuleTwo());
        System.out.println(solver.getNewContext(context));
    }
}
```

这样就达到了在运行期间自由切换算法的目的。Strategy 的核心在于抽象类的使用，使用策略模式可以在用户需要变化时，修改量很少，而且快速。

## 优点

- **可替换继承关系**：将算法封装在独立的 Strategy 类中，使得算法可以独立于 Context 改变，易于切换、易于理解、易于扩展。相比继承，算法不会被硬编码进 Context。
- **消除条件语句**：Strategy 模式提供了替代 `if-else` 条件分支选择行为的方案。当不同行为堆砌在一个类中时很难避免条件语句，将行为封装到独立 Strategy 类中可以消除这些条件语句。
- **实现的选择**：Strategy 模式可以提供相同行为的不同实现，客户可以根据时间/空间权衡取舍从不同策略中进行选择。

## 缺点

- **客户端需要了解所有策略类**：客户端必须知道各策略的区别并自行决定使用哪一个，可能需要向客户暴露具体的实现细节。
- **通信开销**：无论 ConcreteStrategy 实现的算法简单还是复杂，都共享 Strategy 定义的接口。某些简单策略可能不会用到接口传递的所有参数，导致 Context 创建了一些永远不会被用到的参数。
- **策略类数量增多**：每个策略都是一个类，策略较多时会产生大量类。可以通过享元模式在一定程度上减少对象数量。

## 适用场景

- 以不同的格式保存文件
- 以不同的算法压缩文件
- 以不同的算法截获图像
- 以不同的格式输出同样数据的图形（如曲线或柱状图）

Strategy 和 Factory 有一定类似，但 Strategy 相对简单易理解，且可以在运行时刻自由切换；Factory 的重点是创建对象。

---

> 参考：
> - <https://www.jianshu.com/p/71feb016ac05\>
> - <https://www.cnblogs.com/hollischuang/p/13186766.html\>
