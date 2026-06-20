---
title: Java 内部类
author: "-"
date: 2014-04-04T01:00:31+08:00
lastmod: 2026-06-20T15:18:24+08:00
url: inner-class
categories:
  - language
tags:
  - java
  - remix
  - AI-assisted
---

JDK 1.1 起支持在类或方法内部定义嵌套类。本文整理成员内部类、静态嵌套类、局部内部类与匿名内部类的用法与设计动机；版本背景见 [JDK 1.1](./jdk-1.1.md)。

## 概览

### 静态与非静态

Java 把「定义在外部类内部的类」统称**嵌套类**（nested class）。按是否带 `static`，分为两大类：

| | 静态嵌套类 | 非静态内部类 |
| ---- | ---------- | ------------ |
| 关键字 | `static class` | 无 `static`（成员 / 局部 / 匿名） |
| 与外部类实例 | 不绑定，可 `new Outer.Inner()` | 绑定，需 `outer.new Inner()` |
| 访问 outer 的 private | 仅 **static** 成员 | **实例**成员（含 private） |
| 典型用途 | Builder、Holder 单例、`Map.Entry` | 迭代器 helper、回调、访问 outer 私有状态 |

非静态内部类又常按定义位置细分为：**成员内部类**、**局部内部类**、**匿名内部类**。下文分别举例。

### 解决什么问题

