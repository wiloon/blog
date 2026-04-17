---
title: 中介者模式, Mediator Pattern
author: "-"
date: 2026-04-16T18:35:16+08:00
url: mediator-pattern
categories:
  - Pattern
tags:
  - Pattern
  - remix
  - AI-assisted
---

中介者模式（Mediator Pattern）定义一个中介对象来封装一系列对象之间的交互，使各对象不需要显式地相互引用，从而降低耦合度，并可以独立地改变它们之间的交互。

## 核心思想

当系统中多个对象之间存在复杂的多对多交互时，对象之间的依赖关系会形成网状结构，难以维护。中介者模式将这种网状结构转化为星形结构——所有对象只与中介者通信，由中介者协调各对象之间的交互。

```
# 不使用中介者：网状结构
A ←→ B
A ←→ C
B ←→ C
B ←→ D
...

# 使用中介者：星形结构
A → Mediator ← B
      ↑     ↓
      C     D
```

## 角色

- **Mediator（抽象中介者）**：定义各同事对象通信的接口。
- **ConcreteMediator（具体中介者）**：实现协调逻辑，持有所有同事对象的引用。
- **Colleague（同事类）**：每个同事只知道中介者，通过中介者与其他同事交互。

## 示例：聊天室

聊天室是中介者模式的典型场景：用户之间不直接通信，而是通过聊天室（中介者）转发消息。

抽象中介者：

```java
public interface ChatRoom {
    void sendMessage(String message, User sender);
    void addUser(User user);
}
```

具体中介者：

```java
import java.util.ArrayList;
import java.util.List;

public class ChatRoomImpl implements ChatRoom {

    private final List<User> users = new ArrayList<>();

    @Override
    public void addUser(User user) {
        users.add(user);
    }

    @Override
    public void sendMessage(String message, User sender) {
        for (User user : users) {
            if (user != sender) {
                user.receive(message, sender.getName());
            }
        }
    }
}
```

同事类：

```java
public class User {

    private final String name;
    private final ChatRoom chatRoom;

    public User(String name, ChatRoom chatRoom) {
        this.name = name;
        this.chatRoom = chatRoom;
    }

    public String getName() {
        return name;
    }

    public void send(String message) {
        System.out.println(name + " 发送: " + message);
        chatRoom.sendMessage(message, this);
    }

    public void receive(String message, String from) {
        System.out.println(name + " 收到来自 " + from + " 的消息: " + message);
    }
}
```

客户端：

```java
public class Client {

    public static void main(String[] args) {
        ChatRoom room = new ChatRoomImpl();

        User alice = new User("Alice", room);
        User bob = new User("Bob", room);
        User charlie = new User("Charlie", room);

        room.addUser(alice);
        room.addUser(bob);
        room.addUser(charlie);

        alice.send("大家好！");
        bob.send("你好，Alice！");
    }
}
```

输出：

```text
Alice 发送: 大家好！
Bob 收到来自 Alice 的消息: 大家好！
Charlie 收到来自 Alice 的消息: 大家好！
Bob 发送: 你好，Alice！
Alice 收到来自 Bob 的消息: 你好，Alice！
Charlie 收到来自 Bob 的消息: 你好，Alice！
```

## 优点

- **降低耦合度**：同事类之间不直接依赖，只依赖中介者接口，网状依赖变为星形依赖。
- **集中控制交互逻辑**：对象间的交互逻辑集中在中介者中，便于理解和维护。
- **易于扩展同事类**：新增同事类时只需注册到中介者，不影响其他同事。

## 缺点

- **中介者可能过于复杂**：随着同事类增多，中介者需要处理的逻辑越来越多，可能变成"上帝类"，难以维护。

## 与观察者模式的区别

| | 中介者模式 | 观察者模式 |
|--|--|--|
| 通信方向 | 双向：同事通过中介者与其他同事通信 | 单向：Subject 通知 Observer |
| 中心角色 | 中介者主动协调 | Subject 被动广播 |
| 适用场景 | 多个对象之间复杂的多对多交互 | 一对多的事件通知 |

## 适用场景

- 多个对象之间存在复杂、难以理解的多对多依赖关系
- 一个对象引用其他很多对象，导致难以复用
- 典型场景：聊天室、航空管制塔（飞机与塔台通信而不是飞机之间直接通信）、GUI 组件协调、事件总线

---

> 参考：<https://refactoringguru.cn/design-patterns/mediator>
