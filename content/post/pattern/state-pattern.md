---
title: 状态模式, State Pattern
author: "-"
date: 2026-04-16T18:11:56+08:00
url: state-pattern
categories:
  - Pattern
tags:
  - Pattern
  - remix
  - AI-assisted
---

状态模式（State Pattern）允许一个对象在其内部状态发生改变时改变其行为，使该对象看起来像是改变了它的类。

## 核心思想

在不使用状态模式的情况下，对象的行为往往通过大量 `if-else` 或 `switch` 判断当前状态来分支处理，导致代码臃肿、难以扩展。状态模式将每种状态封装成独立的类，对象将行为委托给当前状态对象，状态切换时只需替换状态对象即可。

## 角色

- **Context（上下文）**：持有当前状态的引用，对外暴露行为接口，将行为委托给当前状态对象处理。
- **State（抽象状态）**：定义所有具体状态共同的接口。
- **ConcreteState（具体状态）**：实现 State 接口，封装该状态下的行为，并在必要时触发状态转换。

## 示例：交通灯

交通灯有红、黄、绿三种状态，不同状态下的行为不同，且状态之间按规则流转。

抽象状态接口：

```java
public interface TrafficLightState {
    void handle(TrafficLight light);
    String getColor();
}
```

具体状态类：

```java
public class RedState implements TrafficLightState {

    @Override
    public void handle(TrafficLight light) {
        System.out.println("红灯停。");
        light.setState(new GreenState());
    }

    @Override
    public String getColor() {
        return "红";
    }
}
```

```java
public class GreenState implements TrafficLightState {

    @Override
    public void handle(TrafficLight light) {
        System.out.println("绿灯行。");
        light.setState(new YellowState());
    }

    @Override
    public String getColor() {
        return "绿";
    }
}
```

```java
public class YellowState implements TrafficLightState {

    @Override
    public void handle(TrafficLight light) {
        System.out.println("黄灯警示，请注意。");
        light.setState(new RedState());
    }

    @Override
    public String getColor() {
        return "黄";
    }
}
```

Context（上下文）类：

```java
public class TrafficLight {

    private TrafficLightState state;

    public TrafficLight() {
        this.state = new RedState();
    }

    public void setState(TrafficLightState state) {
        this.state = state;
    }

    public void change() {
        System.out.print("当前：" + state.getColor() + "灯 → ");
        state.handle(this);
    }
}
```

客户端调用：

```java
public class Client {

    public static void main(String[] args) {
        TrafficLight light = new TrafficLight();
        for (int i = 0; i < 6; i++) {
            light.change();
        }
    }
}
```

输出：

```text
当前：红灯 → 红灯停。
当前：绿灯 → 绿灯行。
当前：黄灯 → 黄灯警示，请注意。
当前：红灯 → 红灯停。
当前：绿灯 → 绿灯行。
当前：黄灯 → 黄灯警示，请注意。
```

## 优点

- **消除条件分支**：将各状态的行为分散到各自的状态类中，消除大量 `if-else` / `switch` 语句。
- **符合开闭原则**：新增状态只需添加新的 ConcreteState 类，不需要修改现有代码。
- **状态转换显式化**：状态转换逻辑集中在状态类内部，清晰可见。

## 缺点

- **类数量增多**：每个状态都是一个类，状态较多时会产生大量类。
- **状态切换逻辑分散**：状态转换逻辑分布在各个 ConcreteState 中，整体流转不够集中，需要通读所有状态类才能了解完整流程。

## 与策略模式的区别

状态模式和策略模式结构相似，但意图不同：

| | 状态模式 | 策略模式 |
|--|--|--|
| 目的 | 根据内部状态自动切换行为 | 由客户端选择并注入算法 |
| 切换方式 | 状态对象之间相互知道彼此，自行转换 | 客户端主动替换策略对象 |
| 状态间关系 | 状态之间有依赖（知道转换目标） | 策略之间相互独立 |

## 适用场景

- 对象的行为随其内部状态的变化而变化，且状态数量较多时
- 大量条件语句依赖对象状态进行分支处理时
- 典型场景：订单状态流转、游戏角色状态机、工作流审批流程、TCP 连接状态