- **封装与分组**：把只服务于外部类的 helper 类型收进 `Outer.Inner`，缩小可见范围；外部 API 只暴露外层类或接口。
- **表达逻辑关联**：其它代码也可以使用内部类（如 `Map.Entry`、`Person.Home`），嵌套表示「该类型从属于外部类的概念域」，而不一定是「只用一次」。
- **访问私有成员**：非静态内部类可直接读写 outer 的 `private` 字段和方法，不必为此暴露 getter；这是相对顶层 helper 类的关键优势。
- **局部 / 匿名**：封装**只在一处使用、且与当前方法或外部类强相关**的逻辑；JDK 8 起，[SAM](../../other/functional-interface.md#sam) 回调场景优先用 [Lambda](../lambda.md)（见下文「与现代 Java」）。
- **单继承下的行为组合**：内部类可独立 extends / implements，与外部类已有继承关系互不干扰（现代代码中相对少见，更多用组合或接口 default 方法）。

## 成员内部类

```java
public class OuterClass {
    private String name;
    private int age;
    class InnerClass {
        public InnerClass() {
            name = "mark";
            age = 20;
        }
        public void echo() {
            System.out.println(name + " " + age);
        }
    }
}
```

### 问题思考

上面这个很简单的例子中，也包含了很多应该思考的问题：

- 内部类如何被实例化？
- 内部类能否改变外围类的属性，两者之间又是什么一种关系？
- 内部类存在的意义是什么？

在回答这三个问题之前，必须要明确一个点，那就是内部类是依附于外围类而存在的，其实也就是内部类存在着指向外围类的引用。明白了这个之后，上面的问题就好解答了。

### 实例化与数据访问

内部类与外围类之间形成了一种联系，使得内部类可以无限制地访问外围类中的任意属性。正如上面的例子中，`InnerClass` 内部可以随意访问 `OuterClass` 中的 `private` 属性。

同样的，因为内部类依赖于外围类的存在，所以无法在外部直接将其实例化，而是必须先实例化外围类，才能够实例化内部类（注意，在外围类的成员方法里仍然是可以直接实例化内部类的）：

```java
public static void main(String[] args) {
    InnerClass inner = new OuterClass().new InnerClass();
    inner.echo();
}
```

使用外围类的 `.new` 来创建内部类。内部类和外围类的联系是通过内部类所持有的外部类的引用来实现的；想要获取这个引用，可以使用 `OuterClass.this`：

```java
public class OuterClass {
    private String name;
    private int age;
    class InnerClass {
        public InnerClass() {
            name = "mark";
            age = 20;
        }
        public void echo() {
            System.out.println(name + " " + age);
        }
        public OuterClass getOuter() {
            return OuterClass.this;
        }
    }

    @Test
    public void test() {
        OuterClass outer = new OuterClass();
        InnerClass inner = outer.new InnerClass();
        Assert.assertEquals(outer, inner.getOuter());
    }
}
```

### 内部类的作用

内部类创建起来很麻烦，使用起来也令人困扰，那么内部类存在的意义是什么呢？

#### 实现多重继承

这可能是内部类存在的最重要的意义，参考《Thinking in Java》中的解释：

> 使用内部类最吸引人的原因是：每个内部类都能独立地继承一个（接口的）实现，所以无论外围类是否已经继承了某个（接口的）实现，对于内部类都没有影响。

Java 取消了 C++ 中类的多重继承（但允许接口的多重实现）。若同一个类需要同时继承两个类，可以用内部类来组织。比如有两个抽象类：

```java
public abstract class AbstractFather {
    protected int number;
    protected String fatherName;
    public abstract String sayHello();
}

public abstract class AbstractMother {
    protected int number;
    protected String motherName;
    public abstract String sayHello();
}
```

若外围类同时继承这两个类，势必引起 `number` 与 `sayHello` 的冲突。使用内部类可以让两个不同的类分别继承不同的基类：

```java
public class TestClass extends AbstractFather {
    @Override
    public String sayHello() {
        return fatherName;
    }

    class TestInnerClass extends AbstractMother {
        @Override
        public String sayHello() {
            return motherName;
        }
    }
}
```

#### 其他

（摘自《Thinking in Java》）

- 内部类可以用多个实例，每个实例都有自己的状态信息，并且与其他外围对象的信息相互独立。
- 在单个外围类中，可以让多个内部类以不同的方式实现同一个接口，或者继承同一个类。
- 创建内部类对象的时刻并不依赖于外围类对象的创建。
- 内部类并没有令人迷惑的「is-a」关系，它就是一个独立的实体。
- 内部类提供了更好的封装，除了该外围类，其他类都不能访问。

### 内部类的分类

上面的例子中创建的内部类都属于成员内部类。Java 中还有局部内部类、静态嵌套类与匿名内部类。

#### 局部内部类

嵌套在方法里或某个作用域内，通常不希望这个类对外公开。相比于成员内部类，局部内部类的作用域更窄，出了方法或作用域就无法被访问，一般用于实现私有的辅助功能。

定义在方法里：

```java
public class Parcel5 {
    public Destination destination(String str) {
        class PDestination implements Destination {
            private String label;
            private PDestination(String whereTo) {
                label = whereTo;
            }
            public String readLabel() {
                return label;
            }
        }
        return new PDestination(str);
    }

    public static void main(String[] args) {
        Parcel5 parcel5 = new Parcel5();
        Destination d = parcel5.destination("chenssy");
    }
}
```

定义在作用域内：

```java
public class Parcel6 {
    private void internalTracking(boolean b) {
        if (b) {
            class TrackingSlip {
                private String id;
                TrackingSlip(String s) {
                    id = s;
                }
                String getSlip() {
                    return id;
                }
            }
            TrackingSlip ts = new TrackingSlip("chenssy");
            String string = ts.getSlip();
        }
    }

    public void track() {
        internalTracking(true);
    }

    public static void main(String[] args) {
        Parcel6 parcel6 = new Parcel6();
        parcel6.track();
    }
}
```

不能在 `if` 之外创建 `TrackingSlip` 对象，因为已超出其作用域；编译时仍会生成对应 class 文件，只是运行时访问受作用域限制。

#### 静态嵌套类

使用 `static` 修饰的内部类即为静态嵌套类（static nested class）。与普通成员内部类最大的不同是，静态嵌套类没有指向外围类的引用，创建不依赖外围类实例，也不能使用外围类的非 `static` 成员。

静态嵌套类常用于线程安全的单例：

```java
public class Singleton {
    private static class SingletonHolder {
        private static final Singleton INSTANCE = new Singleton();
    }
    private Singleton() {}
    public static final Singleton getInstance() {
        return SingletonHolder.INSTANCE;
    }
}
```

这是利用了 JVM 的特性：静态嵌套类在类加载时初始化，因此不受多线程竞态影响。

#### 匿名内部类

匿名内部类是没有名字的内部类，语法为 `new InterfaceName() { ... }` 或 `new SuperClassName() { ... }`。

快速创建 `Thread` 时常见：

```java
new Thread(new Runnable() {
    @Override
    public void run() {
        System.out.println("hello");
    }
}).start();
```

实现接口并返回：

```java
public class Goods3 {
    public Contents cont() {
        return new Contents() {
            private int i = 11;
            public int value() {
                return i;
            }
        };
    }
}
```

AWT/Swing 时代的事件适配器也大量使用匿名内部类：

```java
frame.addWindowListener(new WindowAdapter() {
    public void windowClosing(WindowEvent e) {
        System.exit(0);
    }
});
```

现在 SAM 场景可用 [Lambda 表达式](../lambda.md) 替代（如 `() -> System.out.println("hello")`）。二者关系与编译差异见 [Lambda 与内部类](../lambda.md#lambda-与内部类)。

使用匿名内部类时要注意：

- 没有访问修饰符，也没有具名构造方法（继承带参父类时需在 `{ ... }` 内用 `super(...)` 调用）
- 通常 implements 一个接口或 extends 一个类；**不能**同时 implements 多个接口（Lambda 同样只能对应一个函数式接口）
- 若访问局部变量，该变量必须是 `final` 或 effectively final
- 匿名类有自己的 `this`；在实例方法里若需区分外部类，用 `OuterClass.this`

初始化成员变量的常见做法：经方法参数传入（须 effectively final）、改为局部内部类以使用构造器、或在匿名类中使用实例初始化块。

匿名内部类与函数闭包有相似之处（也是 Lambda 能替代它的原因之一），但两者并不相同；对比见 [闭包](../../cs/closure.md)。

> 参考：[不洗碗工作室 · 稀土掘金](https://juejin.cn/post/6844903655510917128)

---

## 静态嵌套类与封装

Java 中的嵌套类（Nested Class）分为静态嵌套类（Static Nested Class）和内部类（Inner Class）。只有在静态嵌套类的情况下才能把 `static` 修饰符放在类前，其他任何时候 `static` 都不能修饰类。

静态嵌套类有两个常见优点：加强封装、提高可读性。

```java
public class Person {
    private String name;
    private Home home;
    public Person(String _name) {
        name = _name;
    }
    public static class Home {
        private String address;
        private String tel;
        public Home(String _address, String _tel) {
            address = _address;
            tel = _tel;
        }
    }
}
```

`Home` 封装家庭信息，不必在 `Person` 中再定义 `homeAddress`、`homeTel` 等字段。使用时语义清晰：

```java
public static void main(String[] args) {
    Person p = new Person("张三");
    p.setHome(new Person.Home("上海", "021"));
}
```

- 提高封装性：静态嵌套类放在外部类内，表示它是外部类的子行为或子属性。
- 提高可读性：相关联的代码放在一起，关联关系一目了然。

静态嵌套类虽然编译后的类文件名包含外部类（格式 `外部类$内部类`），但可以脱离外部类实例存在，仍可通过 `new Person.Home(...)` 创建——此时嵌套主要表达 **Outer 与 Inner 的逻辑从属关系**，Inner 仍可在多处被外部代码使用。

静态嵌套类与普通内部类的区别：

1. 静态嵌套类不持有外部类的引用；普通内部类可直接访问外部类实例成员（含 `private`）。
2. 静态嵌套类可独立存在；普通内部类实例与外部类实例同生共死。
3. 普通内部类不能声明 `static` 的方法和变量（`final static` 常量除外）；静态嵌套类无此限制。

## 接口与访问控制示例

```java
public interface Contents {
    int value();
}

public interface Destination {
    String readLabel();
}

public class Goods {
    private class Content implements Contents {
        private int i = 11;
        public int value() {
            return i;
        }
    }

    protected class GDestination implements Destination {
        private String label;
        private GDestination(String whereTo) {
            label = whereTo;
        }
        public String readLabel() {
            return label;
        }
    }

    public Destination dest(String s) {
        return new GDestination(s);
    }

    public Contents cont() {
        return new Content();
    }
}

class TestGoods {
    public static void main(String[] args) {
        Goods p = new Goods();
        Contents c = p.cont();
        Destination d = p.dest("Beijing");
    }
}
```

`Content` 与 `GDestination` 定义在 `Goods` 内部，分别用 `protected` 和 `private` 控制访问级别。外部通过 `cont()`、`dest()` 获取内部类对象，不必暴露内部类名——这是封装性的体现。

在外部类作用域之外创建非静态内部类对象，语法为：

```text
outerObject = new OuterClass(constructorParameters);
OuterClass.InnerClass innerObject = outerObject.new InnerClass(constructorParameters);
```

非静态内部类对象持有指向外部类对象的引用。若内部类成员与外部类同名，外部类引用写作 `OuterClass.this`：

```java
public class Goods {
    private int valueRate = 2;

    private class Content implements Contents {
        private int i = 11 * valueRate;
        public int value() {
            return i;
        }
    }
    // ...
}
```

## 与现代 Java

内部类仍是语言的一等特性，但日常用法的重心有变化：

| 类型 | 现代地位 |
| ---- | -------- |
| 匿名内部类 | SAM 回调大量被 **Lambda / 方法引用** 取代 |
| 静态嵌套类 | **仍常见**：Builder、Holder 单例、JDK 中的 `Map.Entry` 等 |
| 成员内部类 | **仍有价值**：需稳定持有 outer 引用、实现迭代器或框架内部 helper |
| 局部内部类 | **相对少见**，多数场景用 Lambda 或 private 方法即可 |

Lambda **不能**完全替代内部类：需 extends 类、implements 多个接口、多个方法、显式匿名类 `this` 或实例字段时，仍用内部类。简记：**Lambda = 单抽象方法回调的简写；内部类 = 在类型层面做封装与分组**，二者有交集。

## 为什么需要内部类

若外部类已实现某接口，但接口中某方法与外部类已有方法同名同参，可让内部类实现该接口，利用内部类对外部类成员的访问能力完成逻辑。

更根本的原因：内部类与接口配合，可以在 Java 中实现类似 C++ 多重继承的效果，而避免 C++ 多继承的复杂度。

> 延伸阅读：[51CTO](http://book.51cto.com/art/201202/317517.htm)、[CSDN](http://blog.csdn.net/ilibaba/article/details/3866537)

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-06-20 | 文件重命名为 `inner-class.md`；修正 front matter、标题层级与代码块；补充 JDK 1.1 与闭包内链 | 中文文件名不符合规范；正文格式混乱 |
| 2026-06-20 | 匿名内部类小节增加指向 lambda 文档的内链 | 与 Lambda 文档互链 |
| 2026-06-20 | 新增概览（静态/非静态、设计动机）、与现代 Java、合并匿名/局部内部类重复小节 | 补全对话中讨论要点 |
| 2026-06-20 | SAM 术语链到 functional-interface §SAM | 统一术语出处 |
