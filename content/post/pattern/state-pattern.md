---
title: State 状态模式
author: "-"
date: 2017-01-23T06:47:46+00:00
lastmod: 2026-05-15T13:02:53+08:00
url: state-pattern
categories:
  - pattern
tags:
  - remix
  - AI-assisted
---
## State Pattern, 状态模式

不同的状态，不同的行为；或者说，每个状态有着相应的行为。

## 何时使用

State 模式适合"状态的切换"。因为我们经常会使用 `if-elseif-else` 进行状态切换，如果针对状态的判断切换反复出现，就要联想到是否可以采取 State 模式了。

不只是根据状态，也有根据属性。如果某个对象的属性不同，对象的行为就不一样，这点在数据库系统中出现频率比较高——经常会在数据表的尾部加上属性字段，用以标识记录中一些特殊性质，这种属性的切换又是随时可能发生的，就有可能要使用 State。

## 是否使用

"开关切换状态"和"一般的状态判断"有区别：

**一般的状态判断**：state 的值由另一个变量决定，二者没有关系。

```java
if (which == 1) state = "hello";
else if (which == 2) state = "hi";
else if (which == 3) state = "bye";
```

**开关切换状态**：state 的下一个值由当前值决定，像旋转开关一样。

```java
if (state.equals("bye"))    state = "hello";
else if (state.equals("hello")) state = "hi";
else if (state.equals("hi"))   state = "bye";
```

如果只有一个方向的切换，不一定需要 State 模式（建立很多子类会增加复杂性）；但如果同一操作在多个状态下行为各不相同，且状态数量会增长，就应该考虑 State 了。

## 示例：未使用 State 模式

TCP 连接有三个核心状态：CLOSED、LISTEN、ESTABLISHED。对同一操作，不同状态的行为完全不同：

```java
public class TCPConnection {
    private String state = "CLOSED";

    public void open() {
        if (state.equals("CLOSED")) {
            // 发送 SYN
            state = "ESTABLISHED";
        }
        // LISTEN / ESTABLISHED 状态下忽略
    }

    public void close() {
        if (state.equals("LISTEN")) {
            state = "CLOSED";
        } else if (state.equals("ESTABLISHED")) {
            // 发送 FIN
            state = "CLOSED";
        }
        // CLOSED 状态下忽略
    }

    public void acknowledge() {
        if (state.equals("LISTEN")) {
            state = "ESTABLISHED";
        } else if (state.equals("ESTABLISHED")) {
            // 处理数据 ACK
        }
        // CLOSED 状态下忽略
    }
}
```

随着状态增多，`if-else` 链会急剧膨胀，且每次新增状态都要修改所有方法。下面用 State 模式重构。

## 如何使用

State 模式需要两种类型实体：

1. **State Manager（状态管理器）**：负责持有当前状态并委托操作（上例中的 `TCPConnection`）。
1. **抽象状态父类/接口**：不同状态是继承该父类的子类。

### 第一步：建立状态父类

```java
public abstract class TCPState {
    public void open(TCPConnection c)        {}
    public void close(TCPConnection c)       {}
    public void acknowledge(TCPConnection c) {}
}
```

父类提供空实现，子类只需覆写本状态下有意义的操作。

### 第二步：实现各状态子类

```java
public class TCPClosed extends TCPState {
    @Override
    public void open(TCPConnection c) {
        // 发送 SYN，进入已建立状态
        c.setState(new TCPEstablished());
    }
}
```

```java
public class TCPListen extends TCPState {
    @Override
    public void close(TCPConnection c) {
        c.setState(new TCPClosed());
    }

    @Override
    public void acknowledge(TCPConnection c) {
        // 收到 SYN，完成握手
        c.setState(new TCPEstablished());
    }
}
```

```java
public class TCPEstablished extends TCPState {
    @Override
    public void close(TCPConnection c) {
        // 发送 FIN，关闭连接
        c.setState(new TCPClosed());
    }

    @Override
    public void acknowledge(TCPConnection c) {
        // 处理数据 ACK
    }
}
```

### 第三步：改写 State Manager

```java
public class TCPConnection {

    private TCPState state = new TCPClosed();

    public void setState(TCPState state) {
        this.state = state;
    }

    public void open()        { state.open(this); }
    public void close()       { state.close(this); }
    public void acknowledge() { state.acknowledge(this); }
}
```

至此完成重构。调用方只需调用 `open()` / `close()` / `acknowledge()`，无需关心当前状态——状态自己决定如何响应并完成跳转。

每个状态类只负责两件事：**在当前状态下如何响应某个动作**，以及**是否需要切换到下一个状态**。其他状态的逻辑完全不需要关心。状态也可以选择什么都不做（不切换），比如 `TCPClosed` 收到 `close()` 时直接忽略——父类的空实现解决了"这个状态下这个操作没意义"的问题，不需要到处写 `if (state == X) return;`。

## 优点

1. 封装转换过程（转换规则）。
1. 枚举可能的状态，需要事先确定状态种类。

状态模式可以允许客户端改变状态的转换行为，而状态机能够自动改变状态。

## 应用场景

- **银行账户**：在 Open 和 Close 状态间转换。
- **TCP 连接**：创建、侦听、关闭三个状态反复转换，每个状态的具体行为较复杂，适合使用 State。
- **邮箱 POP 账号**：start、HaveUsername、Authorized、quit 四种状态。
- **绘图工具**：用户选择不同工具（方框、直线、曲线）可看作状态切换。
- **工作流/政府 OA**：批文有未办、正在办理、正在批示、正在审核、已完成等状态。
- **网络游戏**：游戏活动有开始、开玩、正在玩、输赢等状态。

## 实质

使用状态模式前，客户端外界需要介入改变状态，而状态改变的实现是琐碎或复杂的。

使用状态模式后，客户端可以直接使用事件 Event 实现，无需关心该事件导致何种状态变化——这些由状态机等内部实现。

这是一种 Event-condition-State，状态模式封装了 condition-State 部分。

每个状态形成一个子类，每个状态只关心它的下一个可能状态，从而无形中形成了状态转换的规则。新增状态时，只需修改和定义其前一个状态。

状态转换的实现方法：

- 在每个状态中实现 `next()`，指定下一个状态。
- 设定一个 StateOwner，在其中定义 `stateEnter` 和 `stateExit` 行为。

> 参考：[设计模式之 State](http://www.jdon.com/designpatterns/designpattern_State.htm)
