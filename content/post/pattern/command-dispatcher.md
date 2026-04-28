---
title: Command Dispatcher / Command Bus
author: "-"
date: 2026-04-28T10:36:11+08:00
url: command-dispatcher
categories:
  - Pattern
tags:
  - Pattern
  - architecture
  - go
  - remix
  - AI-assisted
---

Command Dispatcher（命令分发器）和 Command Bus（命令总线）是**架构模式**，属于应用层架构设计的范畴，不在 GoF 23 种设计模式之列。

注意："Command Dispatcher" 是开发者社区的口语化称呼，没有权威模式书籍正式定义。对应的正式模式名是 EIP（企业集成模式）中的 **Content-Based Router**（见下文）。

两者不是同一个模式，Command Bus 是在 Content-Based Router 基础上增加了中间件管道的演化版本，核心差异在于**中间件管道**。

| | Command Dispatcher | Command Bus |
| --- | --- | --- |
| 核心机制 | ID → Handler 直接路由 | ID → 中间件链 → Handler |
| 中间件支持 | 无 | 有（日志、验证、事务等） |
| 复杂度 | 简单 | 较复杂 |
| 典型场景 | IoT 协议解析、游戏指令 | CQRS、DDD 应用层 |

## Command Dispatcher

核心结构：

```
收到消息 → 解析 ID → registry.get(id) → handler.Handle(data)
```

服务初始化时将每种指令的处理类注册到一个 Map。运行时收到消息后，解析出消息类型 ID，从注册表查找对应处理器并直接调用。

```go
// Handler 接口，每种指令实现一个
type Handler interface {
    Handle(data []byte) error
}

// Dispatcher 维护 id -> handler 的注册表
type Dispatcher struct {
    handlers map[uint8]Handler
}

func NewDispatcher() *Dispatcher {
    return &Dispatcher{handlers: make(map[uint8]Handler)}
}

func (d *Dispatcher) Register(id uint8, h Handler) {
    d.handlers[id] = h
}

func (d *Dispatcher) Dispatch(id uint8, data []byte) error {
    h, ok := d.handlers[id]
    if !ok {
        return fmt.Errorf("unknown command id: 0x%02X", id)
    }
    return h.Handle(data)
}

// --- 具体指令处理类 ---

type LoginHandler struct{}

func (h *LoginHandler) Handle(data []byte) error {
    fmt.Printf("处理登录指令: %x\n", data)
    return nil
}

type LocationReportHandler struct{}

func (h *LocationReportHandler) Handle(data []byte) error {
    fmt.Printf("处理位置上报: %x\n", data)
    return nil
}

// --- 初始化注册 ---

func main() {
    d := NewDispatcher()
    d.Register(0x01, &LoginHandler{})
    d.Register(0x02, &LocationReportHandler{})

    // 收到一条原始消息，解析出 id=0x02
    d.Dispatch(0x02, []byte{0x01, 0x02, 0x03})
}
```

## Command Bus

在 Dispatcher 的基础上增加了**中间件管道**，每条命令在到达 Handler 之前会依次经过所有中间件。

```
发送命令 → middleware1 → middleware2 → ... → handler.Handle(cmd)
```

中间件可以在命令执行前后插入横切逻辑（日志、参数校验、事务、限流等），且对 Handler 完全透明。

