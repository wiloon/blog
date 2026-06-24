---
title: Java Annotation（注解）
author: "-"
date: 2011-12-26T05:36:33+00:00
lastmod: 2026-06-24T09:40:55+08:00
url: annotation
categories:
  - Java
tags:
  - java
  - annotation
  - remix
  - AI-assisted
---

Annotation 是 [Java 5](./jdk-5.md) 引入的语言特性，中文一般叫注解。它提供了一种类似注释的机制，用来将元数据（metadata）与程序元素（类、方法、成员变量等）关联起来。

更通俗地说，注解为程序元素加上与业务逻辑无关的说明信息，供框架或工具在编译期、类加载期或运行期读取和处理。注解本身不会改变程序的执行逻辑；JVM 执行字节码时会忽略注解，只有通过反射或注解处理器才能访问其中的信息。

## 框架中的注解（以 Spring 为例）

JDK 5 提供的是 **语言机制**（`@interface`、`@Retention`、反射 API）；框架上的 `@Autowired`、`@Controller` 等是 **框架用 `@interface` 自定义的注解**，不是 JDK 内置。容器在启动时扫描类路径、读取注解元数据，再决定注册哪些 Bean、如何注入、如何映射 URL。

| 时期 | 典型配置方式 |
| ---- | ------------ |
| Spring 1.x（2004 起） | 几乎全 **XML**（`<bean>`、`<property>`）；不要求 JDK 5 |
| Spring 2.5（2007） | **XML 骨架** + `@Autowired`、`@Component` / `@Service`、`@Controller`、`@RequestMapping` 等 |
| Spring 3.0（2009） | `@Configuration` + `@Bean`（Java Config），**技术上可零 XML**，但需手写各基础设施 |
| Spring Boot（2014） | 自动配置 + `application.yml`，常见场景几乎不用 XML 或大量 `@Configuration` |

时间上有先后：**[JDK 5](./jdk-5.md) GA（2004-09）** 早于 Spring 大规模注解化（**2006–2007**）；Spring 1.0（2004-03）发布时 JDK 5 尚未 GA，1.x 自然以 XML 为主。整体脉络见 [Spring](./spring/spring.md) §与 JDK 5 注解的关系。

## 注解类型与 @interface

Java 用 `@interface` **声明注解类型**（annotation type）。例如 `public @interface MyTag { ... }` 定义了一种名为 `MyTag` 的注解；在类、方法等上写 `@MyTag(...)` 则是**使用该注解**为程序元素附加元数据。

`@interface` 在规范里叫**注解类型声明语法**，由 `@` 与关键字 `interface` 组合而成。它**不是** JLS 关键字表里的单独一项（不像 `class`、`interface` 那样单列），日常说「用 `@interface` 定义注解」指的就是这种声明形式。

与普通 `interface` 相比：

1. 声明方式不同：定义注解类型必须用 `@interface`，不能写成 `interface`。编译器会令该类型隐式实现 `java.lang.annotation.Annotation`；它是注解类型，不是用 `interface` 声明的普通接口。

2. 成员与方法受限制：必须是无参数、无异常声明的方法。方法名即成员名，返回值即成员类型。返回值只能是 primitive、`Class`、枚举、annotation，或这些类型的一维数组。可用 `default` 声明默认值，但不能用 `null` 作为默认值。Annotation 的方法不能使用泛型参数；只有返回 `Class` 的方法可以在 annotation 类型中使用泛型（通过类型转换处理）。

   下面是一个合法的自定义注解，成员类型覆盖了上述几种允许的形式：

```java
public @interface MyTag {

    // primitive
    int priority() default 0;

    // String
    String label();

    // Class（可写泛型，如 Class<? extends Runnable>）
    Class<?> handler();

    // 枚举
    Level level() default Level.INFO;

    // 另一个 annotation（嵌套注解）
    Deprecated deprecated() default @Deprecated;

    // 一维数组
    String[] tags() default {};

    enum Level { DEBUG, INFO, WARN }
}
```

   使用时为成员赋值，未指定 `default` 的成员必须显式提供：

