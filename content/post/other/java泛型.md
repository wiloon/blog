---
title: java generic, 泛型
author: "-"
date: 2011-12-26T09:57:58+00:00
url: java-generic
categories:
  - Java
tags:$
  - reprint
---
## java generic, 泛型
# 泛型, generic
泛型是jdk5引入的类型机制，本质是将类型参数化(是早在1999年就制定的jsr14的实现)

也就是说所操作的数据类型被指定为一个参数。这种参数类型可以用在类、接口和方法的创建中，分别称为泛型类、泛型接口、泛型方法。 Java语言引入泛型的好处是安全简单。

泛型解决了几个问题: 

1 可读性，从字面上就可以判断集合中的内容类型；

2 类型检查，避免插入非法类型。

3 获取数据时不在需要强制类型转换。


在Java SE 1.5之前，没有泛型的情况的下，通过对类型(Object)的引用来实现参数的"任意化"，"任意化"带来的缺点是要做显式的强制类型转换，而这种转换是要求开发者对实际参数类型可以预知的情况下进行的。对于强制类型转换错误的情况，编译器可能不提示错误，在运行的时候才出现异常，这是一个安全隐患。
  
泛型的好处是在编译的时候检查类型安全，并且所有的强制转换都是自动和隐式的，提高代码的重用率。

规则和限制
  
1. 泛型的类型参数只能是类类型 (包括自定义类) ，不能是简单类型。
  
2. 同一种泛型可以对应多个版本 (因为参数类型是不确定的) ，不同版本的泛型类实例是不兼容的。
  
3. 泛型的类型参数可以有多个。
  
4. 泛型的参数类型可以使用extends语句，例如。习惯上称为"有界类型"。
  
5. 泛型的参数类型还可以是通配符类型。例如Class<?> classType = Class.forName("java.lang.String");

泛型还有接口、方法等等，内容很多，需要花费一番功夫才能理解掌握并熟练应用。在此给出我曾经了解泛型时候写出的两个例子 (根据看的印象写的) ，实现同样的功能，一个使用了泛型，一个没有使用，通过对比，可以很快学会泛型的应用，学会这个基本上学会了泛型70%的内容。

例子一: 使用了泛型

```java
  
package com.wiloon.test.generics;

class Gen<T> {
      
private T ob; // 定义泛型成员变量

public Gen(T ob) {
      
this.ob = ob;
      
}

public T getOb() {
      
return ob;
      
}

public void setOb(T ob) {
      
this.ob = ob;
      
}

public void showType() {
      
System.out.println("T的实际类型是: " + ob.getClass().getName());
      
}
  
}

public class GenDemo {
      
public static void main(String[] args) {
      
// 定义泛型类Gen的一个Integer版本
      
Gen<Integer> intOb = new Gen<Integer>(88);
      
intOb.showType();
      
int i = intOb.getOb();
      
System.out.println("value= " + i);
      
System.out.println("------------");
      
// 定义泛型类Gen的一个String版本
      
Gen<String> strOb = new Gen<String>("Hello Gen!");
      
strOb.showType();
      
String s = strOb.getOb();
      
System.out.println("value= " + s);
      
}
  
}
  
```

例子二: 没有使用泛型

```java
  
package com.wiloon.test.generics;

class Gen2 {
      
private Object ob; // 定义一个通用类型成员

public Gen2(Object ob) {
      
this.ob = ob;
      
}

public Object getOb() {
      
return ob;
      
}

public void setOb(Object ob) {
      
this.ob = ob;
      
}
public void showTyep() {
System.out.println("T的实际类型是: " + ob.getClass().getName());     
}
}

public class GenDemo2 {
public static void main(String[] args) {
      
// 定义类Gen2的一个Integer版本
Gen2 intOb = new Gen2(new Integer(88));
intOb.showTyep();
int i = (Integer) intOb.getOb();
System.out.println("value= " + i);
System.out.println("-----------");
      
// 定义类Gen2的一个String版本
Gen2 strOb = new Gen2("Hello Gen!");
strOb.showTyep();
String s = (String) strOb.getOb();
System.out.println("value= " + s);     
}
}
  
```

运行结果: 
两个例子运行Demo结果是相同的,控制台输出结果如下: 
  
T的实际类型是:
  
java.lang.Integer
  
value= 88
  
------------
  
T的实际类型是: java.lang.String
  
value= Hello Gen!
  
Process finished with exit code 0

看明白这个，以后基本的泛型应用和代码阅读就不成问题了。
  
编辑本段逐渐深入泛型
  
1. 没有任何重构的原始代码
  
有两个类如下，要构造两个类的对象，并打印出各自的成员x。

```java
  
package com.wiloon.test.generics;

public class StringFoo {
      
private String x;

public StringFoo(String x) {
      
this.x = x;
      
}

public String getX() {
      
return x;
      
}

public void setX(String x) {
      
this.x = x;
      
}
  
}
  
```

```java
  
package com.wiloon.test.generics;

public class DoubleFoo {
      
private Double x;

public DoubleFoo(Double x) {
      
this.x = x;
      
}

public Double getX() {
      
return x;
      
}

public void setX(Double x) {
      
this.x = x;
      
}
  
}
  
```

以上的代码实在无聊，就不写如何实现了。

2. 对上面的两个类进行重构，写成一个类
因为上面的类中，成员和方法的逻辑都一样，就是类型不一样，因此考虑重构。Object是所有类的父类，因此可以考虑用Object做为成员类型，这样就可以实现通用了，实际上就是"Object泛型"，暂时这么称呼。

```java
  
package com.wiloon.test.generics;

public class ObjectFoo {
      
private Object x;

public ObjectFoo(Object x) {
      
this.x = x;
      
}

public Object getX() {
      
return x;
      
}

public void setX(Object x) {
      
this.x = x;
      
}
  
}

```

