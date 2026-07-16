---
title: JDK 5
author: "-"
date: 2012-03-28T02:49:08+00:00
lastmod: 2026-06-24T09:37:13+08:00
url: jdk-5
categories:
  - language
tags:
  - java
  - jdk
  - remix
  - AI-assisted
aliases:
  - jdk5
  - jdk-5-features
  - /p642/
  - /p728/
  - /p2045/
  - /p2668/
  - /p3207/
  - /p3209/
  - /p3279/
  - /p3909/
  - /p3911/
  - /p3997/
  - /p4014/
  - /p4139/
  - /p4340/
  - /p4356/
  - /p4410/
  - /p4585/
  - /p4961/
  - /p5029/
  - /p5083/
  - /p5981/
  - /p6399/
  - /p6461/
  - /p6513/
  - /p6518/
  - /p6658/
  - /p6700/
  - /p7847/
  - /p8122/
  - /p8392/
  - /p8447/
  - /p8842/
---

JDK 5（Java SE 5）于 **2004 年 9 月**正式发布，是 [JDK 1.4](./jdk-1-4.md) 之后的一次重大更新。**第一个对外以「Java 5」而非「Java 1.5」命名的版本**；平台品牌 J2SE → Java SE 的过渡亦在此前后。详见 [Java 版本历史](./java-version-history.md)。

Tiger 语言特性（含注解）自 2002 年起在 JCP 并行规划（JSR 175 等于 JDK 1.4 发布后不久立项）；**2003 年 12 月**有 Early Access 构建，**2004 年 2 月**公开 Beta——均早于上述正式版。

## 发布历程

「2004 年 9 月」指 **GA（正式版）**；Tiger 在 JCP 与 Sun 产品线上的里程碑更早：

| 阶段 | 大约时间 | 说明 |
| ---- | -------- | ---- |
| [JDK 1.4](./jdk-1-4.md) GA | 2002-02 | 1.4 落地后，Tiger 语言特性（含 JSR 175 注解）即在 JCP 并行推进 |
| JSR 175 立项 | 2002-03～04 | JCP 评审通过，专家组成立 |
| JSR 175 公开评审 | 2003-11 | 注解规范草案公开 |
| Tiger Early Access | 2003-12 | 预发布 JDK（含注解等语言特性），面向早期测试 |
| Tiger 公开 Beta | 2004-02 | 可在 `java.sun.com/j2se/1.5` 下载试用 |
| **JDK 5 Final** | **2004-09-30** | 对外称 Java 5 / J2SE 5.0；`java.version` 仍为 `1.5.0_xxx` |

同一 Tiger 版本还打包了泛型（JSR 14）、枚举与增强 for（JSR 201）、JUC（JSR 166）等；整体由 **JSR 176**（J2SE 5.0 Release Contents）归集交付。

## 版本号说明

| 维度 | JDK 5 |
| ---- | ----- |
| 对外名称 | Java 5 / J2SE 5.0（旧） |
| `java.version` | `1.5.0_xxx` |
| class major version | 49 |

完整命名演变见 [Java 版本历史](./java-version-history.md)。

## 概览

### 语言

- 泛型（Generics）
- 增强 for 循环（for-each）
- 自动装箱 / 拆箱（Autoboxing）
- 枚举类型（`enum`）
- 变长参数（Varargs）
- 静态导入（`import static`）
- 注解（Annotations / 元数据）

### 类库

- `java.util.concurrent`（JUC 并发包）
- `java.util.Scanner`
- `Formatter` / `printf` 风格格式化输出

---

## 泛型

参数化类型，编译期类型检查，减少强制类型转换（详见 [Java 泛型（Generics）](./generics.md)）：

```java
List<String> list = new ArrayList<String>();
list.add("hello");
String s = list.get(0); // 无需 (String) 强转
```

JDK 7 起可用钻石操作符 `<>` 简化右侧类型声明（见 [JDK 7](./jdk-7.md)）。

---

## 增强 for 循环

增强 for 循环（for-each）是语法糖：编译器对**数组**展开为下标循环，对 **`Iterable`** 展开为 `Iterator` 遍历，字节码层面与手写等价。

JDK 5 之前遍历数组需用下标访问；遍历 `Collection` 则依赖 `Iterator`（完整 1.4 写法见 [JDK 1.4](./jdk-1-4.md)）。注意：**泛型也是 JDK 5 才引入**，JDK 1.4 不能写 `List<String>`，只能用 raw type 并在取出元素时强转：

```java
// JDK 1.4：数组
int[] arr = {1, 2, 3};
for (int i = 0; i < arr.length; i++) {
    System.out.println(arr[i]);
}

// JDK 1.4：集合（无泛型，需强转；asList 只能传数组，见下文）
List list = Arrays.asList(new String[] {"a", "b", "c"});
for (Iterator it = list.iterator(); it.hasNext(); ) {
    System.out.println((String) it.next());
}
```