```java
@MyTag(
    label = "export",
    handler = ExportService.class,
    level = MyTag.Level.WARN,
    tags = {"report", "csv"}
)
public void exportReport() { }
```

   与普通 interface 对比，以下写法在 annotation 中**不允许**：

```java
// ❌ 不能有参数
String name(String prefix);

// ❌ 不能抛异常
int count() throws IOException;

// ❌ 不能用 null 作默认值
String desc() default null;

// ❌ 方法本身不能用泛型参数
<T> Class<T> type();
```

3. Annotation 类型与接口也有相似之处：可以定义常量、静态成员类型（如枚举），也可以被实现或继承。

## 应用场合

Annotation 通常作为辅助机制用在框架或工具中。JUnit、Struts、Spring 等流行框架都广泛使用注解，根据注解信息改变程序元素的行为或执行不同的处理流程。

## JDK 内置标准注解

Java 5 起在 `java.lang` 包中自带三种标准注解。

### @Override

`java.lang.Override` 是 marker annotation，标注在方法上，表明该方法重写了父类方法。若标注的方法实际上并未覆盖父类方法，编译器会报错。它相当于在覆盖父类方法时加一道校验，避免方法名写错。

### @Deprecated

`@Deprecated` 也是 marker annotation。标注在类型或成员上时，编译器会提示不鼓励继续使用。若通过继承或覆盖的方式使用了被 `@Deprecated` 标注的类型或成员，即使子类本身未标注，编译器仍会警告。

注意：`@Deprecated`（编译器识别）与 Javadoc 中的 `@deprecated` tag（由 javadoc 工具识别，用于生成文档说明）是两回事。

### @SuppressWarnings

用于关闭编译器对类、方法或字段的警告。它不是 marker annotation，有一个 `String[]` 类型的 `value` 成员，值为要抑制的警告名。`-Xlint` 有效的警告名对 `@SuppressWarnings` 同样有效；无法识别的警告名会被忽略。

语法允许在注解名后写括号，括号内用逗号分隔的 `name=value` 为成员赋值：

```java
@SuppressWarnings(value = {"unchecked", "fallthrough"})
public void lintTrap() { /* ... */ }
```

`@SuppressWarnings` 只有单一成员且名为 `value` 时可缩写：

```java
@SuppressWarnings({"unchecked", "fallthrough"})
@SuppressWarnings("unchecked")  // 只有一个警告时可省去大括号
```

常用 `value` 取值：

| 值 | 说明 |
| --- | --- |
| `deprecation` | 使用了过时的类或方法 |
| `unchecked` | 执行了未检查的转换 |
| `fallthrough` | switch 缺少 break 直接落入下一 case |
| `path` | 类路径、源文件路径等不存在 |
| `serial` | 可序列化类缺少 `serialVersionUID` |
| `finally` | finally 子句不能正常完成 |
| `all` | 以上所有情况 |

## 元注解

元注解是修饰注解的注解，定义在 `java.lang.annotation` 包中。

### @Documented

让注解信息出现在 Javadoc 生成的 API 文档中。未加 `@Documented` 的注解不会出现在文档里。

### @Target

指定注解可作用的程序元素，参数为 `ElementType` 枚举：

| 值 | 作用范围 |
| --- | --- |
| `TYPE` | 类、接口、枚举、annotation 类型 |
| `FIELD` | 字段（含枚举常量） |
| `METHOD` | 方法（不含构造方法） |
| `PARAMETER` | 方法参数 |
| `CONSTRUCTOR` | 构造方法 |
| `LOCAL_VARIABLE` | 局部变量 |
| `ANNOTATION_TYPE` | annotation 类型本身 |
| `PACKAGE` | 包 |

`@Target` 自身只能标注在 `ANNOTATION_TYPE` 上。若自定义注解未指定 `@Target`，则可用于以上所有元素。

示例：

```java
@Target(ElementType.METHOD)
@Target(value = ElementType.METHOD)
@Target({ElementType.METHOD, ElementType.CONSTRUCTOR})
```

### @Retention

指定注解的保留策略，参数为 `RetentionPolicy` 枚举：