写出Demo方法如下: 

```java
  
package com.wiloon.test.generics;

public class ObjectFooDemo {
      
public static void main(String args[]) {
      
ObjectFoo strFoo = new ObjectFoo("Hello Generics!");
      
ObjectFoo douFoo = new ObjectFoo(33.0);
      
ObjectFoo objFoo = new ObjectFoo(new Object());
      
System.out.println("strFoo.getX=" + (String) strFoo.getX());
      
System.out.println("douFoo.getX=" + (Double) douFoo.getX());
      
System.out.println("objFoo.getX=" + objFoo.getX());
      
System.out.println("strFoo.getX=" + strFoo.getX());
      
System.out.println("douFoo.getX=" + douFoo.getX());
      
}
  
}

```

运行结果如下: 
  
strFoo.getX=Hello Generics!
  
douFoo.getX=33.0
  
objFoo.getX=java.lang.Object@19821f

解说: 在Java 5之前，为了让类有通用性，往往将参数类型、返回类型设置为Object类型，当获取这些返回类型来使用时候，必须将其"强制"转换为原有的类型或者接口，然后才可以调用对象上的方法。

3. Java1.5泛型来实现
  
强制类型转换很麻烦，我还要事先知道各个Object具体类型是什么，才能做出正确转换。否则，要是转换的类型不对，比如将"Hello Generics!"字符串强制转换为Double,那么编译的时候不会报错，可是运行的时候就挂了。那有没有不强制转换的办法--有，改用 Java5泛型来实现。

```java
  
package com.wiloon.test.generics;

class GenericsFoo<T> {
      
private T x;

public GenericsFoo(T x) {
      
this.x = x;
      
}

public T getX() {
      
return x;
      
}

public void setX(T x) {
      
this.x = x;
      
}
  
}

public class GenericsFooDemo {
      
public static void main(String args[]) {
      
GenericsFoo<String> strFoo = new GenericsFoo<String>("Hello Generics!");
      
GenericsFoo<Double> douFoo = new GenericsFoo<Double>(new Double("33.0"));
      
GenericsFoo<Object> objFoo = new GenericsFoo<Object>(new Object());
      
System.out.println("strFoo.getX=" + strFoo.getX());
      
System.out.println("douFoo.getX=" + douFoo.getX());
      
System.out.println("objFoo.getX=" + objFoo.getX());
      
}
  
}
  
```

运行结果: 
  
strFoo.getX=Hello Generics!
  
douFoo.getX=33.0
  
objFoo.getX=java.lang.Object@19821f

和使用"Object泛型"方式实现结果的完全一样，但是这个Demo简单多了，里面没有强制类型转换信息。
  
下面解释一下上面泛型类的语法: 
  
使用来声明一个类型持有者名称，然后就可以把T当作一个类型代表来声明成员、参数和返回值类型。
  
当然T仅仅是个名字，这个名字可以自行定义。
  
class GenericsFoo 声明了一个泛型类，这个T没有任何限制，实际上相当于Object类型，实际上相当于 class GenericsFoo。
  
与Object泛型类相比，使用泛型所定义的类在声明和构造实例的时候，可以使用"<实际类型>"来一并指定泛型类型持有者的真实类型。类如

```java
  
GenericsFoo<Double> douFoo=new GenericsFoo<Double>(new Double("33"));
  
```

当然，也可以在构造对象的时候不使用尖括号指定泛型类型的真实类型，但是你在使用该对象的时候，就需要强制转换了。比如: GenericsFoo

```java
  
douFoo=new GenericsFoo(new Double("33"));
  
```

实际上，当构造对象时不指定类型信息的时候，默认会使用Object类型，这也是要强制转换的原因。

泛型的高级应用
  
1. 限制泛型的可用类型
  
在上面的例子中，由于没有限制class GenericsFoo类型持有者T的范围，实际上这里的限定类型相当于Object，这和"Object泛型"实质是一样的。限制比如我们要限制T为集合接口类型。只需要这么做: 
  
class GenericsFoo，这样类中的泛型T只能是Collection接口的实现类，传入非Collection接口编译会出错。
  
注意: 这里的限定使用关键字 extends，后面可以是类也可以是接口。但这里的extends已经不是继承的含义了，应该理解为T类型是实现Collection接口的类型，或者T是继承了XX类的类型。

下面继续对上面的例子改进，我只要实现了集合接口的类型: 

```java
  
package com.wiloon.test.generics;

import java.util.ArrayList;
  
import java.util.Collection;

public class CollectionGenFoo<T extends Collection> {
      
private T x;

public CollectionGenFoo(T x) {
      
this.x = x;
      
}

public T getX() {
      
return x;
      
}

public void setX(T x) {
      
this.x = x;
      
}

public static void main(String args[]) {
      
CollectionGenFoo listFoo = null;
      
listFoo = new CollectionGenFoo(new ArrayList());
      
// // 出错了,不让这么干。
      
// CollectionGenFoo<Collection> listFoo = null;
      
// listFoo = new CollectionGenFoo(new ArrayList());
      
System.out.println("实例化成功!");
      
}
  
}

```

当前看到的这个写法是可以编译通过，并运行成功。可是注释掉的两行加上就出错了，因为这么定义类型的时候，就限定了构造此类实例的时候T是确定的一个类型，这个类型实现了Collection接口，但是实现 Collection接口的类很多很多，如果针对每一种都要写出具体的子类类型，那也太麻烦了，我干脆还不如用Object通用一下。别急，泛型针对这种情况还有更好的解决方案，那就是"通配符泛型"。

2. 通配符泛型
  
为了解决类型被限制死了不能动态根据实例来确定的缺点，引入了"通配符泛型"，针对上面的例子，使用通配泛型格式为<? extends Collection>，"？"代表未知类型，这个类型是实现Collection接口。那么上面实现的方式可以写为: 

