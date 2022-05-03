---
title: Lambda 表达式
author: "-"
date: 2012-11-17T07:17:38+00:00
url: lambda
categories:
  - Development

tags:
  - reprint
---
## Lambda 表达式

# Lambda

"Lambda 表达式"是一个匿名函数,它可以包含表达式和语句,并且可用于创建委托或表达式目录树类型。 所有 Lambda 表达式都使用 Lambda 运算符 =>,该运算符读为"goes to"。该 Lambda 运算符的左边是输入参数 (如果有) ,右边包含表达式或语句块。Lambda 表达式 x => x * x 读作"x goes to x times x"。

### 函数式接口functional interface, @FunctionalInterface

函数式接口(Functional Interface)是Java 8对一类特殊类型的接口的称呼。 这类接口只定义了唯一的抽象方法的接口 (除了隐含的Object对象的公共方法) , 因此最开始也就做SAM类型的接口 (Single Abstract Method) 。

为什么会单单从接口中定义出此类接口呢？ 原因是在 Java Lambda 的实现中, 开发组不想再为Lambda表达式单独定义一种特殊的Structural函数类型,称之为箭头类型 (arrow type) , 依然想采用Java既有的类型系统(class, interface, method等), 原因是增加一个结构化的函数类型会增加函数类型的复杂性,破坏既有的Java类型,并对成千上万的Java类库造成严重的影响。 权衡利弊, 因此最终还是利用SAM 接口作为 Lambda表达式的目标类型。

JDK中已有的一些接口本身就是函数式接口,如Runnable。 JDK 8中又增加了java.util.function包, 提供了常用的函数式接口。

函数式接口代表的一种契约, 一种对某个特定函数类型的契约。 在它出现的地方,实际期望一个符合契约要求的函数。 Lambda表达式不能脱离上下文而存在,它必须要有一个明确的目标类型,而这个目标类型就是某个函数式接口。

### 方法引用 (method reference)

双冒号 "::" 是 Java 8 引入 Lambda 表达式后的一种用法,表示方法引用 (method reference) ,可以更加简洁的实例化接口
双冒号表达式返回的是一个 函数式接口对象  (用 @FunctionalInterface 注解的 interface 类型) 的实例,如下:

```java
@Test
public void test0() {
    List<Integer> list = Arrays.asList(1, 2, 3);

    Consumer<Integer> consumer = System.out::println;
    list.forEach(consumer);
}

// java.util.function.Consumer
@FunctionalInterface
public interface Consumer<T> {
    void accept(T t);
}
```

### 方法引用 Method Reference

双冒号 (::) 运算符在 Java 8 中被用作方法引用 (method reference) ,方法引用是与 lambda 表达式相关的一个重要特性。
它提供了一种不执行方法的方法: 双冒号的方式只是指明方法引用,具体执行还是传统的方式。
方法引用需要兼容函数式接口组成的目标类型上下文: 也就是说被引用的方法的参数和 函数式接口 的参数类型必须一致。
具体使用方式有以下几种

### 静态方法引用(Reference to a static method)

语法: ContainingClass::staticMethodName
例如: Person::getAge

### 对象的实例方法引用(Reference to an instance method of a particular object)

语法: containingObject::instanceMethodName
例如: System.out::println

### 特定类型的任意对象实例的方法(Reference to an instance method of an arbitrary object of a particular type)

语法: (ContainingType::methodName)
例如: String::compareToIgnoreCase

### 类构造器引用语法 (Reference to a constructor)

语法: ClassName::new
例如: ArrayList::new

简单地说,就是一个 Lambda 表达式。在 Java 8 中,我们会使用 Lambda 表达式创建匿名方法,但是有时候,我们的 Lambda 表达式可能仅仅调用一个已存在的方法,而不做任何其它事,对于这种情况,通过一个方法名字来引用这个已存在的方法会更加清晰,Java 8 的方法引用允许我们这样做。方法引用是一个更加紧凑,易读的 Lambda 表达式,注意方法引用是一个 Lambda 表达式,其中方法引用的操作符是双冒号 "::"。

### 方法引用例子

首先定义一个 Person 类,如下:

```java
public class Person { 
    String name;
    LocalDate birthday; 

    public Person(String name, LocalDate birthday) { 
        this.name = name; 
        this.birthday = birthday;
    }

    public LocalDate getBirthday() { 
        return birthday;
    } 

    public static int compareByAge(Person a, Person b) { 
        return a.birthday.compareTo(b.birthday);
    }

    @Override 
    public String toString() { 
        return this.name;
    }
}
```

假设我们有一个 Person 数组,并且想对它进行排序,这时候,我们可能会这样写:

### 原始写法

```java
public class Main { 
    static class PersonAgeComparator implements Comparator<Person> { 
        public int compare(Person a, Person b) { 
            return a.getBirthday().compareTo(b.getBirthday());
        }
    } 

    public static void main(String[] args) {
        Person[] pArr = new Person[]{ 
            new Person("003", LocalDate.of(2016, 9, 1)), 
            new Person("001", LocalDate.of(2016, 2, 1)), 
            new Person("002", LocalDate.of(2016, 3, 1)), 
            new Person("004", LocalDate.of(2016, 12, 1))};

        Arrays.sort(pArr, new PersonAgeComparator());

        System.out.println(Arrays.asList(pArr));
    }
}
```