| 策略 | 说明 |
| --- | --- |
| `SOURCE` | 仅保留在源文件，编译后丢弃（如 `@Override`） |
| `CLASS` | 保留在 `.class` 中，默认不暴露给运行时反射；编译期工具、字节码库仍可读取（默认值） |
| `RUNTIME` | 保留在 `.class` 文件，JVM 加载后仍可通过反射读取（如 `@Deprecated`） |

保留范围逐级扩大：`SOURCE` 最短，只到编译前；`CLASS` 会写入 `.class`，但运行时反射读不到；`RUNTIME` 最长，运行时仍可通过反射 API 读取。

自定义注解若未写 `@Retention`，默认为 `CLASS`；此时 `Class.getAnnotation()` 等反射 API 读不到该注解。

选择建议：

- 运行时需要反射读取 → `RUNTIME`
- 编译期注解处理器生成代码、运行时不需要反射读取 → `CLASS`
- 仅做编译期检查（如 `@Override`、`@SuppressWarnings`）→ `SOURCE`

### @Inherited

`@Inherited` 标在**注解类型**的声明上（元注解），不是标在业务类上。它控制的是：某个注解修饰父类时，子类在反射查询时是否也算带有该注解。

- 注解类型**带** `@Inherited`：父类打了该注解后，子类即使未显式声明，`getAnnotation()`、`isAnnotationPresent()` 等 API 仍会认为子类也有；实现上会沿超类继承链向上查找，直到找到或到达 `Object`
- 注解类型**不带** `@Inherited`：注解只作用在声明它的那个类上，子类反射时查不到父类上的该注解

这不是 OOP 意义上的「类能不能被 extends」——类本来就可以继承。`@Inherited` 只影响「父类上的注解，子类在反射里算不算也有」。子类 `.class` 字节码里通常并没有这份注解，是反射 API 查询时沿继承链解析的结果；Spring 等框架识别子类是否具备某类注解，依赖的就是这套机制。

其他限制：

- 仅对标注在**类**上的注解有效，对方法、字段等无效
- 只从超类继承，**不**从实现的接口继承

Spring Boot 中 `@SpringBootApplication` 带有 `@Inherited`，因此子类可通过反射查到该注解；但 `@Service` 等不带 `@Inherited`，子类上查不到。

```java
@SpringBootApplication
@Service
public class Person { }

public class Employee extends Person { }

// Employee.class.isAnnotationPresent(SpringBootApplication.class) → true
// Employee.class.isAnnotationPresent(Service.class) → false
```

## 自定义注解

### 定义规则

所有 annotation 类型自动继承 `java.lang.annotation.Annotation`，不能再继承其他类或接口。

定义时注意：

1. 只能用 `public` 或默认（包访问）修饰
2. 成员类型只能是 primitive、`String`、`Class`、枚举、annotation 或其数组
3. 若只有一个成员，建议命名为 `value`，使用时可以省略 `value=`

### 示例：定义与使用

```java
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Inherited
public @interface Test {
    int id();
    String description() default "no description";
}
```

```java
public class TestDemo {

    @Test(id = 1, description = "hello method_1")
    public void method_1() { }

    @Test(id = 2)
    public void method_2() { }

    @Test(id = 3, description = "last method")
    public void method_3() { }
}
```

成员可以是枚举类型，并指定默认值：

```java
@Retention(RetentionPolicy.RUNTIME)
@Target({ElementType.METHOD, ElementType.CONSTRUCTOR})
public @interface Greeting {

    enum FontColor { BLUE, RED, GREEN }

    String name();
    FontColor fontColor() default FontColor.RED;
}
```

### 完整示例：类级与方法级注解

**Description.java**（类级注解）：

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
@Documented
public @interface Description {
    String value();
}
```

**Author.java**（方法级注解）：

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
@Documented
public @interface Author {
    String name();
    String group();
}
```

**Utility.java**（被注解的类）：

```java
@Description("这是一个有用的工具类")
public class Utility {

    @Author(name = "wiloon", group = "com.wiloon")
    public String work() {
        return "work over!";
    }
}
```

## 通过反射读取注解