```java
  
package com.wiloon.test.generics;

import java.util.ArrayList;
  
import java.util.Collection;

public class CollectionGenFooDemo {
      
public static void main(String args[]) {
      
CollectionGenFoo<? extends Collection> listFoo = null;
      
listFoo = new CollectionGenFoo(new ArrayList());
      
// 现在不会出错了
      
listFoo = new CollectionGenFoo<Collection>(new ArrayList());
      
System.out.println("实例化成功!");
      
}

}
  
```

注意: 
  
1. 如果只指定了<?>，而没有extends，则默认是允许Object及其下的任何Java类了。也就是任意类。
  
2. 通配符泛型不单可以向下限制，如<? extends Collection>，还可以向上限制，如<? super Double>，表示类型只能接受Double及其上层父类类型，如Number、Object类型的实例。
  
3. 泛型类定义可以有多个泛型参数，中间用逗号隔开，还可以定义泛型接口，泛型方法。这些都泛型类中泛型的使用规则类似。

泛型方法
  
是否拥有泛型方法，与其所在的类是否泛型没有关系。要定义泛型方法，只需将泛型参数列表置于返回值前。如:

```java
  
package com.wiloon.test.generics;

public class ExampleA {
      
public <T> void f(T x) {
      
System.out.println(x.getClass().getName());
      
}

public void testf(String x) {

}

public <T> String testB(T x) {

return "abc";
      
}

public <T> T testC(T x) {

return x;
      
}

public static void main(String[] args) {
      
ExampleA ea = new ExampleA();
      
ea.f(" ");
      
ea.f(10);
      
ea.f('a');
      
ea.f(ea);
      
}
  
}
  
```

输出结果: 
  
java.lang.String
  
java.lang.Integer
  
java.lang.Character

ExampleA
  
使用泛型方法时，不必指明参数类型，编译器会自己找出具体的类型。泛型方法除了定义不同，调用就像普通方法一样。
  
需要注意，一个static方法，无法访问泛型类的类型参数，所以，若要static方法需要使用泛型能力，必须使其成为泛型方法。


一 泛型简介

什么是泛型？

泛型 (Generic type 或者 generics) 是对 Java 语言的类型系统的一种扩展，以支持创建可以按类型进行参数化的类。可以把类型参数看作是使用参数化类型时指定的类型的一个占位符，就像方法的形式参数是运行时传递的值的占位符一样。

可以在集合框架 (Collection framework) 中看到泛型的动机。例如，Map 类允许您向一个 Map 添加任意类的对象，即使最常见的情况是在给定映射 (map) 中保存某个特定类型 (比如 String) 的对象。

因为 Map.get() 被定义为返回 Object，所以一般必须将 Map.get() 的结果强制类型转换为期望的类型，如下面的代码所示: 

Map m = new HashMap();
  
m.put("key", "blarg");
  
String s = (String) m.get("key");

要让程序通过编译，必须将 get() 的结果强制类型转换为 String，并且希望结果真的是一个 String。但是有可能某人已经在该映射中保存了不是 String 的东西，这样的话，上面的代码将会抛出 ClassCastException。

理想情况下，您可能会得出这样一个观点，即 m 是一个 Map，它将 String 键映射到 String 值。这可以让您消除代码中的强制类型转换，同时获得一个附加的类型检查层，该检查层可以防止有人将错误类型的键或值保存在集合中。这就是泛型所做的工作。

泛型的好处

Java 语言中引入泛型是一个较大的功能增强。不仅语言、类型系统和编译器有了较大的变化，以支持泛型，而且类库也进行了大翻修，所以许多重要的类，比如集合框架，都已经成为泛型化的了。这带来了很多好处: 

类型安全。 泛型的主要目标是提高 Java 程序的类型安全。通过知道使用泛型定义的变量的类型限制，编译器可以在一个高得多的程度上验证类型假设。没有泛型，这些假设就只存在于程序员的头脑中 (或者如果幸运的话，还存在于代码注释中) 。

Java 程序中的一种流行技术是定义这样的集合，即它的元素或键是公共类型的，比如"String 列表"或者"String 到 String 的映射"。通过在变量声明中捕获这一附加的类型信息，泛型允许编译器实施这些附加的类型约束。类型错误现在就可以在编译时被捕获了，而不是在运行时当作 ClassCastException 展示出来。将类型检查从运行时挪到编译时有助于您更容易找到错误，并可提高程序的可靠性。

消除强制类型转换。 泛型的一个附带好处是，消除源代码中的许多强制类型转换。这使得代码更加可读，并且减少了出错机会。

尽管减少强制类型转换可以降低使用泛型类的代码的罗嗦程度，但是声明泛型变量会带来相应的罗嗦。比较下面两个代码例子。

该代码不使用泛型: 

List li = new ArrayList();
  
li.put(new Integer(3));
  
Integer i = (Integer) li.get(0);

该代码使用泛型: 

Listli = new ArrayList();
  
li.put(new Integer(3));
  
Integer i = li.get(0);

在简单的程序中使用一次泛型变量不会降低罗嗦程度。但是对于多次使用泛型变量的大型程序来说，则可以累积起来降低罗嗦程度。

潜在的性能收益。 泛型为较大的优化带来可能。在泛型的初始实现中，编译器将强制类型转换 (没有泛型的话，程序员会指定这些强制类型转换) 插入生成的字节码中。但是更多类型信息可用于编译器这一事实，为未来版本的 JVM 的优化带来可能。

由于泛型的实现方式，支持泛型 (几乎) 不需要 JVM 或类文件更改。所有工作都在编译器中完成，编译器生成类似于没有泛型 (和强制类型转换) 时所写的代码，只是更能确保类型安全而已。

泛型用法的例子

