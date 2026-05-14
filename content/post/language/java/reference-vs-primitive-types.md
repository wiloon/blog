---
title: Java 引用类型与基本类型
author: "-"
date: 2012-09-20T03:12:25+00:00
lastmod: 2026-05-13T14:25:14+08:00
url: reference-vs-primitive-types
categories:
  - Java
tags:
  - java
  - remix
  - AI-assisted
---

在 Java 性能优化中，内存管理是一个要优先考虑的关键因素。而说到内存分配，就必然会涉及到基本类型和引用类型。

## 名词定义

所谓基本类型，就是 Java 语言中如下 8 种内置类型：`boolean`、`char`、`byte`、`short`、`int`、`long`、`float`、`double`。而引用类型就是那些可以通过 `new` 来创建对象的类型（基本上都派生自 `Object`）。

## 两种类型的存储方式

这两种类型的差异，首先体现在存储方式上。在 Java 中，引用类型的对象存储在堆（Heap）上；而基本类型的值存储在栈（Stack）上。

## 堆和栈的性能差异

堆和栈在性能方面差别很大。堆相对进程来说是全局的，能够被所有线程访问；而栈是线程局部的，只能本线程访问。

由于堆是所有线程共有的，从堆里申请内存要进行相关的加锁操作，因此申请堆内存的复杂度和时间开销比栈要大很多；从栈里申请内存，虽然又简单又快，但是栈的大小有限，分配不了太多内存。

## 为什么这样设计

James Gosling 设计 Java 时，把各种东西都放置到栈中显然不现实：一来栈是线程私有的（不便于共享），二来栈的大小是有限的，三来栈的结构也间接限制了它的用途。而都放堆里面，申请堆内存需要加锁，开销太大。如果仅仅在函数中写一个简单的 `int n = 0`，也要到堆里面去分配内存，性能就会很差。

最终的折中方案：把类型分为基本类型和引用类型；引用类型（Object 派生）的对象存放到堆里面；把基本类型（非 Object 派生）的值存放到栈里面。从 Java 语法上也可以看出两者的差别：引用类型可以用 `new` 创建对象；而基本类型则不需要用 `new` 来创建。

### 这样设计的弊端

这个折中决策带来了一些深远影响：

1. 由于基本类型不是派生自 `Object`，因此不能算是纯粹的对象，使 Java 的"纯面向对象"招牌打了折扣。
1. 出于某些场合（比如容器类）的考虑，不得不为每个基本类型加上对应的包装类（比如 `Integer`、`Byte` 等），使语言变得有点冗余。

### 结论

使用 `new` 创建对象的开销不小，在程序中能避免就应该尽量避免。另外，使用 `new` 创建对象，不光创建时开销大，将来垃圾回收时销毁对象也是有开销的。

参考：

- <http://program-think.blogspot.com/2009/03/java-performance-tuning-1-two-types.html>
- <http://www.ibm.com/developerworks/cn/java/praxis/pr8.html>

## 原始类型和封装类

| 原始类型 | 封装类    |
| -------- | --------- |
| boolean  | Boolean   |
| char     | Character |
| byte     | Byte      |
| short    | Short     |
| int      | Integer   |
| long     | Long      |
| float    | Float     |
| double   | Double    |

## 引用类型与基本类型的行为差异

引用类型和原始类型的行为完全不同。例如，假定一个方法中有两个局部变量，一个变量为 `int` 原始类型，另一个变量是对一个 `Integer` 对象的对象引用：

```java
int i = 5;                   // 原始类型
Integer j = new Integer(10); // 对象引用
```

原始类型 `int` 和对象引用各占堆栈的 32 位。`Integer` 对象的堆栈项并不是对象本身，而是一个对象引用。Java 中的所有对象都要通过对象引用访问，对象引用是指向对象存储所在堆中某个区域的指针。

引用类型和原始类型具有不同的特征和用法，包括大小和速度问题、存储结构差异，以及作为实例变量时的缺省值差异。对象引用实例变量的缺省值为 `null`，而原始类型实例变量的缺省值与它们的类型有关。

不能对原始类型调用方法，但可以对对象调用方法：

```java
int j = 5;
j.hashCode();  // 编译错误

Integer i = new Integer(5);
i.hashCode();  // 正确
```

混合使用原始类型和对象也可能导致与赋值有关的意外结果。例如：

```java
import java.awt.Point;

class Assign {
    public static void main(String args[]) {
        int a = 1;
        int b = 2;
        Point x = new Point(0, 0);
        Point y = new Point(1, 1);

        System.out.println("a is " + a);
        System.out.println("b is " + b);
        System.out.println("x is " + x);
        System.out.println("y is " + y);
        System.out.println("Performing assignment and setLocation...");

        a = b;
        a++;
        x = y;             // x 和 y 指向同一个对象
        x.setLocation(5, 5); // 修改了 x 也修改了 y

        System.out.println("a is " + a);
        System.out.println("b is " + b);
        System.out.println("x is " + x);
        System.out.println("y is " + y);
    }
}
```

输出结果：

```text
a is 1
b is 2
x is java.awt.Point[x=0,y=0]
y is java.awt.Point[x=1,y=1]
Performing assignment and setLocation...
a is 3
b is 2
x is java.awt.Point[x=5,y=5]
y is java.awt.Point[x=5,y=5]
```

`a = b` 后修改 `a` 不影响 `b`（值拷贝）；而 `x = y` 后修改 `x` 同时影响了 `y`（引用拷贝，两者指向同一个对象）。
