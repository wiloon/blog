---
title: Java 8 函数式接口 functional interface
author: "-"
date: 2014-12-24T02:39:51+00:00
url: /?p=7127
categories:
  - Uncategorized

tags:
  - reprint
---
## Java 8 函数式接口 functional interface

http://colobu.com/2014/10/28/secrets-of-java-8-functional-interface/

@FunctionalInterface
  
函数式接口(Functional Interface)是Java 8对一类特殊类型的接口的称呼。 这类接口只定义了唯一的抽象方法的接口 (除了隐含的Object对象的公共方法) , 因此最开始也就做SAM类型的接口 (Single Abstract Method) 。

为什么会单单从接口中定义出此类接口呢？ 原因是在Java Lambda的实现中, 开发组不想再为Lambda表达式单独定义一种特殊的Structural函数类型,称之为箭头类型 (arrow type) , 依然想采用Java既有的类型系统(class, interface, method等), 原因是增加一个结构化的函数类型会增加函数类型的复杂性,破坏既有的Java类型,并对成千上万的Java类库造成严重的影响。 权衡利弊, 因此最终还是利用SAM 接口作为 Lambda表达式的目标类型。

JDK中已有的一些接口本身就是函数式接口,如Runnable。 JDK 8中又增加了java.util.function包, 提供了常用的函数式接口。

函数式接口代表的一种契约, 一种对某个特定函数类型的契约。 在它出现的地方,实际期望一个符合契约要求的函数。 Lambda表达式不能脱离上下文而存在,它必须要有一个明确的目标类型,而这个目标类型就是某个函数式接口。

当然, Java 8发布快一年了, 你对以上的概念也应该有所了解了,这篇文章也不会介绍这些基础的东西, 而是想深入的探讨函数式接口的定义和应用。

JDK 8之前已有的函数式接口

java.lang.Runnable
  
java.util.concurrent.Callable
  
java.security.PrivilegedAction
  
java.util.Comparator
  
java.io.FileFilter
  
java.nio.file.PathMatcher
  
java.lang.reflect.InvocationHandler
  
java.beans.PropertyChangeListener
  
java.awt.event.ActionListener
  
javax.swing.event.ChangeListener
  
新定义的函数式接口

java.util.function中定义了几组类型的函数式接口以及针对基本数据类型的子接口。

Predicate - 传入一个参数,返回一个bool结果, 方法为boolean test(T t)
  
Consumer - 传入一个参数,无返回值,纯消费。 方法为void accept(T t)
  
Function - 传入一个参数,返回一个结果,方法为R apply(T t)
  
Supplier - 无参数传入,返回一个结果,方法为T get()
  
UnaryOperator - 一元操作符, 继承Function,传入参数的类型和返回类型相同。
  
BinaryOperator - 二元操作符, 传入的两个参数的类型和返回类型相同, 继承BiFunction
  
Java API对函数式接口都已经标明了, 如

java.lang
  
Interface Runnable
      
All Known Subinterfaces:
          
RunnableFuture<V>, RunnableScheduledFuture<V>
      
All Known Implementing Classes:
          
AsyncBoxView.ChildState, ForkJoinWorkerThread, FutureTask, RenderableImageProducer, SwingWorker, Thread, TimerTask
      
Functional Interface:
          
This is a functional interface and can therefore be used as the assignment target for a lambda expression or method reference.
  
函数式接口中可以额外定义多个抽象方法,但这些抽象方法签名必须和Object的public方法一样

接口最终有确定的类实现, 而类的最终父类是Object。 因此函数式接口可以定义Object的public方法。
  
如以下的接口依然是函数式接口: 

@FunctionalInterface
  
public interface ObjectMethodFunctionalInterface {
      
void count(int i);

    String toString(); //same to Object.toString
    int hashCode(); //same to Object.hashCode
    boolean equals(Object obj); //same to Object.equals
    

}
  
为什么限定public类型的方法呢？因为接口中定义的方法都是public类型的。 举个例子,下面的接口就不是函数式接口: 

interface WrongObjectMethodFunctionalInterface {
      
void count(int i);

    Object clone(); //Object.clone is protected
    

}
  
因为Object.clone方法是protected类型。

声明异常

函数式接口的抽象方法可以声明 可检查异常(checked exception)。 在调用目标对象的这个方法时必须catch这个异常。

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
  
@FunctionalInterface
  
interface InterfaceWithException {
      
void apply(int i) throws Exception;
  
}
  
这和以前的接口/方法调用一样。

但是,如果在Lambda表达式中抛出异常, 而目标接口中的抽象函数没有声明这个可检查, 则此接口不能作为此lambda表达式的目标类型。

public class FunctionalInterfaceWithException {
      
public static void main(String[] args) {
          
InterfaceWithException target = i -> {throw new Exception();};
      
}
  
}
  
@FunctionalInterface
  
interface InterfaceWithException {
      
void apply(int i);
  
}
  
上面的例子中不能编译, 因为lambda表达式要求的目标类型和InterfaceWithException不同。 InterfaceWithException的函数没有声明异常。

静态方法

函数式接口中除了那个抽象方法外还可以包含静态方法。
  
Java 8以前的规范中接口中不允许定义静态方法。 静态方法只能在类中定义。 Java 8中可以定义静态方法。

一个或者多个静态方法不会影响SAM接口成为函数式接口。
  
下面的例子中FunctionalInterfaceWithStaticMethod包含一个SAM: apply,还有一个静态方法sum。 它依然是函数式接口。

@FunctionalInterface
  
