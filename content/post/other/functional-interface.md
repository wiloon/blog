---
title: Java 8 函数式接口 functional interface
author: "-"
date: 2014-12-24T02:39:51+00:00
lastmod: 2026-06-20T17:33:09+08:00
url: functional-interface
categories:
  - language
tags:
  - java
  - functional-interface
  - remix
  - AI-assisted
aliases:
  - /p7127/
---

> 原文参考：[Secrets of Java 8 Functional Interface](http://colobu.com/2014/10/28/secrets-of-java-8-functional-interface/)（colobu，2014）

## 概述

**函数式接口不是一种新类型**，而是 Java 8 对一类**早已存在的接口**给出的正式定义与命名：接口中恰好有一个抽象方法（**SAM，Single Abstract Method**），因此可以作为 Lambda 表达式或方法引用的**目标类型**。判定细节见下一节 [SAM 定义](#sam)。

可以这样理解二者关系：

| 概念 | 角色 |
| ---- | ---- |
| **Lambda / 方法引用** | Java 8 **新语法**，表达「一段可传递的逻辑」 |
| **函数式接口** | **类型契约**——Lambda 不能单独存在，必须赋给通过 SAM 判定的接口 |

Java 8 **没有**新增独立的函数类型（arrow type），而是继续用 `interface` 承载函数语义。JDK 8 之前已有不少接口在结构上符合 SAM（如 `Runnable`、`Comparator`），只是当时没有「函数式接口」这一术语，也不能写 Lambda 赋给它们；Java 8 把 SAM 规则写进语言规范，并新增 `java.util.function` 包中的标准函数式接口。

函数式接口代表一种契约：在需要它的上下文中，实际期望的是符合该契约的函数。Lambda 不能脱离上下文存在，必须有一个明确的目标类型，而这个目标类型必须是通过 SAM 判定的函数式接口。

## SAM（Single Abstract Method） {#sam}

**SAM** 即 Single Abstract Method：接口中**恰好有一个**抽象方法（合并父接口继承来的抽象方法，并按规则排除 `Object` 的 public 方法）。

### SAM 是函数式接口的判定标准

「函数式接口」是 Javadoc 和语言特性里的叫法；**SAM** 是判定它是否成立的**结构规则**。二者在 Java 8 里指同一类接口，只是视角不同：

| 说法 | 视角 |
| ---- | ---- |
| **SAM** | 结构：数抽象方法——是否「只有一个待实现的抽象方法」 |
| **函数式接口** | 用途：通过 SAM 判定的接口，可作 Lambda / 方法引用的**目标类型** |

说 **「SAM 是函数式接口的判定标准」**，意思是：

编译器**不是**看接口有没有 `@FunctionalInterface` 注解、名字里有没有 Functional，而是先按 SAM 规则数抽象方法。**数出来恰好一个** → 该接口是函数式接口 → 才允许 `() -> ...` 或 `Type::method` 赋给它；**零个或多个** → 不是函数式接口 → Lambda 不能作为该类型的值。

`@FunctionalInterface` 是 API 作者可选的**文档 + 编译期约束**（防止后来误加第二个抽象方法），**不参与**「是不是函数式接口」的判定本身。

编译器判定流程（简化）：

1. 收集本接口及父接口中的全部抽象方法
2. 去掉与 `Object` public 实例方法签名相同的方法（见 [Object 的 public 方法](#object-的-public-方法)）
3. 若剩余**恰好一个** → SAM 成立 → 函数式接口 → 可作 Lambda 目标
4. 若剩余零个或多个 → 不是函数式接口

```java
@FunctionalInterface
interface Runnable {
    void run(); // the one SAM
}

// default / static methods do not add a second SAM
@FunctionalInterface
interface WithDefault {
    void apply();
    default void log() { System.out.println("ok"); }
}
```

### 什么算「那一个」抽象方法

- 本接口或父接口声明的普通抽象方法，如 `void run()`、`int apply(T t)`
- 接口继承合并后，若多个父接口的抽象方法在签名与返回类型上可合并为一个，仍算一个 SAM（复杂情形见 [泛型及继承关系](#泛型及继承关系)）

### 什么不算第二个 SAM

- `default` 方法（已有方法体，不是 abstract）
- `static` 方法
- 与 `Object` public 实例方法签名相同的声明（如 `equals`、`hashCode`）

后续章节按 SAM 规则的边界情况展开：`Object` 方法、异常、静态/默认方法、泛型继承、接口交集，以及 [`@FunctionalInterface`](#functionalinterface) 注解的用途。

## JDK 8 之前已有的函数式接口

- `java.lang.Runnable`
- `java.util.concurrent.Callable`
- `java.security.PrivilegedAction`
- `java.util.Comparator`
- `java.io.FileFilter`
- `java.nio.file.PathMatcher`
- `java.lang.reflect.InvocationHandler`
- `java.beans.PropertyChangeListener`
- `java.awt.event.ActionListener`
- `javax.swing.event.ChangeListener`

## java.util.function 包

`java.util.function` 中定义了几组函数式接口，以及针对基本数据类型的子接口：

| 接口 | 说明 | 抽象方法 |
| ---- | ---- | -------- |
| `Predicate` | 传入一个参数，返回布尔结果 | `boolean test(T t)` |
| `Consumer` | 传入一个参数，无返回值 | `void accept(T t)` |
| `Function` | 传入一个参数，返回一个结果 | `R apply(T t)` |
| `Supplier` | 无参数，返回一个结果 | `T get()` |
| `UnaryOperator` | 一元操作，参数与返回类型相同 | 继承 `Function` |
| `BinaryOperator` | 二元操作，两参数与返回类型相同 | 继承 `BiFunction` |

Java API 文档会对函数式接口标注 `Functional Interface`，并说明其可作为 Lambda 或方法引用的赋值目标。例如 `Runnable` 的 Javadoc 会写明：

```text
Functional Interface:
This is a functional interface and can therefore be used as the assignment
target for a lambda expression or method reference.
```

## Object 的 public 方法

函数式接口可以额外声明与 `Object` public 方法签名相同的抽象方法；接口实例最终由类实现，而类的根类型是 `Object`，因此这些声明不会增加第二个 SAM。

```java
@FunctionalInterface
public interface ObjectMethodFunctionalInterface {
    void count(int i);

    String toString(); // same as Object.toString()
    int hashCode();    // same as Object.hashCode()
    boolean equals(Object obj); // same as Object.equals()
}
```

为什么只限定 public 方法？因为接口中的方法默认就是 public。若签名对应 `Object` 的 protected 方法，则不算 SAM 的「额外抽象方法」豁免，接口也不再是函数式接口：

```java
interface WrongObjectMethodFunctionalInterface {
    void count(int i);

    Object clone(); // Object.clone() is protected
}
```

## 声明异常

函数式接口的抽象方法可以声明 checked exception；调用方必须按常规接口规则处理。

```java
@FunctionalInterface
interface InterfaceWithException {
    void apply(int i) throws Exception;
}

public class FunctionalInterfaceWithException {
    public static void main(String[] args) {
        InterfaceWithException target = i -> {};
        try {
            target.apply(10);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

若 Lambda 体抛出 checked exception，而目标接口的抽象方法未声明该异常，则编译失败——Lambda 的目标类型与接口声明不匹配：

```java
@FunctionalInterface
interface InterfaceWithException {
    void apply(int i);
}

public class FunctionalInterfaceWithException {
    public static void main(String[] args) {
        // 编译错误：Lambda 抛出的 Exception 未在接口中声明
        InterfaceWithException target = i -> { throw new Exception(); };
    }
}
```

## 静态方法

Java 8 之前，接口不能定义静态方法；Java 8 起可以。一个或多个静态方法不影响接口仍是函数式接口。

```java
@FunctionalInterface
interface FunctionalInterfaceWithStaticMethod {
    static int sum(int[] array) {
        return Arrays.stream(array).reduce((a, b) -> a + b).getAsInt();
    }

    void apply();
}

public class StaticMethodFunctionalInterface {
    public static void main(String[] args) {
        int sum = FunctionalInterfaceWithStaticMethod.sum(new int[]{1, 2, 3, 4, 5});
        FunctionalInterfaceWithStaticMethod f = () -> {};
    }
}
```

## 默认方法

Java 8 允许在接口中用 `default` 提供具体实现。默认方法不是抽象方法，不影响 SAM 判定。

```java
@FunctionalInterface
interface InterfaceWithDefaultMethod {
    void apply(Object obj);

    default void say(String name) {
        System.out.println("hello " + name);
    }
}

class FunctionalInterfaceWithDefaultMethod {
    public static void main(String[] args) {
        InterfaceWithDefaultMethod i = (o) -> {};
        i.apply(null);
        i.say("default method");
    }
}
```

`InterfaceWithDefaultMethod` 仍然是函数式接口。

## 泛型及继承关系

接口可以继承接口。若父接口是函数式接口，子接口是否仍为函数式接口，取决于合并后的抽象方法集合。

对接口 `I`，设 `M` 为 `I` 及其父接口中所有抽象方法的集合，并排除与 `Object` public 实例方法签名相同的方法。若存在方法 `m` 满足：

1. `m` 的签名是 `M` 中每个方法签名的 subsignature
2. `m` 的返回类型与 `M` 中每个方法的返回类型 return-type-substitutable

则 `I` 是函数式接口。

### 示例

**1）相同签名，是函数式接口**

```java
interface X { int m(Iterable<String> arg); }
interface Y { int m(Iterable<String> arg); }
interface Z extends X, Y {}
// Z 的唯一抽象方法：int m(Iterable<String> arg)
```

**2）泛型擦除后签名兼容，是函数式接口**

```java
interface X { Iterable m(Iterable<String> arg); }
interface Y { Iterable<String> m(Iterable arg); }
interface Z extends X, Y {}
// 函数类型：Iterable<String> m(Iterable arg)
```

**3）参数类型不兼容，编译错误**

```java
interface X { int m(Iterable<String> arg); }
interface Y { int m(Iterable<Integer> arg); }
interface Z extends X, Y {}
// 编译错误：没有一个方法的签名是所有方法的 subsignature
```

**4）参数列表不兼容，编译错误**

```java
interface X { int m(Iterable<String> arg, Class c); }
interface Y { int m(Iterable arg, Class<?> c); }
interface Z extends X, Y {}
// Compiler error: No method has a subsignature of all abstract methods
```

**5）返回类型不兼容，编译错误**

```java
interface X { long m(); }
interface Y { int m(); }
interface Z extends X, Y {}
// Compiler error: no method is return type substitutable
```

**6）擦除后相同但签名不同，编译错误**

```java
interface Foo<T> { void m(T arg); }
interface Bar<T> { void m(T arg); }
interface FooBar<X, Y> extends Foo<X>, Bar<Y> {}
// Compiler error: different signatures, same erasure
```

**7）类型参数不同，不是函数式接口**

```java
interface Foo { void m(String arg); }
interface Bar<T> { void m(T arg); }
interface FooBar<T> extends Foo, Bar<T> {}
```

**8）异常列表不同，仍可能是函数式接口，但函数类型不同**

```java
interface X { void m() throws IOException; }
interface Y { void m() throws EOFException; }
interface Z { void m() throws ClassNotFoundException; }
interface XY extends X, Y {}
interface XYZ extends X, Y, Z {}
// XY  的函数类型：() -> void throws EOFException
// XYZ 的函数类型：() -> void（throws nothing）
```

**9）复杂泛型与异常合并**

```java
interface A {
    List<String> foo(List<String> arg) throws IOException, SQLTransientException;
}
interface B {
    List foo(List<String> arg) throws EOFException, SQLException, TimeoutException;
}
interface C {
    List foo(List arg) throws Exception;
}
interface D extends A, B {}
interface E extends A, B, C {}
// D 的函数类型：(List) -> List throws EOFException, SQLTransientException
// E 的函数类型：(List) -> List throws EOFException, SQLTransientException
```

**10）泛型异常边界**

```java
interface G1 {
    <E extends Exception> Object m() throws E;
}
interface G2 {
    <F extends Exception> String m() throws Exception;
}
interface G extends G1, G2 {}
// G 的函数类型：() -> String throws F
```

## 函数式接口的交集

### 两个接口方法相同

```java
public class Z {
    public static void main(String[] args) {
        Object o = (I & J) () -> {};
    }
}

interface I {
    void foo();
}

interface J {
    void foo();
}
```

`I` 和 `J` 的方法交集仍符合函数式接口定义。上述代码可用 `javac` 编译通过；旧版 Eclipse 可能误报，属于 IDE 问题。

### 两个接口方法不一致

```java
public class Z {
    public static void main(String[] args) {
        Object o = (I & J) () -> {};
    }
}

interface I {
    void foo();
}

interface J {
    void foo();
    void bar();
}
```

此例中 Eclipse 可能不报错，但 `javac` 无法编译——`(I & J)` 不是函数式接口。

## @FunctionalInterface {#functionalinterface} 注解

`@FunctionalInterface` 随 **Java 8（JDK 8）** 引入，位于 `java.lang.FunctionalInterface`。它与 Lambda、SAM 判定规则同属 Java 8 函数式编程特性的一部分；**JDK 8 之前不存在此注解**。

Java 不强制用 `@FunctionalInterface` 标记函数式接口；作为 API 作者，加上该注解可以明确设计意图，也方便读者识别。再次强调：有没有该注解**不影响**接口是否通过 SAM 判定为函数式接口——判定只看抽象方法个数与合并规则（见 [SAM 定义](#sam)）。

```java
@FunctionalInterface
public interface SimpleFuncInterface {
    void doWork();
}
```

若接口不符合 SAM 规则仍加上该注解，编译器会报错：

```text
error: Unexpected @FunctionalInterface annotation
@FunctionalInterface
^
  I is not a functional interface
    multiple non-overriding abstract methods found in interface I
```

注解还会在后续维护中阻止误加第二个抽象方法，起到编译期约束作用。

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-06-20 | 重组章节结构；代码块添加语法高亮；分类改为 language；更新过时表述 | 提升可读性与 Markdown 规范 |
| 2026-06-20 | 新增 §SAM  canonical 定义；说明 SAM 与函数式接口的判定关系 | 统一术语出处，供 lambda/jdk-8 互链 |
| 2026-06-20 | 概述补充「非新类型、Lambda 与函数式接口分工」；`@FunctionalInterface` 注明 JDK 8 引入 | 澄清概念理解 |
