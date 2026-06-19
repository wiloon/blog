---
title: Java 泛型（Generics）
author: "-"
date: 2011-12-26T09:57:58+00:00
lastmod: 2026-06-19T17:56:45+08:00
url: generics
categories:
  - Java
tags:
  - java
  - generics
  - remix
  - AI-assisted
aliases:
  - /java-generic
---

泛型是 JDK 5 引入的类型机制，本质是将类型参数化。可以把类型参数看作占位符：在定义类、接口或方法时声明 `T`、`K`、`V` 等类型变量，在使用时填入具体类型（如 `String`、`Integer`）。

泛型带来的主要好处：

- **可读性**：从声明即可看出集合或容器中的元素类型
- **类型安全**：非法类型在编译期报错，而非运行时才抛出 `ClassCastException`
- **消除强制转换**：`List<String>` 的 `get()` 直接返回 `String`

## 为什么类型参数不能是 primitive

类型参数只能是**引用类型**（类、接口、枚举、数组、annotation），不能是 [基本数据类型](./primitive-types.md)（primitive）。根本原因是：Java 泛型在语言规范和实现上，都只面向引用类型。

### 语言规范直接规定

JLS 要求类型参数的边界必须是引用类型。`int`、`double`、`boolean` 等 primitive 不是类，不能作为 `T` 填入：

```java
List<int> list;       // ❌ 编译错误
List<Integer> list;   // ✅ 用包装类代替
```

### 泛型靠类型擦除实现，擦除后是 Object

Java 泛型在编译后会被**擦除**：`List<String>` 运行时其实就是 `List`，元素按 `Object` 处理。引用类型可以统一向上转型到 `Object`，而 primitive **不是** `Object` 的子类型，也**不能**直接赋给 `Object` 变量（必须先装箱）：

```java
Object o = "hello";                  // ✅
Object o = 42;                       // ❌ int 不能赋给 Object
Object o = Integer.valueOf(42);      // ✅ 装箱后才是引用类型
```

泛型容器在字节码层面按「对象引用」运作，primitive 放不进去这套模型。

### 设计取舍：兼容优先，而非真泛型

C++ 模板会为 `int`、`double` 各生成一份特化代码。Java 为了**不改动 JVM、不破坏已有字节码**，选择了擦除方案：泛型主要是编译期检查，运行时几乎「不存在」。在这种实现下，只支持所有引用类型共用的机制，没有为每种 primitive 单独生成特化版本。这不是技术上完全做不到，而是 Java 在引入泛型时做的取舍。

### 实际做法：用包装类

需要存放数值时，使用对应的包装类，配合 [自动装箱拆箱](./java-wrapper.md)：

| primitive | 包装类 |
| --- | --- |
| `int` | `Integer` |
| `long` | `Long` |
| `double` | `Double` |
| `boolean` | `Boolean` |
| `char` | `Character` |
| `byte` | `Byte` |
| `short` | `Short` |
| `float` | `Float` |

```java
List<Integer> nums = new ArrayList<>();
nums.add(42);        // 自动装箱：int → Integer
int n = nums.get(0); // 自动拆箱：Integer → int
```

代价是装箱会产生额外对象开销。对性能敏感的场景，应使用 `int[]` 等原生数组，或 Guava 的 `IntList` 等专门结构，而不是期望 `List<int>` 存在。

## 与 Object「伪泛型」的对比

没有泛型时，常用 `Object` 作为通用成员类型，取出时再强转：

```java
class Gen2 {
    private Object ob;

    public Gen2(Object ob) { this.ob = ob; }
    public Object getOb() { return ob; }
}

Gen2 intOb = new Gen2(88);
int i = (Integer) intOb.getOb();  // 必须强转，类型错误要到运行时才暴露
```

使用泛型后，编译器在编译期完成类型检查：

```java
class Gen<T> {
    private T ob;

    public Gen(T ob) { this.ob = ob; }
    public T getOb() { return ob; }

    public void showType() {
        System.out.println("T 的实际类型: " + ob.getClass().getName());
    }
}

Gen<Integer> intOb = new Gen<>(88);
int i = intOb.getOb();  // 无需强转

Gen<String> strOb = new Gen<>("Hello Gen!");
String s = strOb.getOb();
```