要通过反射读取注解，必须将 `@Retention` 设为 `RUNTIME`。示例中的 `Class<?>` 表示任意类型的 [`Class`](./lang-class.md) 对象；获取方式见该文。

```java
import java.lang.reflect.Method;

public class AnalysisAnnotation {

    public static void main(String[] args) throws Exception {
        Class<?> clazz = Class.forName("com.example.Utility");

        if (clazz.isAnnotationPresent(Description.class)) {
            Description desc = clazz.getAnnotation(Description.class);
            System.out.println("Description → " + desc.value());
        }

        for (Method method : clazz.getMethods()) {
            if (method.isAnnotationPresent(Author.class)) {
                Author author = method.getAnnotation(Author.class);
                System.out.println("Author → " + author.name()
                    + " from " + author.group());
            }
        }
    }
}
```

解析 `Test` 注解的示例：

```java
public class ParseTest {

    public static void main(String[] args) {
        for (Method method : TestDemo.class.getDeclaredMethods()) {
            if (method.isAnnotationPresent(Test.class)) {
                Test ann = method.getAnnotation(Test.class);
                System.out.println("Test(method = " + method.getName()
                    + ", id = " + ann.id()
                    + ", description = " + ann.description() + ")");
            }
        }
    }
}
```

输出：

```text
Test(method = method_1, id = 1, description = hello method_1)
Test(method = method_2, id = 2, description = no description)
Test(method = method_3, id = 3, description = last method)
```

更通用的读取方式——遍历方法上所有注解及其成员：

```java
import java.lang.annotation.Annotation;
import java.lang.reflect.Method;

public class ReadAnnotationInfo {

    public static void main(String[] args) throws Exception {
        Class<?> c = Class.forName("com.example.AnnotationTest");
        for (Method method : c.getDeclaredMethods()) {
            System.out.println(method.getName());
            for (Annotation an : method.getDeclaredAnnotations()) {
                System.out.println("  注解: " + an.annotationType().getSimpleName());
                for (Method meth : an.annotationType().getDeclaredMethods()) {
                    System.out.println("    成员: " + meth.getName());
                }
            }
        }
    }
}
```

## 参考来源

- [Annotation/注解 - 博客园](https://www.cnblogs.com/mandroid/archive/2011/07/18/2109829.html)
- [@Inherited 注解用法 - CSDN](https://blog.csdn.net/liuwenbo0920/article/details/7290586)
- [Java 注解(Annotation) - 博客园](https://www.cnblogs.com/hzhuxin/p/7799899.html)

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-06-19 | 文件重命名为 `annotation.md`；去重合并多篇转载内容；修正代码块与标题层级；更新 front matter | 原文由多篇博客拼接，重复严重、格式混乱 |
| 2026-06-19 | 在「Annotation 与 interface 的异同」第 2 点补充成员类型与限制示例 | 说明较抽象，补充可运行示例便于理解 |
| 2026-06-21 | 首段「Java 5」链接至 `jdk-5.md` | 关联 JDK 5 专用文档 |
| 2026-06-21 | 修订「@Retention」：澄清保留范围、默认 `CLASS` 与反射关系、更新选择建议表述 | 消除「前者能作用的地方」歧义，补充常见踩坑点 |
| 2026-06-21 | 「Annotation 与 interface」改为「注解类型与 @interface」；补充声明语法术语与定义/使用区分 | 原文未点明 `@interface` 用途，且误称为关键字 |
| 2026-06-21 | 「通过反射读取注解」链至 `java-lang-class.md` | Class 概念独立成文 |
| 2026-06-23 | 扩充「@Inherited」：澄清元注解作用对象、反射语义继承与不带 `@Inherited` 时的差异 | 消除「注解继承」与「类继承」的歧义 |
| 2026-06-24 | 新增「框架中的注解（以 Spring 为例）」；链到 spring.md、jdk-5.md | 厘清 JDK 5 语言特性与 Spring 注解化时间线 |
| 2026-06-24 | Spring 配置表补充 2.5 XML 混合期、3.0 Java Config、Boot 自动配置分工 | 与 spring.md 配置演进章节对齐 |