其中,Arrays类的sort方法定义如下:

```java
public static <T> void sort(T[] a, Comparator<? super T> c)
//...
@FunctionalInterface
public interface Comparator<T> {
    int compare(T o1, T o2);
    boolean equals(Object obj);
    //...
}
```

Comparator接口是一个函数式接口,因此可以使用 Lambda 表达式,而不需要定义一个实现 Comparator 接口的类,并创建它的实例对象,传给 sort 方法。

使用 Lambda 表达式,我们可以这样写:

### 改进一,使用 Lambda 表达式, 未调用已存在的方法

```java
public class Main { 
    public static void main(String[] args) {
        Person[] pArr = new Person[]{ 
            new Person("003", LocalDate.of(2016, 9, 1)), 
            new Person("001", LocalDate.of(2016, 2, 1)), 
            new Person("002", LocalDate.of(2016, 3, 1)), 
            new Person("004", LocalDate.of(2016, 12, 1))};

        Arrays.sort(pArr, (Person a, Person b) -> { 
            return a.getBirthday().compareTo(b.getBirthday());
        });

        System.out.println(Arrays.asList(pArr));
    }
}
```

然而,在以上代码中,关于两个人生日的比较方法在 Person 类中已经定义了,因此,我们可以直接使用已存在的 Person.compareByAge 方法。

### 改进二,使用 Lambda 表达式,调用已存在的方法

```java
public class Main { 
    public static void main(String[] args) {
        Person[] pArr = new Person[]{ 
            new Person("003", LocalDate.of(2016, 9, 1)), 
            new Person("001", LocalDate.of(2016, 2, 1)), 
            new Person("002", LocalDate.of(2016, 3, 1)), 
            new Person("004", LocalDate.of(2016, 12, 1))};

        Arrays.sort(pArr, (a, b) -> Person.compareByAge(a, b));

        System.out.println(Arrays.asList(pArr));
    }
}
```

因为这个 Lambda 表达式调用了一个已存在的方法,因此,我们可以直接使用方法引用来替代这个 Lambda 表达式

### 改进三,使用方法引用

```java
public class Main { 
    public static void main(String[] args) {
        Person[] pArr = new Person[]{ 
            new Person("003", LocalDate.of(2016, 9, 1)), 
            new Person("001", LocalDate.of(2016, 2, 1)), 
            new Person("002", LocalDate.of(2016, 3, 1)), 
            new Person("004", LocalDate.of(2016, 12, 1))};

        Arrays.sort(pArr, Person::compareByAge);

        System.out.println(Arrays.asList(pArr));
    }
}
```

在以上代码中,方法引用 Person::compareByAge 在语义上与 Lambda 表达式 (a, b) -> Person.compareByAge(a, b) 是等同的

四种方法引用类型

### 静态方法引用

ContainingClass::staticMethodName
比较容易理解,和静态方法调用相比,只是把 . 换为 ::

例子:

String::valueOf,等价于 Lambda: s -> String.valueOf(s)
Math::pow 等价于lambda表达式 (x, y) -> Math.pow(x, y);
前面举的例子 Person::compareByAge 就是一个静态方法引用
从一个数字列表中找出最大的一个数字,方法引用方式:
Function, Integer> maxFn = Collections::max;
// 等价于 Lambda 表达式:
// Function, Integer> maxFn = (numbers) -> Collections.max(numbers);
maxFn.apply(Arrays.asList(1, 10, 3, 5))。
字符串反转
// 函数式接口  
interface StringFunc {  
    String func(String n);  
}  

class MyStringOps {  
    // 静态方法: 反转字符串  
    public static String strReverse(String str) {  
        String result = "";  
        for (int i = str.length() - 1; i >= 0; i--) {  
            result += str.charAt(i);  
        }  
        return result;  
    }  
}  

class MethodRefDemo {  
    public static String stringOp(StringFunc sf, String s) {  
        return sf.func(s);  
    }  
    public static void main(String[] args) {  
        String inStr = "lambda add power to Java";  
        // MyStringOps::strReverse 相当于实现了接口方法 func() ,并在接口方法 func() 中作了 MyStringOps.strReverse() 操作  
        String outStr = stringOp(MyStringOps::strReverse, inStr);  
        System.out.println("Original string: " + inStr);  
        System.out.println("String reserved: " + outStr);  
    }  
}  

### 引用特定对象的实例方法

实例上的实例方法引用

```java
instanceReference::instanceMethodName 
```

例子: x::toString,对应的 Lambda: () -> this.toString()
与引用静态方法相比,都换为实例对象而已

如下示例,引用的方法是 myComparisonProvider 对象的 compareByName 方法:

```java
class ComparisonProvider { 
    public int compareByName(Person a, Person b) { 
        return a.getName().compareTo(b.getName());
    } 

    public int compareByAge(Person a, Person b) { 
        return a.getBirthday().compareTo(b.getBirthday());
    }
}
```