```go
// Command 是命令的抽象接口
type Command interface{}

// CommandHandler 处理具体命令
type CommandHandler interface {
    Handle(cmd Command) error
}

// Middleware 是中间件函数类型
// next 是调用链中的下一个处理函数
type Middleware func(cmd Command, next func(Command) error) error

// CommandBus 持有 handler 注册表和中间件链
type CommandBus struct {
    handlers    map[string]CommandHandler
    middlewares []Middleware
}

func NewCommandBus() *CommandBus {
    return &CommandBus{handlers: make(map[string]CommandHandler)}
}

func (b *CommandBus) Use(m Middleware) {
    b.middlewares = append(b.middlewares, m)
}

func (b *CommandBus) Register(name string, h CommandHandler) {
    b.handlers[name] = h
}

func (b *CommandBus) Dispatch(name string, cmd Command) error {
    h, ok := b.handlers[name]
    if !ok {
        return fmt.Errorf("no handler for: %s", name)
    }

    // 构建中间件调用链
    final := func(c Command) error { return h.Handle(c) }
    for i := len(b.middlewares) - 1; i >= 0; i-- {
        m := b.middlewares[i]
        next := final
        final = func(c Command) error { return m(c, next) }
    }
    return final(cmd)
}

// --- 中间件示例 ---

func LoggingMiddleware(cmd Command, next func(Command) error) error {
    fmt.Printf("[LOG] 开始处理: %T\n", cmd)
    err := next(cmd)
    fmt.Printf("[LOG] 处理完成: %T, err=%v\n", cmd, err)
    return err
}

func ValidationMiddleware(cmd Command, next func(Command) error) error {
    // 校验逻辑...
    fmt.Printf("[VALID] 校验通过: %T\n", cmd)
    return next(cmd)
}

// --- 具体命令和处理器 ---

type CreateOrderCommand struct {
    UserID  int
    Product string
}

type CreateOrderHandler struct{}

func (h *CreateOrderHandler) Handle(cmd Command) error {
    c := cmd.(CreateOrderCommand)
    fmt.Printf("创建订单: user=%d, product=%s\n", c.UserID, c.Product)
    return nil
}

// --- 初始化 ---

func main() {
    bus := NewCommandBus()
    bus.Use(LoggingMiddleware)
    bus.Use(ValidationMiddleware)
    bus.Register("CreateOrder", &CreateOrderHandler{})

    bus.Dispatch("CreateOrder", CreateOrderCommand{UserID: 42, Product: "keyboard"})
}
```

执行顺序：

```
LoggingMiddleware (前) → ValidationMiddleware (前) → CreateOrderHandler → ValidationMiddleware (后) → LoggingMiddleware (后)
```

## Content-Based Router（正式模式名）

Content-Based Router 是《Enterprise Integration Patterns》（EIP）中定义的消息路由模式，由 Gregor Hohpe & Bobby Woolf 于 2003 年出版的同名书籍中正式命名。

官网：[enterpriseintegrationpatterns.com/ContentBasedRouter](https://www.enterpriseintegrationpatterns.com/patterns/messaging/ContentBasedRouter.html)

**问题场景**：同一个入口会收到多种不同类型的消息，每种消息需要由不同的处理组件处理，如何在不耦合各处理组件的情况下将消息分发到正确目标？

**解决方案**：插入一个路由组件，检查消息内容（通常是某个字段或头信息），根据内容决定将消息转发到哪个处理通道/处理器。

```
incoming message
      ↓
[Content-Based Router]
   ├── type=login    → LoginHandler
   ├── type=location → LocationHandler
   └── type=alarm    → AlarmHandler
```

**核心特征**：

- 路由器不修改消息内容，只决定消息的去向
- 路由规则集中在路由器中维护，各处理器对路由逻辑完全无感知
- 新增消息类型时，只需修改路由器，其他组件不受影响

在 Apache Camel、Spring Integration、MassTransit 等主流集成框架中都有原生支持。

## 与 GoF Command Pattern 的关系

GoF 的 Command Pattern 意图是将请求封装为对象，支持撤销、队列、日志等操作。Command Dispatcher / Command Bus 是对其的延伸和演化：

| | GoF Command Pattern | Command Dispatcher | Command Bus |
| --- | --- | --- | --- |
| 意图 | 将请求封装为可操作对象 | 按 ID 路由到处理器 | 路由 + 中间件管道 |
| 关注点 | 撤销、队列、事务 | 动态分发、解耦 | 横切关注点、CQRS |

## 常见应用场景

- **CQRS** 架构中的 Command Bus
- **消息驱动架构**中的 Message Dispatcher
- **IoT / 车联网**协议解析服务：每种指令 ID 对应一个处理类，注册到分发器后统一路由
- **企业集成模式**（EIP）中的 Message Router

## 与策略模式的区别

两者代码结构相似（公共接口 + 多实现 + 运行时选择），但意图不同：

| | 策略模式 | Command Dispatcher |
| --- | --- | --- |
| 核心意图 | 对**同一件事**选择不同算法 | 对**不同的事**路由到不同处理器 |
| 典型例子 | 排序可换快排/归并/堆排 | 指令 0x01 → 登录处理器，0x02 → 上报处理器 |