JDK 5 起支持[变长参数](#变长参数)，`Arrays.asList("a", "b", "c")` 才无需先构造数组。下面为 JDK 5 写法：

```java
int[] arr = {1, 2, 3};
for (int n : arr) {
    System.out.println(n);
}

List<String> list = Arrays.asList("a", "b", "c");
for (String s : list) {
    System.out.println(s);
}
```

---

## 自动装箱与拆箱

基本类型与包装类之间自动转换：

```java
List<Integer> list = new ArrayList<>();
list.add(42);          // int → Integer
int x = list.get(0);   // Integer → int
```

---

## 枚举

类型安全的枚举常量，可带字段与方法：

```java
public enum Season {
    SPRING, SUMMER, AUTUMN, WINTER
}
```

---

## 变长参数

方法最后一个参数可声明为变长参数，本质是语法糖，编译器按数组处理：

```java
public class Varargs {
    public static void test(String... args) {
        for (String arg : args) {
            System.out.println(arg);
        }
    }

    public static void main(String[] args) {
        test();                              // 0 个参数
        test("a");                           // 1 个参数
        test("a", "b");                      // 多个参数
        test(new String[] {"a", "b", "c"});  // 直接传数组
    }
}
```

---

## 静态导入

导入类的静态成员，简化调用：

```java
import static java.lang.Math.PI;
import static java.lang.Math.pow;

double area = PI * pow(r, 2);
```

---

## 注解

为代码附加元数据，供编译器或运行时框架读取（如 `@Override`、`@Deprecated`；JDK 5 内置注解，也可自定义；详见 [Java Annotation（注解）](./annotation.md)）：

```java
@Override
public String toString() {
    return "example";
}
```

注解成为语言特性后，框架不必再只靠 XML 描述元数据，可在启动或类加载时通过反射读取。典型例子：[Spring](../spring/spring.md) 在 1.x 时代以 XML 配置 Bean；**Spring 2.0 / 2.5（2006–2007）** 起才大规模采用自定义注解（`@Autowired`、`@Transactional`、`@RequestMapping` 等）——这些注解本身由 Spring 用 `@interface` 定义，依赖的正是 JDK 5 提供的注解机制与 Java 5 基线。

---

## java.util.concurrent

JSR 166 引入的并发工具包，包括 `ExecutorService`、`ConcurrentHashMap`、`CountDownLatch`、`BlockingQueue` 等，是后续 Java 并发编程的基础。

---

## 与其它版本

- 上一版本：[JDK 1.4](./jdk-1-4.md)——assert、NIO、正则、JUL 等
- JDK 6（1.6）：脚本引擎、Web Service 增强等，改动相对 JDK 5 较小
- JDK 7：[JDK 7](./jdk-7.md)——try-with-resources、NIO.2、ForkJoin 等
- JDK 8：[JDK 8](./jdk-8.md)——Lambda、Stream、`java.time`

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-06-20 | 重命名为 `jdk-5-features.md`；扩展为 JDK 5 全特性概览；补充版本号说明 | 整理文档；记录版本命名演变 |
| 2026-06-20 | title 改为「JDK 5 特性」 | 「新特性」仅适用于发布当期，回顾性文档用「特性」 |
| 2026-06-20 | 重命名为 `jdk-5.md`；title 改为「JDK 5」；url 改为 `jdk-5` | 全系列统一简洁命名 |
| 2026-06-20 | 泛型章节关联 [Java 泛型（Generics）](./generics.md) | 站内已有专题文档 |
| 2026-06-20 | 增强 for 循环章节补充 JDK 1.4 对比写法 | 便于理解语法演进 |
| 2026-06-20 | 修正 JDK 1.4 集合示例：去掉泛型语法，改用 raw type + 强转 | 泛型与 for-each 同为 JDK 5 引入 |
| 2026-06-20 | JDK 1.4 集合示例改回 `Arrays.asList` + 数组；变长参数说明链到本文 §变长参数 | 示例更简洁，与文档内章节呼应 |
| 2026-06-20 | 增强 for 循环章节补充语法糖说明 | 与变长参数章节表述一致 |
| 2026-06-20 | 关联 [JDK 1.4](./jdk-1-4.md) | 新建 1.4 特性文档，互为引用 |
| 2026-06-20 | 版本号说明精简，链到 [Java 版本历史](./java-version-history.md) | 集中维护命名演变 |
| 2026-06-21 | 注解章节关联 `annotation.md` | 站内已有专题文档 |
| 2026-06-24 | 补充 Tiger EA/Beta 时间线；注解章节关联 Spring 采用注解的历程 | 厘清 JDK 5 预览版与框架演进关系 |
| 2026-06-24 | 新增「发布历程」表（JSR 175 / Tiger EA / Beta / GA） | 集中维护 JDK 5 预览与正式版时间线 |