```java
ComparisonProvider myComparisonProvider = new ComparisonProvider();
Arrays.sort(rosterAsArray, myComparisonProvider::compareByName);
```

超类上的实例方法引用
super::methodName
通过使用 super,可以引用方法的超类版本。除此以外,还可以捕获 this 指针

this::equals 等价于 Lambda 表达式 x -> this.equals(x)
引用特定类型的任意对象的实例方法  (较少用)
ClassName::methodName
若类型的实例方法是泛型的,就需要在::分隔符前提供类型参数,或者 (多数情况下) 利用目标类型推导出其类型。
静态方法引用和引用特定类型的任意对象的实例方法拥有一样的语法。编译器会根据实际情况做出决定。
一般我们不需要指定方法引用中的参数类型,因为编译器往往可以推导出结果,但如果需要我们也可以显式在::分隔符之前提供参数类型信息。

例子:

String::toString,对应的 Lambda: (s) -> s.toString()
这里不太容易理解,实例方法要通过对象来调用,方法引用对应 Lambda,Lambda 的第一个参数会成为调用实例方法的对象。
字符串数组中任意一个对象的 compareToIgnoreCase 方法:
String[] stringArray = { "Barbara", "James", "Mary" };
Arrays.sort(stringArray, String::compareToIgnoreCase);
在泛型类或泛型方法中,也可以使用方法引用
interface MyFunc<T> {  
    int func(T[] als, T v);  
}  
class MyArrayOps {  
    public static <T> int countMatching(T[] vals, T v) {  
        int count = 0;  
        for (int i = 0; i < vals.length; i++) {  
            if (vals[i] == v) count++;  
        }  
        return count;  
    }  
}  
class GenericMethodRefDemo {  
    public static <T> int myOp(MyFunc<T> f, T[] vals, T v) {  
        return f.func(vals, v);  
    }  
    public static void main(String[] args){  
        Integer[] vals = {1, 2, 3, 4, 2, 3, 4, 4, 5};  
        String[] strs = {"One", "Two", "Three", "Two"};  
        int count;  
        count = myOp(MyArrayOps::<Integer>countMatching, vals, 4);  
        System.out.println("vals contains " + count + " 4s");  
        count = myOp(MyArrayOps::<String>countMatching, strs, "Two");  
        System.out.println("strs contains " + count + " Twos");  
    }  
}  
当把泛型方法指定为方法引用时,类型参数出现在 :: 之后、方法名之前。在这种情况下,并非必须显示指定类型参数,因为类型参数会被自动推断得出。对于指定泛型类的情况,类型参数位于类名的后面::的前面。

构造方法引用
构造方法引用又分构造方法引用和数组构造方法引用

构造方法引用  (也可以称作构造器引用)
ClassName::new
构造函数本质上是静态方法,只是方法名字比较特殊,使用前提是该类必须有无参构造函数

例子:

String::new,对应的 Lambda: () -> new String()
Supplier
class PersonFactory {
    private Supplier<Person> supplier;

    public PersonFactory(Supplier<Person> supplier) {
        this.supplier = supplier;
    }

    public Person getPerson() {
        return supplier.get();
    }
}

PersonFactory factory = new PersonFactory(Person::new);
Person p1 = factory.getPerson();
Stream
List<String> strings = new ArrayList<String>();  
strings.add("a");  
strings.add("b");  
Stream<Button> stream = strings.stream().map(Button::new);  
List<Button> buttons = stream.collect(Collectors.toList());  
数组构造方法引用
TypeName[]::new
int[]::new 是一个含有一个参数的构造器引用,这个参数就是数组的长度。等价于 lambda 表达式 x -> new int[x]

IntFunction<int[]> arrayMaker = int[]::new;
int[] array = arrayMaker.apply(10)     // 创建数组 int[10]
引用特定对象的实例方法 与 引用特定类型的任意对象的实例方法 的区别
class Person {
    private String name;     // 省略 getter、setter

    public int compare(Person p1, Person p2) {
        return p1.getName().compareTo(p2.getName());
    }

    public int compareTo(Person p) {
        return this.getName().compareTo(p.getName());
    }
}

// 用特定对象的实例方法
Arrays.sort(persons, p1::compare);

// 引用特定类型的任意对象的实例方法
Arrays.sort(persons, Person::compareTo);
// 相当于 (p1, p2) -> p1.compareTo(p2)
什么场景适合使用方法引用
当一个 Lambda 表达式调用了一个已存在的方法

什么场景不适合使用方法引用
需要往引用的方法传参数的时候不适合:

IsReferable demo = () -> ReferenceDemo.commonMethod("Argument in method.");

作者: 杰哥长得帅
链接: <https://www.jianshu.com/p/4a3da6a11b58>
来源: 简书
著作权归作者所有。商业转载请联系作者获得授权,非商业转载请注明出处。

---

<https://colobu.com/2014/10/28/secrets-of-java-8-functional-interface/>

<http://ckjava.com/2019/05/14/understand-Java-8-method-reference/>  
<https://liujiacai.net/blog/2014/10/12/lambda-calculus-introduction/>
<https://www.jianshu.com/p/4a3da6a11b58>  