构造时建议写尖括号指定类型参数；若省略，默认按 `Object` 处理，使用时仍需强转。

## 基本规则

1. 类型参数只能是引用类型，不能是 primitive（见上文「为什么类型参数不能是 primitive」）
2. 同一泛型类的不同类型实参互不兼容：`List<String>` 与 `List<Integer>` 是不同类型
3. 可以有多个类型参数：`Map<K, V>`
4. 可用 `extends` 限制上界（有界类型）
5. 可用通配符 `?` 表示未知类型

## 有界类型参数

`extends` 在这里表示「上界约束」，后面可以是类或接口：

```java
class CollectionGenFoo<T extends Collection> {
    private T x;
    public CollectionGenFoo(T x) { this.x = x; }
    public T getX() { return x; }
}

CollectionGenFoo<ArrayList> listFoo = new CollectionGenFoo<>(new ArrayList<>());
```

## 通配符

### 为什么需要通配符

这里的「编译期无法固定」，不是说运行时才确定类型，而是指：**你不想、也不能在声明处写死一个具体的类型参数**，但又需要表达「某种满足约束的类型」。

泛型类型是**不变的**（invariant）：类型参数一旦写死，就必须精确匹配，不能像普通引用那样向上转型：

```java
ArrayList list = new ArrayList();
Collection col = list;  // ✅ 引用类型可以向上转型

List<String> strList = new ArrayList<>();
// List<Object> objList = strList;  // ❌ 泛型不行
```

`CollectionGenFoo<ArrayList>` 与 `CollectionGenFoo<Collection>` 也是两种完全不同的类型，即使 `ArrayList` 实现了 `Collection`。

接上文的 `CollectionGenFoo`，若把类型参数固定为某一种实现，赋值就会失败：

```java
// ✅ T 固定为 ArrayList，两边一致
CollectionGenFoo<ArrayList> a = new CollectionGenFoo<>(new ArrayList<>());

// ❌ 右边推断为 CollectionGenFoo<ArrayList>，不能赋给 CollectionGenFoo<Collection>
// CollectionGenFoo<Collection> b = new CollectionGenFoo<>(new ArrayList<>());
```

实际需求往往是：变量既要能接住 `ArrayList`，也要能接住 `LinkedList`、`HashSet` 等——**具体是哪一个 `T` 在写变量类型时不应定死**，只应表达「某个 `Collection` 的实现类」。

通配符 `?` 表示**未知但有限制的类型**，用 `? extends Collection` 只约束上界，不绑定具体实现：

```java
CollectionGenFoo<? extends Collection> foo =
    new CollectionGenFoo<>(new ArrayList<>());    // T = ArrayList
foo = new CollectionGenFoo<>(new LinkedList<>()); // T = LinkedList
```

### 写通用 API 时的用法

方法参数若写死 `List<String>`，只能接收 `List<String>`。若要接收 `List<Integer>`、`List<Double>` 等不同元素类型，同样无法在签名里固定一个具体 `T`，此时用通配符：

```java
void print(List<?> list) {  // 任意元素类型
    for (Object o : list) { /* ... */ }
}

void sum(List<? extends Number> nums) {  // Integer、Double 均可
    /* ... */
}
```

### 语法与 PECS

| 写法 | 含义 |
| --- | --- |
| `?` | 任意引用类型（默认上界为 `Object`） |
| `? extends T` | 上界为 `T`，可读（适合读取） |
| `? super T` | 下界为 `T`，可写（适合写入） |

PECS 记忆法：**Producer Extends, Consumer Super**——只读用 `extends`，只写用 `super`。

```java
// 只读：可以安全地当作 Number 取出
List<? extends Number> nums = new ArrayList<Integer>();
Number n = nums.get(0);
// nums.add(1);  // 编译错误

// 只写：可以安全地放入 Integer 及其子类
List<? super Integer> ints = new ArrayList<Number>();
ints.add(42);
```

## 泛型不是协变的

上文通配符一节已说明：`List<Integer>` 不能赋给 `List<Number>`。数组则相反，是协变的：

