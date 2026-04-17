---
title: 外观模式, Facade Pattern
author: "-"
date: 2026-04-16T17:05:05+08:00
url: facade-pattern
categories:
  - Pattern
tags:
  - remix
  - AI-assisted
---

## 概念

看到"门面"这个词，大家一定都觉得很熟悉。日常生活中的"门面"就是我们买东西的地方，它跟各种商品的生产商打交道，收集商品后再卖给我们。如果没有"门面"，我们将不得不直接跟各种各样的生产商买商品。

Facade 模式正是这样一个"门面"：我们本来需要与后台的多个类或接口打交道，而 Facade 模式在客户端和后台之间插入一个中间层——门面，这个门面跟后台的多个类或接口打交道，客户端只需要跟门面打交道即可。

Facade 类是一个简化的用户接口，它和后台中的多个类产生依赖关系，而客户类则只跟 Facade 类产生依赖关系。后台的开发者熟悉自己开发的各个类，容易解决与多个类的依赖关系；而使用者不太熟悉后台的各个类，通过 Facade 可以大大降低使用难度。

## 情况一：功能分布在多个无关类中

客户类要使用的功能分布在多个类中，客户必须先初始化各个类才能使用。这时适合将这些功能集中在一个 Facade 类里，同时替用户做初始化工作。

**场景：** 商店里出售三种商品——衣服、电脑和手机，分别由各自的生产厂商提供。

各厂商类：

```java
public class CoatFactory {
    public Coat saleCoat() {
        // ...
        return coat;
    }
}

public class ComputerFactory {
    public Computer saleComputer() {
        // ...
        return computer;
    }
}

public class MobileFactory {
    public Mobile saleMobile() {
        // ...
        return mobile;
    }
}
```

没有商店时，客户需要分别跟各厂商打交道：

```java
// 买衣服
CoatFactory coatFactory = new CoatFactory();
coatFactory.saleCoat();

// 买电脑
ComputerFactory computerFactory = new ComputerFactory();
computerFactory.saleComputer();

// 买手机
MobileFactory mobileFactory = new MobileFactory();
mobileFactory.saleMobile();
```

对客户来说，和这么多厂家类打交道显然很麻烦。

引入 Facade（商店类），让商店和厂家打交道，客户只和商店打交道：

```java
public class Store {
    public Coat saleCoat() {
        CoatFactory coatFactory = new CoatFactory();
        return coatFactory.saleCoat();
    }

    public Computer saleComputer() {
        ComputerFactory computerFactory = new ComputerFactory();
        return computerFactory.saleComputer();
    }

    public Mobile saleMobile() {
        MobileFactory mobileFactory = new MobileFactory();
        return mobileFactory.saleMobile();
    }
}
```

客户端调用：

```java
Store store = new Store();

store.saleCoat();
store.saleComputer();
store.saleMobile();
```

## 情况二：完成某个功能需要调用后台多个类

客户要完成某个功能，需要调用后台多个类才能实现，这时尤其应该使用 Facade 模式。

**反例：** 后台开发人员强迫使用者自己写这样的代码：

```java
String xmlString = null;
try {
    xmlString = gdSizeChart.buildDataXML(incBean);

    String path = "D:/workspace/gridfile.xml";
    File f = new File(path);
    PrintWriter out = new PrintWriter(new FileWriter(f));
    out.print(xmlString);
    out.close();

    request.setAttribute("xmlString", xmlString);
} catch (Exception ex) {
    ex.printStackTrace();
}
```

使用者不了解后台思路，不知道来龙去脉，这样的调用方式很困难。

**改进：** 引入 Facade 类，把不该由客户类做的事封装起来：

```java
public class Facade {
    public static void doAll(PE_MeasTableExdBean incBean, HttpServletRequest request) {
        // ... 其他调用 ...
        request.setAttribute("xmlString", Facade.getFromOut(incBean));
    }

    private static String getFromOut(PE_MeasTableExdBean incBean) {
        try {
            String xmlString = gdSizeChart.buildDataXML(incBean);

            String path = "D:/workspace/gridfile.xml";
            File f = new File(path);
            PrintWriter out = new PrintWriter(new FileWriter(f));
            out.print(xmlString);
            out.close();

            return xmlString;
        } catch (Exception ex) {
            ex.printStackTrace();
            return null;
        }
    }
}
```

客户端调用：

```java
Facade.doAll(incBean, request);
```

> 注意：`getFromOut` 方法放在 Facade 类中是为了示例简洁，实际上违反了单一职责原则，应单独抽取。

## 总结模式结构

后台有多个类实现某个功能：

```java
public class ClassA {
    public void doA() { /* ... */ }
}

public class ClassB {
    public void doB() { /* ... */ }
}

public class ClassC {
    public void doC() { /* ... */ }
}
```

没有 Facade 时客户需要：

```java
ClassA a = new ClassA();
a.doA();
ClassB b = new ClassB();
b.doB();
ClassC c = new ClassC();
c.doC();
```

引入 Facade：

```java
public class Facade {
    public void doAll() {
        new ClassA().doA();
        new ClassB().doB();
        new ClassC().doC();
    }
}
```

客户端：

```java
Facade facade = new Facade();
facade.doAll();
```

## 现实中的 Facade：企业 Portal

企业内部通常有很多应用系统——OA、HR、财务、CRM 等，不同系统完成不同功能。企业一般会做一个 **Portal 页面**，用户在这里可以选择进入哪个子系统，不需要记忆各系统的 URL。

这正是 Facade 模式在产品层面的体现：

| 角色 | 对应 |
|------|------|
| Client | 用户 |
| Facade | Portal 页面 |
| Subsystems | OA、HR、财务等各子系统 |

不过 Portal 更多是 UI 层面的"门面"，代码中的 Facade 通常还会做**调用编排**——不只是提供入口列表，还会把多个子系统的调用封装成一个简单方法（如先调 A，再调 B，最后调 C）。两者概念一脉相承，Portal 是 Facade 思想在系统设计层面的自然延伸。