interface FunctionalInterfaceWithStaticMethod {
      
static int sum(int[] array) {
          
return Arrays.stream(array).reduce((a, b) -> a+b).getAsInt();
      
}

    void apply();
    

}
  
public class StaticMethodFunctionalInterface {
      
public static void main(String[] args) {
          
int sum = FunctionalInterfaceWithStaticMethod.sum(new int[]{1,2,3,4,5});

        FunctionalInterfaceWithStaticMethod f = () -> {};
    }
    

}
  
### 默认方法, Java 8 默认方法 default

Java 8中允许接口实现方法, 而不是简单的声明, 这些方法叫做默认方法,使用特殊的关键字default。
  
因为默认方法不是抽象方法,所以不影响我们判断一个接口是否是函数式接口。

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
  
InterfaceWithDefaultMethod仍然是一个函数式接口。

泛型及继承关系

接口可以继承接口。 如果父接口是一个函数接口, 那么子接口也可能是一个函数式接口。 判断标准依据下面的条件: 

对于接口I, 假定M是接口成员里的所有抽象方法的继承(包括继承于父接口的方法), 除去具有和Object的public的实例方法签名的方法, 那么我们可以依据下面的条件判断一个接口是否是函数式接口, 这样可以更精确的定义函数式接口。
  
如果存在一个一个方法m, 满足: 

m的签名 (subsignature) 是M中每一个方法签名的子签名 (signature) 
  
m的返回值类型是M中的每一个方法的返回值类型的替代类型 (return-type-substitutable) 
  
那么I就是一个函数式接口。
  
看几个例子。

1)

interface X { int m(Iterable<String> arg); }
  
interface Y { int m(Iterable<String> arg); }
  
interface Z extends X, Y {}
  
接口Z继承了X,Y接口的m方法,由于这两个方法的签名相同,返回值也一样,所以Z有唯一的一个抽象方法int m(Iterable<String> arg);,可以作为函数式接口。

2)

interface X { Iterable m(Iterable<String> arg); }
  
interface Y { Iterable<String> m(Iterable arg); }
  
interface Z extends X, Y {}
  
方法签名Y.m 既满足签名是X.m,并且返回值也满足return-type-substitutable。所以Z是函数式接口,函数类型为Iterable<String> m(Iterable arg)。

3)

interface X { int m(Iterable<String> arg); }
  
interface Y { int m(Iterable<Integer> arg); }
  
interface Z extends X, Y {}
  
编译出错, 没有一个方法的签名是所有方法的子签名: 

4)

interface X { int m(Iterable<String> arg, Class c); }
  
interface Y { int m(Iterable arg, Class<?> c); }
  
interface Z extends X, Y {}
  
Compiler error: No method has a subsignature of all abstract methods
  
编译出错, 没有一个方法的签名是所有方法的子签名

5)

interface X { long m(); }
  
interface Y { int m(); }
  
interface Z extends X, Y {}
  
Compiler error: no method is return type substitutable
  
编译出错, 返回值类型不同。

6)

interface Foo<T> { void m(T arg); }
  
interface Bar<T> { void m(T arg); }
  
interface FooBar<X, Y> extends Foo<X>, Bar<Y> {}
  
Compiler error: different signatures, same erasure
  
编译出错

7)

interface Foo { void m(String arg); }
  
interface Bar<T> { void m(T arg); }
  
interface FooBar<T> extends Foo, Bar<T> {}
  
不是一个函数式接口, 两个方法的类型参数不一样。

8)

interface X { void m() throws IOException; }
  
interface Y { void m() throws EOFException; }
  
interface Z { void m() throws ClassNotFoundException; }
  
interface XY extends X, Y {}
  
interface XYZ extends X, Y, Z {}
  
X.m,Y.m,Z.m方法签名相同,返回值类型都是void,只是异常列表不同。 EOFException是IOException的子类。
  
在这种情况下XY和XYZ都是函数式接口,但是函数类型不同。
  
// XY has function type ()->void throws EOFException
  
// XYZ has function type ()->void (throws nothing)

9)

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
  
// D has function type (List)->List throws EOFException, SQLTransientException
  
// E has function type (List)->List throws EOFException, SQLTransientException

10)

interface G1 {
    
<E extends Exception> Object m() throws E;
  
}
  
interface G2 {
    
<F extends Exception> String m() throws Exception;
  
}
  
interface G extends G1, G2 {}
  
// G has function type ()->String throws F

函数式接口的交集

1)

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
  
I和J方法的交集依然符合函数式接口的定义。 上述代码可以用JDK中的javac编译通过但是Eclipse报错,这是Eclipse的一个bug。

2)

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
  
上述代码Eclipse不会报错但是javac无法编译,javac认为 (I & J)不是一个函数式接口。 看起来javac工作正常, Eclipse处理这样的case还有问题。

@FunctionalInterface

Java 不会强制要求你使用@FunctionalInterface注解来标记你的接口是函数式接口, 然而,作为API作者, 你可能倾向使用@FunctionalInterface指明特定的接口为函数式接口, 这只是一个设计上的考虑, 可以让用户很明显的知道一个接口是函数式接口。

@FunctionalInterface
  
public interface SimpleFuncInterface {
      
public void doWork();
  
}
  
如果你在一个不是函数式的接口使用@FunctionalInterface标记的话,会出现什么情况？编译时出错。

error: Unexpected @FunctionalInterface annotation
  
@FunctionalInterface
  
^
    
I is not a functional interface
      
multiple non-overriding abstract methods found in interface I