```java
Integer[] intArray = new Integer[10];
Number[] numberArray = intArray;  // ✅ 数组可以协变

List<Integer> intList = new ArrayList<>();
// List<Number> numberList = intList;  // ❌ 泛型不行
```

若允许上述赋值，`numberList.add(3.14f)` 就会破坏 `intList` 的类型安全。

## 泛型方法

泛型方法与所在类是否为泛型类无关。将类型参数列表放在返回值之前：

```java
public class Example {

    public <T> void print(T x) {
        System.out.println(x.getClass().getName());
    }

    public <T> T identity(T x) {
        return x;
    }

    // static 方法无法使用类的类型参数，必须声明为泛型方法
    public static <T> T staticIdentity(T x) {
        return x;
    }
}
```

调用时通常不必显式指定类型参数，编译器会推断：

```java
String s = identity("hello");
```

选择泛型方法而非在类上声明 `T` 的常见原因：

- 方法是 `static` 的
- 类型约束只对该方法局部有效，不必污染整个类签名

### 有界泛型方法

```java
public static <T extends Comparable<T>> T max(T a, T b) {
    return a.compareTo(b) > 0 ? a : b;
}

String s = max("moo", "bark");  // 编译器推断 T 为 String
```

## 命名约定

| 参数 | 常见用途 |
| --- | --- |
| `T` | 通用类型（Type） |
| `E` | 集合元素（Element） |
| `K` | 键（Key） |
| `V` | 值（Value） |

以上为行业惯例，**不是语法强制要求**。类型参数只要是合法 Java 标识符即可，例如 `class Box<Content>` 或 `interface Mapper<Input, Output>` 都能编译通过。参数较多或含义不明显时，也可用 `From`/`To` 等更有语义的名称，关键是保持一致、便于阅读。

## 类型擦除

Java 泛型通过**擦除**实现：编译后字节码中，类型参数被替换为其上界（无界则为 `Object`）。因此：

- `List<String>` 与 `List<Integer>` 运行时都是同一个 `List` 类
- 不能 `new T()`、不能创建 `T[]`、不能在运行时获取 `T` 的实际类型
- 泛型信息在反射中可通过 `ParameterizedType` 等有限获取，但运行时容器本身不保留元素类型

```java
new ArrayList<String>().getClass() == new ArrayList<Integer>().getClass()  // true
```

## 类库中的泛型

JDK 集合框架已全面泛型化：`Collection<E>`、`List<E>`、`Set<E>`、`Map<K,V>`。`Comparable<T>`、`Class<T>`、`Enum<E>` 等也使用了泛型。

常见用法：

```java
Map<String, String> m = new HashMap<>();
m.put("key", "value");
String s = m.get("key");  // 无需强转
```

## 与非泛型代码互操作

不带类型参数的泛型声明称为**原始类型**（raw type），如 `List` 而非 `List<String>`。原始类型与任意参数化类型赋值兼容，但会产生 unchecked 警告，类型安全由程序员自行保证。

```java
List raw = new ArrayList();
raw.add("hello");
raw.add(42);  // 编译通过，运行期可能 ClassCastException

@SuppressWarnings("unchecked")
List<String> strings = raw;
```

JDK 5 起现有非泛型代码无需修改即可编译运行，但未使用泛型的代码无法获得编译期类型检查的好处。

## 参考来源

- [Java 泛型 - OSChina](https://my.oschina.net/polly/blog/877647)

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-06-19 | 文件重命名为 `generics.md`；去重合并教程与长篇转载；修正代码块；`url` 改为 `generics` 并保留 `/java-generic` 别名 | 文件名含中文；原文由多篇内容拼接，重复严重且部分泛型符号丢失 |
| 2026-06-19 | 新增「为什么类型参数不能是 primitive」章节 | 补充语言规范、类型擦除与设计取舍说明 |
| 2026-06-19 | 扩充「通配符」章节：泛型不变性、`CollectionGenFoo` 示例、通用 API 用法 | 原表述「编译期无法固定」易误解，补充动机说明 |
| 2026-06-19 | 「命名约定」补充说明：惯例非语法强制，可用任意合法标识符 | 澄清 T/E/K/V 仅为推荐 |
