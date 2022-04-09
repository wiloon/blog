---
title: 闭包, closure
author: "-"
date: 2014-08-10T07:38:21+00:00
url: closure
categories:
  - Uncategorized
tags:
  - Java

---
## 闭包, closure
### java内部类
>wiloon.com/inner-class

### 何为闭包
闭包是由函数及其相关的引用环境组合而成的实体(即：闭包=函数+引用环境)

### golang 闭包
```go
func Add(y int) {
    return func(x int) int {
        return x + y
    }
}

a := Add(10)
a(5) // return 15

```
我们知道这个返回的闭包中包含了Add函数中提供的变量y (也就是闭包产生的环境）
也就是说这个闭包包含了函数本身，以及一个对局部变量y的引用。
这里特别需要注意的一点是，如果y是定义在函数Add的调用栈里的一个变量，那么当Add()函数被调用完毕后，y就销毁了，这时候再用原来的指针去访问y就会出问题，因此这里就出现了一个原则：
闭包中引用的外部变量必须是在堆上分配的
实际上Go的编译器在处理到这个闭包时，会使用escape analyze来识别变量y的作用域，当发现变量y被一个闭包所引用时，就会把y转移到堆中 (这一过程称为变量逃逸）。
总结一下，闭包从底层理解，就是函数本身和其所需外部变量的引用，用R大的话来形容闭包的创建过程就是：

capture by reference

内部类与闭包
看一下最后我们对闭包的定义，“所需外部变量的引用”是否像极了Java中内部类对外围类的引用？
所以大家都认为Java中不存在闭包，其实Java里处处都是闭包 (对象就是闭包），以致于我们感觉不到自己在使用闭包，成员内部类就是一个最典型的例子，因为它持有一个指向外围类的引用，看下面这个例子:


### java 闭包
```java
public class OuterClass {
    private int y = 10;
    private class Inner {
        public int innerAdd(int x) {
            return x + y;
        }
    }

    public static void main(String[] args) {
        OuterClass outer = new OuterClass();
        Inner inner = outer.new Inner();
        System.out.println(inner.innerAdd(5)); //result: 15
    }
}
```
有很多不同的人都对闭包过进行了定义,这里收集了一些。

- 是引用了自由变量的函数。这个函数通常被定义在另一个外部函数中,并且引用了外部函数中的变量。 - <<wikipedia>>
- 是一个可调用的对象,它记录了一些信息,这些信息来自于创建它的作用域。- <<Java编程思想>>
- 是一个匿名的代码块,可以接受参数,并返回一个返回值,也可以引用和使用在它周围的,可见域中定义的变量。- Groovy ['ɡru:vi]
- 是一个表达式,它具有自由变量及邦定这些变量的上下文环境。
- 闭包允许你将一些行为封装,将它像一个对象一样传来递去,而且它依然能够访问到原来第一次声明时的上下文。
- 是指拥有多个变量和绑定了这些变量的环境的表达式 (通常是一个函数) ,因而这些变量也是该表达式的一部分。
- 闭包是可以包含自由 (未绑定) 变量的代码块；这些变量不是在这个代码块或者任何全局上下文中定义的,而是在定义代码块的环境中定义。

在这些定义中都有一些关键字: 变量、函数、上下文等, 闭包在回调函数、函数式编程、Lambda表达式中有重要的应用,为了更深刻的理解闭包,我们会试图通过JavaScript、C#和JAVA的代码进行举例,不过本次的重点还是通过JAVA如何这内部类来实现闭包,以及闭包的应用。

### JavaScript中的闭包。
在JavaScript中,闭包是通过函数的嵌套来实现,以下是一个简单的例子: 

### closure.htm
```html
<script type="text/javascript">
    function f1() {
        const n = 99;

        function f2() {
            alert(n);
        }

        return f2();
    }

    f1();
</script>
```

这段代码的特点: 
1. 函数f1()返回了函数f2()
2. 函数f2()引用了f1()定义的局部变量

正常来讲,我们在外部是不能操作到f1()函数内部所定义的局部变量n,但是通过变通的方法,我们在f1()函数内部定义了一个新的函数f2(),通过f2()输出其外围函数的局部变量n,f2()是f1()的内部函数,对于f2()来说其外围函数所定义的变量、函数等上下文是可以被内部函数所访问到的；最后在f1()函数中再调用f2()以在f1()被调用时触发对f2()的调用,从而把局部变量输出。 我们对照一下闭包的定义: "引用了自由变量的函数",这里的n就是定义中的自由变量,而函数f2()通过邦定自由变量n从而形式了一个闭包。

### JAVA中的闭包。
在JAVA中,闭包是通过"接口+内部类"实现,JAVA的内部类也可以有匿名内部类。我们现在就来详细认识一下JAVA内部类。

#### 内部类。
顾名思义,内部类就是将一个类定义在另一个类的内部。在JAVA中, 内部类可以访问到外围类的变量、方法或者其它内部类等所有成员,即使它被定义成 private 了, 但是外部类不能访问内部类中的变量。这样通过内部类就可以提供一种代码隐藏和代码组织的机制, 并且这些被组织的代码片段还可以自由的访问到包含该内部类的外围上下文环境。

这里提供了一个例子展示这种机制: 

### Closure.java
```java
public class ClosureX {
    private int length = 0;

    private class InnerClass implements ILog {
        @Override
        public void Write(String message) {
            length = message.length();
            System.out.println("DemoClass1.InnerClass:" + length);
        }
    }

    public ILog logger() {
        return new InnerClass();
    }

    public static void main(String[] args) {
        ClosureX closureX = new ClosureX();
        closureX.logger().Write("abc");
        ClosureX closureX1 = new ClosureX();
        InnerClass ic = closureX1.new InnerClass();
        ic.Write("abcde");
    }
}

interface ILog {
    public void Write(String message);
}
```

该例子的主要功能是实现一个写日志的ILog接口,但是该接口的类被定义在 ClosureX 这个外围类中了,而且这个InnerClass内部类还可以访问其外围类中的私有变量length。

#### .new
从上面的例子可见,InnerClass是定义在 ClosureX 内部的一个内部类,而且 InnerClass 还可以是Private。

如何创建这个 InnerClass 的实例? 可以通过外围类的实例进行创建,如: 

```java
ClosureX dc1 = new ClosureX();
InnerClass ic = dc1.new InnerClass();
ic.Write("abcde");
```

#### .this
如何通过this显式引用外围类的变量？通过此格式进行引用: {外围类名}.this.{变量名称}。如: 

```java
ClosureX.this.length = message.length();
```

#### 局部内部类。
局部内部类是指在方法的作用域内定义的的内部类。

### DemoClass2.java
```java
public class DemoClass2 {
    private int length = 0;

    public ILog logger() {
        //在方法体的作用域中定义此局部内部类
        class InnerClass implements ILog {
            @Override
            public void Write(String message) {
                length = message.length();
                System.out.println("DemoClass2.InnerClass:" + length);
            }
        }
        return new InnerClass();
    }
}
```

因为 InnerClass 类是定义在 logger() 方法体之内,所以 InnerClass 类在方法的外围是不可见的。

### 匿名内部类。
顾名思义,匿名内部类就是匿名、没有名字的内部类,通过匿名内部类可以更加简洁的创建一个内部类。
### DemoClass3.java
```java
public class DemoClass3 {
    private int length = 0;

    public ILog logger() {
        return new ILog() {
            @Override
            public void Write(String message) {
                length = message.length();
                System.out.println("DemoClass3.AnonymousClass:" + length);
            }
        };
    }
}
```

由此可见,要创建一个匿名内部类,可以 new 关键字来创建。

格式: new 接口名称(){}

格式: new 接口名称(args...){}


### final关键字。
闭包所绑定的本地变量必须使用final修饰符,以表示为一个恒定不变的数据,创建后不能被更改。
#### DemoClass4.java
```java
public class DemoClass4 {
    private int length = 0;

    public ILog logger(int level) {
        final int logLevel = level + 1;
        switch (level) {
            case 1:
                return new ILog() {
                    @Override
                    public void Write(String message) {
                        length = message.length();
                        System.out.println("DemoClass4.AnonymousClass:InfoLog "
                                + length);
                        System.out.println(logLevel);
                    }
                };
            default:
                return new ILog() {
                    @Override
                    public void Write(String message) {
                        length = message.length();
                        System.out.println("DemoClass4.AnonymousClass:ErrorLog "
                                + length);
                        System.out.println(logLevel);
                    }
                };
        }
    }

    public static void main(String[] args) {
        DemoClass4 demoClass4 = new DemoClass4();
        demoClass4.logger(1).Write("abcefghi");
    }
}
```

从例子中可以看到,logger 方法接受了一个level参数,以表示要写的日志等级, 这个level参数如果直接赋给内部类中使用,会导致编译时错误,提示level参数必须为final,这种机制防止了在闭包共享中变量取值错误的问题。解决方法可以像例子一样在方法体内定义一下新的局部变量,标记为final,然后把参数level赋值给它: 


final int logLevel = level ;
  
或者直接参数中添加一个final修饰符: 

public ILog logger(final int level {


### 实例初始化。

匿名类的实例初始化相当于构造器的作用,但不能重载。
#### DemoClass5.java
```java
public class DemoClass5 {
    private int length = 0;

    public ILog logger(final int level) throws Exception {
        return new ILog() {
            {
                if (level != 1)
                    throw new Exception("日志等级不正确！");
            }

            @Override
            public void Write(String message) {
                length = message.length();
                System.out.println("DemoClass5.AnonymousClass:" + length);
            }
        };
    }
}
```

匿名内部类的实例初始化工作可以通过符号 {...} 来标记,可以在匿名内部类实例化时进行一些初始化的工作,但是因为匿名内部类没有名称,所以不能进行重载,如果必须进行重载,只能定义成命名的内部类。


### 为什么需要闭包。
闭包的价值在于可以作为函数对象或者匿名函数,持有上下文数据,作为第一级对象进行传递和保存。闭包广泛用于回调函数、函数式编程中。

### lambda表达式
```java
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

public class Demo6 {
    @FunctionalInterface
    interface fun {
        void f();
    }

    @Setter
    @Getter
    @AllArgsConstructor
    static class MyInter {
        Integer i;
    }

    public static void main(String[] args) {
        Integer a = 1;
        fun fun = () -> System.out.println(a);
        // a=2;
    }
}
```
我们使用了变量a，这是没问题的。
但是如果我们再加一行 a =2； 那么就会编译报错,如果我们在lambda里面修改了a也是不行的。
java编译时已经强制要求lambda使用的变量不可修改了，所以final关键字不是必须的。
不能修改那么就达不成闭包的条件。

那可以使用一个对象把变量包起来。

```java
public class Demo7 {
    @FunctionalInterface
    interface fun {
        void f();
    }

    @Setter
    @Getter
    @AllArgsConstructor
    static class MyInter{
        Integer i;
    }

    public static void main(String[] args) {
        MyInter inter = new MyInter(1);
        fun fun = ()->inter.setI(2);
        fun.f();
        System.out.println("lambda修改后："+inter.getI());
        inter.setI(3);
        System.out.println("直接修改后："+inter.getI());
    }
}

```
闭包的价值
像上面说的，闭包可以为某种功能提供维持某种状态的能力，如数组遍历需要维持index.
举个栗子：打印给定数量的 斐波那契数列
```java
public class Demo8 {
    @FunctionalInterface
    interface fun {
        int f();
    }

    @Setter
    @Getter
    @AllArgsConstructor
    static class MyInter {
        Integer i;
    }

    public static void main(String[] args) {
        print(10);
    }

    public static void print(int n) {
        MyInter last = new MyInter(0);
        MyInter next = new MyInter(1);
        fun fun = () -> {
            int r = next.getI();
            int i = last.getI() + next.getI();
            last.setI(next.getI());
            next.setI(i);
            return r;
        };
        for (int i = 0; i < n; i++) {
            System.out.println(fun.f());
        }
    }
}


```
>https://juejin.cn/post/6844903655510917128
>http://www.cnblogs.com/chenjunbiao/archive/2011/01/26/1944417.html
>http://baike.baidu.com/view/648413.htm?fr=aladdin
>https://zhuanlan.zhihu.com/p/357864072
>https://juejin.cn/post/6844903969836236808
