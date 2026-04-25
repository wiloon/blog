---
title: JDK 8 新特性
author: "-"
date: 2026-04-25T10:10:10+08:00
url: jdk8-new-features
categories:
  - language
tags:
  - java
  - jdk
  - remix
  - AI-assisted
---

JDK 8 相对于 JDK 7 引入的主要新特性：

- Lambda 表达式
- 函数式接口（Functional Interface）
- Stream API
- 方法引用（Method Reference）
- 默认方法（Default Method）
- Optional
- 新的日期时间 API（java.time）
- Nashorn JavaScript 引擎
- Base64
- 并发增强（CompletableFuture、StampedLock、LongAdder）
- 重复注解（Repeating Annotations）
- 类型注解（Type Annotations）
- PermGen 移除，改用 Metaspace

---

## Lambda 表达式

Lambda 来自数学中的 **λ 演算**（Lambda Calculus），是函数式编程的理论基础。函数式编程的核心思想是：**函数是"一等公民"**，可以像普通值一样被传递、赋值、返回。JDK 8 引入 Lambda，本质上是给 Java 这门面向对象语言加入了函数式编程的能力。

Lambda 表达式允许将函数（即 Lambda 表达式本身）作为参数传递，简化匿名内部类的写法。

### 语法结构

```
(参数列表) -> 方法体
```

- `(参数列表)`：传入的参数，无参数时写空括号 `()`
- `->`：箭头操作符，读作 "goes to"，分隔参数列表和方法体
- `方法体`：要执行的逻辑

`Runnable` 是一个接口（`java.lang.Runnable`），只有一个无参方法 `void run()`，因此参数列表为空 `()`。

```java
// JDK 7：匿名内部类写法
Runnable r = new Runnable() {
    @Override
    public void run() {
        System.out.println("Hello");
    }
};

// JDK 8：Lambda 写法，箭头右边等价于 run() 的方法体
Runnable r = () -> System.out.println("Hello");
```

### 将函数作为参数传递

JDK 8 之前，Java 无法直接传递"一段逻辑"，只能把逻辑包装成匿名对象再传递。Lambda 表达式让你可以直接把逻辑作为参数传入方法，这就是"将函数作为参数传递"的含义。

以 `Thread` 为例，它的构造方法接受一个 `Runnable` 参数：

```java
// JDK 7：先创建匿名类对象，再传入
Runnable r = new Runnable() {
    @Override
    public void run() {
        System.out.println("Hello");
    }
};
new Thread(r).start();

// JDK 8：直接把 Lambda 表达式作为参数传入
new Thread(() -> System.out.println("Hello")).start();
```

### 单行与多行

方法体只有一行时可省略花括号；多行时需要用 `{}` 包裹：

```java
// 单行：省略花括号
Runnable r = () -> System.out.println("Hello");

// 多行：使用花括号
Runnable r = () -> {
    System.out.println("Hello");
    System.out.println("World");
};
```

### 返回值

单行时返回值隐式返回，不需要写 `return`；多行时必须显式写 `return`：

```java
// 单行：隐式返回
Function<Integer, Integer> f = x -> x * 2;

// 多行：必须显式 return
Function<Integer, Integer> f = x -> {
    int result = x * 2;
    return result;
};
```

## 函数式接口（Functional Interface）

只有一个抽象方法的接口称为函数式接口，可用 `@FunctionalInterface` 注解标记。

```java
@FunctionalInterface
public interface MyFunction {
    int apply(int x, int y);
}
```

## Stream API

Stream API 提供对集合进行函数式风格操作（过滤、映射、归约等）的能力。

```java
List<String> names = Arrays.asList("Alice", "Bob", "Charlie");

// 过滤 + 映射 + 收集
List<String> result = names.stream()
    .filter(name -> name.startsWith("A"))
    .map(String::toUpperCase)
    .collect(Collectors.toList());
```

## 方法引用（Method Reference）

方法引用是 Lambda 的简写形式，直接引用已有方法。

```java
// 静态方法引用
Function<String, Integer> parseInt = Integer::parseInt;

// 实例方法引用
Consumer<String> printer = System.out::println;

// 构造方法引用
Supplier<List<String>> listFactory = ArrayList::new;
```

## 默认方法（Default Method）

接口可以定义带有默认实现的方法，不破坏已有实现类。

```java
public interface Greeting {
    default String greet(String name) {
        return "Hello, " + name;
    }
}
```

## Optional

`Optional<T>` 用于包装可能为 null 的值，减少 NullPointerException。

```java
Optional<String> opt = Optional.ofNullable(getValue());
String result = opt.orElse("default");
```

## 新的日期时间 API（java.time）

取代旧的 `java.util.Date` 和 `Calendar`，提供不可变、线程安全的日期时间类。

```java
LocalDate date = LocalDate.now();
LocalTime time = LocalTime.of(10, 30);
LocalDateTime dateTime = LocalDateTime.now();
ZonedDateTime zoned = ZonedDateTime.now(ZoneId.of("Asia/Shanghai"));

// 格式化
String formatted = dateTime.format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));
```

## Nashorn JavaScript 引擎

内置 Nashorn 引擎，可在 JVM 上运行 JavaScript 代码（JDK 11 已废弃）。

```java
ScriptEngine engine = new ScriptEngineManager().getEngineByName("nashorn");
engine.eval("print('Hello from JavaScript')");
```

## Base64

标准库新增 `java.util.Base64`，提供 Base64 编解码支持。

```java
String encoded = Base64.getEncoder().encodeToString("hello".getBytes());
byte[] decoded = Base64.getDecoder().decode(encoded);
```

## 并发增强

- `CompletableFuture`：支持异步编程和链式组合
- `StampedLock`：读写锁的改进版，支持乐观读
- `LongAdder` / `LongAccumulator`：高并发计数器

```java
CompletableFuture<String> future = CompletableFuture
    .supplyAsync(() -> "Hello")
    .thenApply(s -> s + " World")
    .thenApply(String::toUpperCase);

System.out.println(future.get()); // HELLO WORLD
```

## 重复注解（Repeating Annotations）

同一位置可以多次使用同一个注解。

```java
@Retention(RetentionPolicy.RUNTIME)
@Repeatable(Schedules.class)
public @interface Schedule {
    String day();
}

@Schedule(day = "Mon")
@Schedule(day = "Wed")
public void meeting() {}
```

## 类型注解（Type Annotations）

注解可以应用到类型使用处，支持更强的静态分析。

```java
@NonNull String name = "Alice";
List<@NonNull String> items = new ArrayList<>();
```

## PermGen 移除

移除永久代（PermGen），改用本地内存中的元空间（Metaspace），解决 `OutOfMemoryError: PermGen space` 问题。