泛型的许多最佳例子都来自集合框架，因为泛型让您在保存在集合中的元素上指定类型约束。考虑这个使用 Map 类的例子，其中涉及一定程度的优化，即 Map.get() 返回的结果将确实是一个 String: 

Map m = new HashMap();
  
m.put("key", "blarg");
  
String s = (String) m.get("key");

如果有人已经在映射中放置了不是 String 的其他东西，上面的代码将会抛出 ClassCastException。泛型允许您表达这样的类型约束，即 m 是一个将 String 键映射到 String 值的 Map。这可以消除代码中的强制类型转换，同时获得一个附加的类型检查层，这个检查层可以防止有人将错误类型的键或值保存在集合中。

下面的代码示例展示了 JDK 5.0 中集合框架中的 Map 接口的定义的一部分: 

public interface Map{
  
public void put(K key, V value);
  
public V get(K key);
  
}

注意该接口的两个附加物: 

类型参数 K 和 V 在类级别的规格说明，表示在声明一个 Map 类型的变量时指定的类型的占位符。

在 get()、put() 和其他方法的方法签名中使用的 K 和 V。

为了赢得使用泛型的好处，必须在定义或实例化 Map 类型的变量时为 K 和 V 提供具体的值。以一种相对直观的方式做这件事: 

Mapm = new HashMap();
  
m.put("key", "blarg");
  
String s = m.get("key");

当使用 Map 的泛型化版本时，您不再需要将 Map.get() 的结果强制类型转换为 String，因为编译器知道 get() 将返回一个 String。

在使用泛型的版本中并没有减少键盘录入；实际上，比使用强制类型转换的版本需要做更多键入。使用泛型只是带来了附加的类型安全。因为编译器知道关于您将放进 Map 中的键和值的类型的更多信息，所以类型检查从执行时挪到了编译时，这会提高可靠性并加快开发速度。

向后兼容

在 Java 语言中引入泛型的一个重要目标就是维护向后兼容。尽管 JDK 5.0 的标准类库中的许多类，比如集合框架，都已经泛型化了，但是使用集合类 (比如 HashMap 和 ArrayList) 的现有代码将继续不加修改地在 JDK 5.0 中工作。当然，没有利用泛型的现有代码将不会赢得泛型的类型安全好处。

二 泛型基础

类型参数

在定义泛型类或声明泛型类的变量时，使用尖括号来指定形式类型参数。形式类型参数与实际类型参数之间的关系类似于形式方法参数与实际方法参数之间的关系，只是类型参数表示类型，而不是表示值。

泛型类中的类型参数几乎可以用于任何可以使用类名的地方。例如，下面是 java.util.Map 接口的定义的摘录: 

public interface Map{
  
public void put(K key, V value);
  
public V get(K key);
  
}

Map 接口是由两个类型参数化的，这两个类型是键类型 K 和值类型 V。 (不使用泛型) 将会接受或返回 Object 的方法现在在它们的方法签名中使用 K 或 V，指示附加的类型约束位于 Map 的规格说明之下。

当声明或者实例化一个泛型的对象时，必须指定类型参数的值: 

Mapmap = new HashMap();

注意，在本例中，必须指定两次类型参数。一次是在声明变量 map 的类型时，另一次是在选择 HashMap 类的参数化以便可以实例化正确类型的一个实例时。

编译器在遇到一个 Map类型的变量时，知道 K 和 V 现在被绑定为 String，因此它知道在这样的变量上调用 Map.get() 将会得到 String 类型。

除了异常类型、枚举或匿名内部类以外，任何类都可以具有类型参数。

命名类型参数

推荐的命名约定是使用大写的单个字母名称作为类型参数。这与 C++ 约定有所不同 (参阅 附录 A: 与 C++ 模板的比较) ，并反映了大多数泛型类将具有少量类型参数的假定。对于常见的泛型模式，推荐的名称是: 

K —— 键，比如映射的键。
  
V —— 值，比如 List 和 Set 的内容，或者 Map 中的值。
  
E —— 异常类。
  
T —— 泛型。

泛型不是协变的

关于泛型的混淆，一个常见的来源就是假设它们像数组一样是协变的。其实它们不是协变的。

如果 A 扩展 B，那么 A 的数组也是 B 的数组，并且完全可以在需要 B[] 的地方使用 A[]: 

Integer[] intArray = new Integer[10];
  
Number[] numberArray = intArray;

上面的代码是有效的，因为一个 Integer 是 一个 Number，因而一个 Integer 数组是 一个 Number 数组。但是对于泛型来说则不然。下面的代码是无效的: 

ListintList = new ArrayList();
  
List numberList = intList; // invalid

最初，大多数 Java 程序员觉得这缺少协变很烦人，或者甚至是"坏的 (broken) "，但是之所以这样有一个很好的原因。如果可以将 List赋给 List，下面的代码就会违背泛型应该提供的类型安全: 

ListintList = new ArrayList();
  
List numberList = intList; // invalid
  
numberList.add(new Float(3.1415));

因为 intList 和 numberList 都是有别名的，如果允许的话，上面的代码就会让您将不是 Integers 的东西放进 intList 中。但是，正如下一屏将会看到的，您有一个更加灵活的方式来定义泛型。

类型通配符

假设您具有该方法: 

void printList(List l) {
  
for (Object o : l)
  
System.out.println(o);
  
}

上面的代码在 JDK 5.0 上编译通过，但是如果试图用 List调用它，则会得到警告。出现警告是因为，您将泛型 (List) 传递给一个只承诺将它当作 List (所谓的原始类型) 的方法，这将破坏使用泛型的类型安全。

如果试图编写像下面这样的方法，那么将会怎么样？void printList(List

它仍然不会通过编译，因为一个 List不是 一个 List

解决方案是使用类型通配符: 

void printList(Listl) {
  
for (Object o : l)
  
System.out.println(o);
  
}

上面代码中的问号是一个类型通配符。它读作"问号"。List是任何泛型 List 的父类型，

类型通配符的作用

前一屏 类型通配符 中引入了类型通配符，这让您可以声明 List类型的变量。您可以对这样的 List 做什么呢？非常方便，可以从中检索元素，但是不能添加元素。原因不是编译器知道哪些方法修改列表哪些方法不修改列表，而是 (大多数) 变化的方法比不变化的方法需要更多的类型信息。下面的代码则工作得很好: 

Listli = new ArrayList();
  
li.add(new Integer(42));
  
List lu = li;
  
System.out.println(lu.get(0));

为什么该代码能工作呢？对于 lu，编译器一点都不知道 List 的类型参数的值。但是编译器比较聪明，它可以做一些类型推理。在本例中，它推断未知的类型参数必须扩展 Object。 (这个特定的推理没有太大的跳跃，但是编译器可以作出一些非常令人佩服的类型推理，后面就会看到 (在 底层细节 一节中) 。所以它让您调用 List.get() 并推断返回类型为 Object。

另一方面，下面的代码不能工作: 

Listli = new ArrayList();
  
li.add(new Integer(42));
  
List lu = li;
  
lu.add(new Integer(43)); // error

在本例中，对于 lu，编译器不能对 List 的类型参数作出足够严密的推理，以确定将 Integer 传递给 List.add() 是类型安全的。所以编译器将不允许您这么做。

以免您仍然认为编译器知道哪些方法更改列表的内容哪些不更改列表内容，请注意下面的代码将能工作，因为它不依赖于编译器必须知道关于 lu 的类型参数的任何信息: 

Listli = new ArrayList();
  
li.add(new Integer(42));
  
List lu = li;
  
lu.clear();

泛型方法

 (在 类型参数 一节中) 您已经看到，通过在类的定义中添加一个形式类型参数列表，可以将类泛型化。方法也可以被泛型化，不管它们定义在其中的类是不是泛型化的。

泛型类在多个方法签名间实施类型约束。在 List中，类型参数 V 出现在 get()、add()、contains() 等方法的签名中。当创建一个 Map类型的变量时，您就在方法之间宣称一个类型约束。您传递给 add() 的值将与 get() 返回的值的类型相同。

类似地，之所以声明泛型方法，一般是因为您想要在该方法的多个参数之间宣称一个类型约束。例如，下面代码中的 ifThenElse() 方法，根据它的第一个参数的布尔值，它将返回第二个或第三个参数: 

public T ifThenElse(boolean b, T first, T second) {
  
return b ? first : second;
  
}

注意，您可以调用 ifThenElse()，而不用显式地告诉编译器，您想要 T 的什么值。编译器不必显式地被告知 T 将具有什么值；它只知道这些值都必须相同。编译器允许您调用下面的代码，因为编译器可以使用类型推理来推断出，替代 T 的 String 满足所有的类型约束: 

String s = ifThenElse(b, "a", "b");

类似地，您可以调用: 

Integer i = ifThenElse(b, new Integer(1), new Integer(2));

但是，编译器不允许下面的代码，因为没有类型会满足所需的类型约束: 

String s = ifThenElse(b, "pi", new Float(3.14));

为什么您选择使用泛型方法，而不是将类型 T 添加到类定义呢？ (至少) 有两种情况应该这样做: 

当泛型方法是静态的时，这种情况下不能使用类类型参数。

当 T 上的类型约束对于方法真正是局部的时，这意味着没有在相同类的另一个 方法签名中使用相同 类型 T 的约束。通过使得泛型方法的类型参数对于方法是局部的，可以简化封闭类型的签名。

有限制类型

在前一屏 泛型方法 的例子中，类型参数 V 是无约束的或无限制的 类型。有时在还没有完全指定类型参数时，需要对类型参数指定附加的约束。

考虑例子 Matrix 类，它使用类型参数 V，该参数由 Number 类来限制: 

public class Matrix{ ... }

编译器允许您创建 Matrix或 Matrix类型的变量，但是如果您试图定义 Matrix类型的变量，则会出现错误。类型参数 V 被判断为由 Number 限制 。在没有类型限制时，假设类型参数由 Object 限制。这就是为什么前一屏 泛型方法 中的例子，允许 List.get() 在 List上调用时返回 Object，即使编译器不知道类型参数 V 的类型。

三 一个简单的泛型类

编写基本的容器类

此时，您可以开始编写简单的泛型类了。到目前为止，泛型类最常见的用例是容器类 (比如集合框架) 或者值持有者类 (比如 WeakReference 或 ThreadLocal) 。我们来编写一个类，它类似于 List，充当一个容器。其中，我们使用泛型来表示这样一个约束，即 Lhist 的所有元素将具有相同类型。为了实现起来简单，Lhist 使用一个固定大小的数组来保存值，并且不接受 null 值。

Lhist 类将具有一个类型参数 V (该参数是 Lhist 中的值的类型) ，并将具有以下方法: 

public class Lhist{
  
public Lhist(int capacity) { ... }
  
public int size() { ... }
  
public void add(V value) { ... }
  
public void remove(V value) { ... }
  
public V get(int index) { ... }
  
}

要实例化 Lhist，只要在声明时指定类型参数和想要的容量: 

LhiststringList = new Lhist(10);

实现构造函数

在实现 Lhist 类时，您将会遇到的第一个拦路石是实现构造函数。您可能会像下面这样实现它: 

public class Lhist{
  
private V[] array;
  
public Lhist(int capacity) {
  
array = new V[capacity]; // illegal
  
}
  
}

这似乎是分配后备数组最自然的一种方式，但是不幸的是，您不能这样做。具体原因很复杂，当学习到 底层细节 一节中的"擦除"主题时，您就会明白。分配后备数组的实现方式很古怪且违反直觉。下面是构造函数的一种可能的实现 (该实现使用集合类所采用的方法) : 

public class Lhist{
  
private V[] array;
  
public Lhist(int capacity) {
  
array = (V[]) new Object[capacity];
  
}
  
}

另外，也可以使用反射来实例化数组。但是这样做需要给构造函数传递一个附加的参数 —— 一个类常量，比如 Foo.class。后面在 Class一节中将讨论类常量。

实现方法

实现 Lhist 的方法要容易得多。下面是 Lhist 类的完整实现: 

public class Lhist{
  
private V[] array;
  
private int size;

public Lhist(int capacity) {
  
array = (V[]) new Object[capacity];
  
}

public void add(V value) {
  
if (size == array.length)
  
throw new IndexOutOfBoundsException(Integer.toString(size));
  
else if (value == null)
  
throw new NullPointerException();
  
array[size++] = value;
  
}

public void remove(V value) {
  
int removalCount = 0;
  
for (int i=0; i if (array[i].equals(value))
  
++removalCount;
  
else if (removalCount > 0) {
  
array[i-removalCount] = array[i];
  
array[i] = null;
  
}
  
}
  
size -= removalCount;
  
}

public int size() { return size; }

public V get(int i) {
  
if (i >= size)
  
throw new IndexOutOfBoundsException(Integer.toString(i));
  
return array[i];
  
}
  
}

注意，您在将会接受或返回 V 的方法中使用了形式类型参数 V，但是您一点也不知道 V 具有什么样的方法或域，因为这些对泛型代码是不可知的。

使用 Lhist 类

使用 Lhist 类很容易。要定义一个整数 Lhist，只需要在声明和构造函数中为类型参数提供一个实际值即可: 

Lhistli = new Lhist(30);

编译器知道，li.get() 返回的任何值都将是 Integer 类型，并且它还强制传递给 li.add() 或 li.remove() 的任何东西都是 Integer。除了实现构造函数的方式很古怪之外，您不需要做任何十分特殊的事情以使 Lhist 是一个泛型类。

四 Java类库中的泛型

集合类

到目前为止，Java 类库中泛型支持存在最多的地方就是集合框架。就像容器类是 C++ 语言中模板的主要动机一样 (参阅 附录 A: 与 C++ 模板的比较)  (尽管它们随后用于很多别的用途) ，改善集合类的类型安全是 Java 语言中泛型的主要动机。集合类也充当如何使用泛型的模型，因为它们演示了泛型的几乎所有的标准技巧和方言。

所有的标准集合接口都是泛型化的 —— Collection、List、Set和 Map。类似地，集合接口的实现都是用相同类型参数泛型化的，所以 HashMap实现 Map等。

集合类也使用泛型的许多"技巧"和方言，比如上限通配符和下限通配符。例如，在接口 Collection中，addAll 方法是像下面这样定义的: 

interface Collection{
  
boolean addAll(Collection);
  
}

该定义组合了通配符类型参数和有限制类型参数，允许您将 Collection的内容添加到 Collection。

如果类库将 addAll() 定义为接受 Collection，您就不能将 Collection的内容添加到 Collection。不是限制 addAll() 的参数是一个与您将要添加到的集合包含相同类型的集合，而有可能建立一个更合理的约束，即传递给 addAll() 的集合的元素 适合于添加到您的集合。有限制类型允许您这样做，并且使用有限制通配符使您不需要使用另一个不会用在其他任何地方的占位符名称。

应该可以将 addAll() 的类型参数定义为 Collection。但是，这不但没什么用，而且还会改变 Collection 接口的语义，因为泛型版本的语义将会不同于非泛型版本的语义。这阐述了泛型化一个现有的类要比定义一个新的泛型类难得多，因为您必须注意不要更改类的语义或者破坏现有的非泛型代码。

作为泛型化一个类 (如果不小心的话) 如何会更改其语义的一个更加微妙的例子，注意 Collection.removeAll() 的参数的类型是 Collection，而不是 Collection。这是因为传递混合类型的集合给 removeAll() 是可接受的，并且更加限制地定义 removeAll 将会更改方法的语义和有用性。

其他容器类

除了集合类之外，Java 类库中还有几个其他的类也充当值的容器。这些类包括 WeakReference、SoftReference 和 ThreadLocal。它们都已经在其包含的值的类型上泛型化了，所以 WeakReference是对 T 类型的对象的弱引用，ThreadLocal则是到 T 类型的线程局部变量的句柄。

泛型不止用于容器

泛型最常见最直观的使用是容器类，比如集合类或引用类 (比如 WeakReference) 。Collection中类型参数的含义很明显 —— "一个所有值都是 V 类型的集合"。类似地，ThreadLocal也有一个明显的解释 —— "一个其类型是 T 的线程局部变量"。但是，泛型规格说明中没有指定容积。

像 Comparable或 Class这样的类中类型参数的含义更加微妙。有时，就像 Class中一样，类型变量主要是帮助编译器进行类型推理。有时，就像隐含的 Enum> 中一样，类型变量只是在类层次结构上加一个约束。

Comparable

Comparable 接口已经泛型化了，所以实现 Comparable 的对象声明它可以与什么类型进行比较。 (通常，这是对象本身的类型，但是有时也可能是父类。) 

public interface Comparable{
  
public boolean compareTo(T other);
  
}

所以 Comparable 接口包含一个类型参数 T，该参数是一个实现 Comparable 的类可以与之比较的对象的类型。这意味着如果定义一个实现 Comparable 的类，比如 String，就必须不仅声明类支持比较，还要声明它可与什么比较 (通常是与它本身比较) : 

public class String implements Comparable{ ... }

现在来考虑一个二元 max() 方法的实现。您想要接受两个相同类型的参数，二者都是 Comparable，并且相互之间是 Comparable。幸运的是，如果使用泛型方法和有限制类型参数的话，这相当直观: 

public static > T max(T t1, T t2) {
  
if (t1.compareTo(t2) > 0)
  
return t1;
  
else
  
return t2;
  
}

在本例中，您定义了一个泛型方法，在类型 T 上泛型化，您约束该类型扩展 (实现)  Comparable。两个参数都必须是 T 类型，这表示它们是相同类型，支持比较，并且相互可比较。容易！

更好的是，编译器将使用类型推理来确定当调用 max() 时 T 的值表示什么意思。所以根本不用指定 T，下面的调用就能工作: 

String s = max("moo", "bark");

编译器将计算出 T 的预定值是 String，因此它将进行编译和类型检查。但是如果您试图用不实现 Comparable的 类 X 的参数调用 max()，那么编译器将不允许这样做。

Class

类 Class 已经泛型化了，但是很多人一开始都感觉其泛型化的方式很混乱。Class中类型参数 T 的含义是什么？事实证明它是所引用的类接口。怎么会是这样的呢？那是一个循环推理？如果不是的话，为什么这样定义它？

在以前的 JDK 中，Class.newInstance() 方法的定义返回 Object，您很可能要将该返回类型强制转换为另一种类型: 

class Class {
  
Object newInstance();
  
}

但是使用泛型，您定义 Class.newInstance() 方法具有一个更加特定的返回类型: 

class Class{
  
T newInstance();
  
}

如何创建一个 Class类型的实例？就像使用非泛型代码一样，有两种方式: 调用方法 Class.forName() 或者使用类常量 X.class。Class.forName() 被定义为返回 Class。另一方面，类常量 X.class 被定义为具有类型 Class，所以 String.class 是 Class类型的。

让 Foo.class 是 Class类型的有什么好处？大的好处是，通过类型推理的魔力，可以提高使用反射的代码的类型安全。另外，还不需要将 Foo.class.newInstance() 强制类型转换为 Foo。

考虑一个方法，它从数据库检索一组对象，并返回 JavaBeans 对象的一个集合。您通过反射来实例化和初始化创建的对象，但是这并不意味着类型安全必须完全被抛至脑后。考虑下面这个方法: 

public staticListgetRecords(Classc, Selector s) {
  
// Use Selector to select rows
  
List list = new ArrayList();
  
for (/* iterate over results */) {
  
T row = c.newInstance();
  
// use reflection to set fields from result
  
list.add(row);
  
}
  
return list;
  
}

可以像下面这样简单地调用该方法: 

Listl = getRecords(FooRecord.class, fooSelector);

编译器将会根据 FooRecord.class 是 Class类型的这一事实，推断 getRecords() 的返回类型。您使用类常量来构造新的实例并提供编译器在类型检查中要用到的类型信息。

用 Class替换 T[]

Collection 接口包含一个方法，用于将集合的内容复制到一个调用者指定类型的数组中: 

public Object[] toArray(Object[] prototypeArray) { ... }

toArray(Object[]) 的语义是，如果传递的数组足够大，就会使用它来保存结果，否则，就会使用反射分配一个相同类型的新数组。一般来说，单独传递一个数组作为参数来提供想要的返回类型是一个小技巧，但是在引入泛型之前，这是与方法交流类型信息最方便的方式。

有了泛型，就可以用一种更加直观的方式来做这件事。不像上面这样定义 toArray()，泛型 toArray() 可能看起来像下面这样: 

publicT[] toArray(ClassreturnType)

调用这样一个 toArray() 方法很简单: 

FooBar[] fba = something.toArray(FooBar.class);

Collection 接口还没有改变为使用该技术，因为这会破坏许多现有的集合实现。但是如果使用泛型从新构建 Collection，则当然会使用该方言来指定它想要返回值是哪种类型。

Enum

JDK 5.0 中 Java 语言另一个增加的特性是枚举。当您使用 enum 关键字声明一个枚举时，编译器就会在内部为您生成一个类，用于扩展 Enum 并为枚举的每个值声明静态实例。所以如果您说: 

public enum Suit {HEART, DIAMOND, CLUB, SPADE};

编译器就会在内部生成一个叫做 Suit 的类，该类扩展 java.lang.Enum并具有叫做 HEART、DIAMOND、CLUB 和 SPADE 的常量 (public static final) 成员，每个成员都是 Suit 类。

与 Class 一样，Enum 也是一个泛型类。但是与 Class 不同，它的签名稍微更复杂一些: 

class Enum> { . . . }

这究竟是什么意思？这难道不会导致无限递归？

我们逐步来分析。类型参数 E 用于 Enum 的各种方法中，比如 compareTo() 或 getDeclaringClass()。为了这些方法的类型安全，Enum 类必须在枚举的类上泛型化。

所以 extends Enum部分如何理解？该部分又具有两个部分。第一部分指出，作为 Enum 的类型参数的类本身必须是 Enum 的子类型，所以您不能声明一个类 X 扩展 Enum。第二部分指出，任何扩展 Enum 的类必须传递它本身 作为类型参数。您不能声明 X 扩展 Enum，即使 Y 扩展 Enum。

总之，Enum 是一个参数化的类型，只可以为它的子类型实例化，并且这些子类型然后将根据子类型来继承方法。幸运的是，在 Enum 情况下，编译器为您做这些工作，一切都很好。

与非泛型代码相互操作

数百万行现有代码使用已经泛型化的 Java 类库中的类，比如集合框架、Class 和 ThreadLocal。JDK 5.0 中的改进不要破坏所有这些代码是很重要的，所以编译器允许您在不指定其类型参数的情况下使用泛型类。

当然，以"旧方式"做事没有新方式安全，因为忽略了编译器准备提供的类型安全。如果您试图将 List传递给一个接受 List 的方法，它将能够工作，但是编译器将会发出一个可能丧失类型安全的警告，即所谓的"unchecked conversion (不检查转换) "警告。

没有类型参数的泛型，比如声明为 List 类型而不是 List类型的变量，叫做原始类型。原始类型与参数化类型的任何实例化是赋值兼容的，但是这样的赋值会生成 unchecked-conversion 警告。

为了消除一些 unchecked-conversion 警告，假设您不准备泛型化所有的代码，您可以使用通配符类型参数。使用 List而不使用 List。List 是原始类型；List是具有未知类型参数的泛型。编译器将以不同的方式对待它们，并很可能发出更少的警告。

无论在哪种情况下，编译器在生成字节码时都会生成强制类型转换，所以生成的字节码在每种情况下都不会比没有泛型时更不安全。如果您设法通过使用原始类型或类文件来破坏类型安全，就会得到与不使用泛型时得到的相同的 ClassCastException 或 ArrayStoreException。

已检查集合

作为从原始集合类型迁移到泛型集合类型的帮助，集合框架添加了一些新的集合包装器，以便为一些类型安全 bug 提供早期警告。就像 Collections.unmodifiableSet() 工厂方法用一个不允许任何修改的 Set 包装一个现有 Set 一样，Collections.checkedSet() (以及 checkedList() 和 checkedMap()) 工厂方法创建一个包装器 (或者视图) 类，以防止您将错误类型的变量放在集合中。

checkedXxx() 方法都接受一个类常量作为参数，所以它们可以 (在运行时) 检查这些修改是允许的。典型的实现可能像下面这样: 

public class Collections {
  
public static Collection checkedCollection(Collection c, Class type ) {
  
return new CheckedCollection(c, type);
  
}

private static class CheckedCollectionimplements Collection{
  
private final Collection c;
  
private final Class type;

CheckedCollection(Collectionc, Classtype) {
  
this.c = c;
  
this.type = type;
  
}

public boolean add(E o) {
  
if (!type.isInstance(o))
  
throw new ClassCastException();
  
else
  
return c.add(o);
  
}
  
}
  
}

五 底层细节

擦除

也许泛型最具挑战性的方面是擦除 (erasure) ，这是 Java 语言中泛型实现的底层技术。擦除意味着编译器在生成类文件时基本上会抛开参数化类的大量类型信息。编译器用它的强制类型转换生成代码，就像程序员在泛型出现之前手工所做的一样。区别在于，编译器开始已经验证了大量如果没有泛型就不会验证的类型安全约束。

通过擦除实现泛型的含意是很重要的，并且初看也是混乱的。尽管不能将 List赋给 List，因为它们是不同的类型，但是 List和 List类型的变量是相同的类！要明白这一点，请评价下面的代码: 

new List().getClass() == new List().getClass()

编译器只为 List 生成一个类。当生成了 List 的字节码时，将很少剩下其类型参数的的跟踪。

当生成泛型类的字节码时，编译器用类型参数的擦除 替换类型参数。对于无限制类型参数 () ，它的擦除是 Object。对于上限类型参数 (>) ，它的擦除是其上限 (在本例中是 Comparable) 的擦除。对于具有多个限制的类型参数，使用其最左限制的擦除。

如果检查生成的字节码，您无法说出 List和 List的代码之间的区别。类型限制 T 在字节码中被 T 的上限所取代，该上限一般是 Object。

多重限制

一个类型参数可以具有多个限制。当您想要约束一个类型参数比如说同时为 Comparable 和 Serializable 时，这将很有用。多重限制的语法是用"与"符号分隔限制: 

class C& Serializable>

通配符类型可以具有单个限制 —— 上限或者下限。一个指定的类型参数可以具有一个或多个上限。具有多重限制的类型参数可以用于访问它的每个限制的方法和域。

类型形参和类型实参

在参数化类的定义中，占位符名称 (比如 Collection中的 V) 叫做类型形参 (type parameter) ，它们类似于方法定义中的形式参数。在参数化类的变量的声明中，声明中指定的类型值叫做类型实参 (type argument) ，它们类似于方法调用中的实际参数。但是实际中二者一般都通称为"类型参数"。所以给出定义: 

interface Collection{ ... }

和声明: 

Collectioncs = new HashSet();

那么，名称 V (它可用于整个 Collection 接口体内) 叫做一个类型形参。在 cs 的声明中，String 的两次使用都是类型实参 (一次用于 Collection，另一次用于 HashSet) 。

关于何时可以使用类型形参，存在一些限制。大多数时候，可以在能够使用实际类型定义的任何地方使用类型形参。但是有例外情况。不能使用它们创建对象或数组，并且不能将它们用于静态上下文中或者处理异常的上下文中。还不能将它们用作父类型 (class Fooextends T) ，不能用于 instanceof 表达式中，不能用作类常量。

类似地，关于可以使用哪些类型作为类型实参，也存在一些限制。类型实参必须是引用类型 (不是基本类型) 、通配符、类型参数，或者其他参数化类型的实例化。所以您可以定义 List (引用类型) 、List (通配符) 或者 List> (其他参数化类型的实例化) 。在带有类型形参 T 的参数化类型的定义中，您也可以声明 List (类型形参) 。

六 结束语

泛型的引入是对 Java 语言和 Java 类库的一个主要改变。泛型可以提高 Java 应用程序的类型安全、可维护性和可靠性，代价是一些附加的复杂性。

已经做了非常小心的处理，以确保现有的类将继续与 JDK 5.0 中的泛型化类库一起工作，所以您可以根据自己的意愿选择从什么时候开始使用泛型。

Author: orangelizq
email: orangelizq@163.com

https://my.oschina.net/polly/blog/877647
