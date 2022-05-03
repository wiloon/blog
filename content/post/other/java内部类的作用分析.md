---
title: java 内部类, 静态内部类, inner class
author: "-"
date: 2014-04-04T01:00:31+00:00
url: inner-class
categories:
  - Java
tags:
  - Java

---
## java 内部类, 静态内部类, inner class
# 内部类
```java
public class OuterClass {
    private String name;
    private int age;
    class InnerClass {
        public InnerClass(){
            name = "mark";
            age = 20;
        }
        public void echo() {
            System.out.println(name + " " + age);
        }
    }
}


```

问题思考
上面这个很简单的例子中，也包含了很多应该思考的问题：

内部类如何被实例化？
内部类能否改变外围类的属性，两者之间又是什么一种关系？
内部类存在的意义是什么？

在回答这三个问题之前，必须要明确一个点，那就是内部类是依附于外围类而存在的，其实也就是内部类存在着指向外围类的引用。明白了这个之后，上面的问题就好解答了。
实例化与数据访问
内部类与外围类之间形成了一种联系，使得内部类可以无限制地访问外围类中的任意属性。
正如上面的例子中，InnerClass内部可以随意访问OuterClass中的private属性。
同样的，因为内部类依赖与外围类的存在，所以无法在外部直接将其实例化，而是必须先实例化外围类，才能够实例化内部类 (注意，在外围类的成员方法里仍然是可以直接实例化内部类的）：
public static void main(String[] args) {
        InnerClass inner = new OuterClass().new InnerClass();
        inner.echo();
}
复制代码使用外围类的.new来创建外部类。
我们也知道，内部类和外围类的联系是通过内部类所持有的外部类的引用来实现的，想要获取这个引用，可以使用外围类的.this来实现，可以参考下面这个测试用例
public class OuterClass {
    private String name;
    private int age;
    class InnerClass {
        public InnerClass(){
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
复制代码内部类的作用
内部类创建起来很麻烦，使用起来也令人困扰，那么内部类存在的意义是什么呢？
实现多重继承
这可能是内部类存在的最重要的意义，参考《Thinking in Java》中的解释：

使用内部类最吸引人的原因是：每个内部类都能独立地继承一个 (接口的）实现，所以无论外围类是否已经继承了某个 (接口的）实现，对于内部类都没有影响。

我们都知道，Java中取消了C++中类的多重继承(但是允许接口的多重实现)，但是在实际编程中，又不免会遇到同一个类需要同时继承自两个类的情况，这时候就可以使用内部类来实现了。
比如有两个抽象类
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
复制代码如果想要同时继承这两个类，势必会引起number变量的冲突，以及sayHello方法的冲突，这些问题在C++中是以一种复杂的方案来实现的，如果使用内部类，就可以使用两个不同的类来继承不同的基类，并且可以根据自己的需要来组织数据的访问：
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
复制代码其他
(摘自《Think in Java》）


内部类可以用多个实例，每个实例都有自己的状态信息，并且与其他外围对象的信息相互独立。


在单个外围类中，可以让多个内部类以不同的方式实现同一个接口，或者继承同一个类。


创建内部类对象的时刻并不依赖于外围类对象的创建。


内部类并没有令人迷惑的“is-a”关系，他就是一个独立的实体。


内部类提供了更好的封装，除了该外围类，其他类都不能访问。


内部类的分类
上面的例子中创建的内部类，都属于成员内部类，实际上Java中还有三种其他的内部类：


局部内部类
嵌套在方法里或者是某个作用域内，通常情况下不希望这个类是公共可用的，相比于成员内部类，局部内部类的作用域更加狭小了，出了方法或者作用域就无法被访问。一般用于在内部实现一些私有的辅助功能。
定义在方法里：
public class Parcel5 {
public Destionation destionation(String str){
    class PDestionation implements Destionation{
        private String label;
        private PDestionation(String whereTo){
            label = whereTo;
        }
        public String readLabel(){
            return label;
        }
    }
    return new PDestionation(str);
}

public static void main(String[] args) {
    Parcel5 parcel5 = new Parcel5();
    Destionation d = parcel5.destionation("chenssy");
}
}
复制代码定义在作用域内：
public class Parcel6 {
private void internalTracking(boolean b){
    if(b){
        class TrackingSlip{
            private String id;
            TrackingSlip(String s) {
                id = s;
            }
            String getSlip(){
                return id;
            }
        }
        TrackingSlip ts = new TrackingSlip("chenssy");
        String string = ts.getSlip();
    }
}

public void track(){
    internalTracking(true);
}

public static void main(String[] args) {
    Parcel6 parcel6 = new Parcel6();
    parcel6.track();
}
复制代码

}
```


静态内部类
使用了static修饰的内部类即为静态内部类，和普通的成员内部类最大的不同是，静态内部类没有了指向外围类的引用。
因此，它的创建不需要依赖于外围类，但也不能够使用任何外围类的非static成员变量和方法。
静态内部类一个很好的用途是，用来创建线程安全的单例模式：
public class Singleton {  
    private static class SingletonHolder {  
        private static final Singleton INSTANCE = new Singleton();  
    }  
    private Singleton (){}  
    public static final Singleton getInstance() {  
        return SingletonHolder.INSTANCE; 
    }  
}
复制代码这是利用了JVM的特性：静态内部类时在类加载时实现的，因此不会受到多线程的影响，自然也就不会出现多个实例。


匿名内部类
匿名内部类就是没有被命名的内部类，当我们需要快速创建多个Thread的时候，经常会使用到它：
new Thread(new Runnable() {
        @Override
        public void run() {
            System.out.println("hello");
        }
    }).start();
复制代码当然现在也可以用λ表达式来实现了，我们暂且不提这两者之间的关系，先来看一下使用匿名内部类时要注意哪些事情：

匿名内部类没有访问修饰符，也没有构造方法
匿名内部类依附于接口而存在，如果它要继承的接口并不存在，那这个类就无法被创建
如果匿名内部类要访问局部变量，那这个数据必须是final的

熟悉函数式编程的人会发现匿名内部类和函数闭包有些类似 (这也是为什么能够用λ表达式来代替它），但实际上两者还是有着一些区别的，下面的部分中我们就来对比闭包和内部类。

作者：不洗碗工作室
链接：https://juejin.cn/post/6844903655510917128
来源：稀土掘金
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

---

使用静态内部类提高封装性

Java中的嵌套类 (Nested Class) 分为两种: 静态内部类 (也叫静态嵌套类，Static Nested Class) 和内部类 (Inner Class) 。内部类我们介绍过很多了，现在来看看静态内部类。什么是静态内部类呢？是内部类，并且是静态 (static修饰) 的即为静态内部类。只有在是静态内部类的情况下才能把static修复符放在类前，其他任何时候static都是不能修饰类的。

静态内部类的形式很好理解，但是为什么需要静态内部类呢？那是因为静态内部类有两个优点: 加强了类的封装性和提高了代码的可读性，我们通过一段代码来解释这两个优点，如下所示: 

```java
public class Person{
     private String name;
     private Home home;
     public Person(String _name){
          name = _name;
     }
     public static class Home{
          private String address;
          private String tel;
          public Home(String _address,String _tel){
            address = _address;
            tel = _tel;
          }
     }
}
```

其中，Person类中定义了一个静态内部类Home，它表示的意思是"人的家庭信息"，由于Home类封装了家庭信息，不用在Person类中再定义homeAddre、homeTel等属性，这就使封装性提高了。同时我们仅仅通过代码就可以分析出Person和Home之间的强关联关系，也就是说语义增强了，可读性提高了。所以在使用时就会非常清楚它要表达的含义: 

```java
public static void main(String[] args) {
     Person p = new Person("张三");
     p.setHome(new Person.Home("上海","021"));
}
```

定义张三这个人，然后通过Person.Home类设置张三的家庭信息，这是不是就和我们真实世界的情形相同了？先登记人的主要信息，然后登记人员的分类信息。可能你又要问了，这和我们一般定义的类有什么区别呢？又有什么吸引人的地方呢？如下所示: 
  
- 提高封装性。从代码位置上来讲，静态内部类放置在外部类内，其代码层意义就是: 静态内部类是外部类的子行为或子属性，两者直接保持着一定的关系，比如在我们的例子中，看到Home类就知道它是Person的Home信息。
  
- 提高代码的可读性。相关联的代码放在一起，可读性当然提高了。

形似内部，神似外部。静态内部类虽然存在于外部类内，而且编译后的类文件名也包含外部类 (格式是: 外部类+$+内部类) ，但是它可以脱离外部类存在，也就是说我们仍然可以通过new Home()声明一个Home对象，只是需要导入"Person.Home"而已。

解释了这么多，读者可能会觉得外部类和静态内部类之间是组合关系 (Composition) 了，这是错误的，外部类和静态内部类之间有强关联关系，这仅仅表现在"字面"上，而深层次的抽象意义则依赖于类的设计。

那静态内部类与普通内部类有什么区别呢？问得好，区别如下: 

1. 静态内部类不持有外部类的引用
    在普通内部类中，我们可以直接访问外部类的属性、方法，即使是private类型也可以访问，这是因为内部类持有一个外部类的引用，可以自由访问。而静态内部类，则只可以访问外部类的静态方法和静态属性 (如果是private权限也能访问，这是由其代码位置所决定的) ，其他则不能访问。
 
2. 静态内部类不依赖外部类
普通内部类与外部类之间是相互依赖的关系，内部类实例不能脱离外部类实例，也就是说它们会同生同死，一起声明，一起被垃圾回收器回收。而静态内部类是可以独立存在的，即使外部类消亡了，静态内部类还是可以存在的。

3. 普通内部类不能声明static的方法和变量
普通内部类不能声明static的方法和变量，注意这里说的是变量，常量 (也就是final static修饰的属性) 还是可以的，而静态内部类形似外部类，没有任何限制。

提起Java内部类 (Inner Class) 可能很多人不太熟悉，实际上类似的概念在C++里也有，那就是嵌套类 (Nested Class) ，关于这两者的区别与联系，在下文中会有对比。内部类从表面上看，就是在类中又定义了一个类 (下文会看到，内部类可以在很多地方定义) ，而实际上并没有那么简单，乍看上去内部类似乎有些多余，它的用处对于初学者来说可能并不是那么显著，但是随着对它的深入了解，你会发现Java的设计者在内部类身上的确是用心良苦。学会使用内部类，是掌握Java高级编程的一部分，它可以让你更优雅地设计你的程序结构。下面从以下几个方面来介绍: 

第一次见面

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

在这个例子里类Content和GDestination被定义在了类Goods内部，并且分别有着protected和private修饰符来控制访问级别。Content代表着Goods的内容，而GDestination代表着Goods的目的地。它们分别实现了两个接口Content和Destination。在后面的main方法里，直接用 Contents c和Destination d进行操作，你甚至连这两个内部类的名字都没有看见！这样，内部类的第一个好处就体现出来了 隐藏你不想让别人知道的操作，也即封装性。

同时，我们也发现了在外部类作用范围之外得到内部类对象的第一个方法，那就是利用其外部类的方法创建并返回。上例中的cont()和dest()方法就是这么做的。那么还有没有别的方法呢？当然有，其语法格式如下: 

outerObject=new outerClass(Constructor Parameters);

outerClass.innerClass innerObject=outerObject.new InnerClass(Constructor Parameters);

注意在创建非静态内部类对象时，一定要先创建起相应的外部类对象。至于原因，也就引出了我们下一个话题 非静态内部类对象有着指向其外部类对象的引用，对刚才的例子稍作修改: 

```java
public class Goods {

private int valueRate = 2;

private class Content implements Contents {

private int i = 11 * valueRate;

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
```

在这里我们给Goods类增加了一个private成员变量valueRate，意义是货物的价值系数，在内部类Content的方法value()计算价值时把它乘上。我们发现，value()可以访问valueRate，这也是内部类的第二个好处 一个内部类对象可以访问创建它的外部类对象的内容，甚至包括私有变量！这是一个非常有用的特性，为我们在设计时提供了更多的思路和捷径。要想实现这个功能，内部类对象就必须有指向外部类对象的引用。Java编译器在创建内部类对象时，隐式的把其外部类对象的引用也传了进去并一直保存着。这样就使得内部类对象始终可以访问其外部类对象，同时这也是为什么在外部类作用范围之外向要创建内部类对象必须先创建其外部类对象的原因。

有人会问，如果内部类里的一个成员变量与外部类的一个成员变量同名，也即外部类的同名成员变量被屏蔽了，怎么办？没事，Java里用如下格式表达外部类的引用: 

outerClass.this

有了它，我们就不怕这种屏蔽的情况了。

静态内部类

和普通的类一样，内部类也可以有静态的。不过和非静态内部类相比，区别就在于静态内部类没有了指向外部的引用。这实际上和C++中的嵌套类很相像了，Java内部类与C++嵌套类最大的不同就在于是否有指向外部的引用这一点上，当然从设计的角度以及以它一些细节来讲还有区别。

除此之外，在任何非静态内部类中，都不能有静态数据，静态方法或者又一个静态内部类 (内部类的嵌套可以不止一层) 。不过静态内部类中却可以拥有这一切。这也算是两者的第二个区别吧。

局部内部类

是的，Java内部类也可以是局部的，它可以定义在一个方法甚至一个代码块之内。





public class Goods1 {

public Destination dest(String s) {

class GDestination implements Destination {

private String label;

private GDestination(String whereTo) {

label = whereTo;

}

public String readLabel() {

return label;

}

}

return new GDestination(s);

}

public static void main(String[] args) {

Goods1 g = new Goods1();

Destination d = g.dest("Beijing");

}

}

上面就是这样一个例子。在方法dest中我们定义了一个内部类，最后由这个方法返回这个内部类的对象。如果我们在用一个内部类的时候仅需要创建它的一个对象并创给外部，就可以这样做。当然，定义在方法中的内部类可以使设计多样化，用途绝不仅仅在这一点。

下面有一个更怪的例子: 





public class Goods2 {

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

TrackingSlip ts = new TrackingSlip("slip");

String s = ts.getSlip();

}

}

public void track() {

internalTracking(true);

}

public static void main(String[] args) {

Goods2 g = new Goods2();

g.track();

}

}

你不能在if之外创建这个内部类的对象，因为这已经超出了它的作用域。不过在编译的时候，内部类TrackingSlip和其他类一样同时被编译，只不过它由它自己的作用域，超出了这个范围就无效，除此之外它和其他内部类并没有区别。

匿名内部类

java的匿名内部类的语法规则看上去有些古怪，不过如同匿名数组一样，当你只需要创建一个类的对象而且用不上它的名字时，使用内部类可以使代码看上去简洁清楚。它的语法规则是这样的: 

new interfacename(){……}; 或 new superclassname(){……};

下面接着前面继续举例子: 





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

这里方法cont()使用匿名内部类直接返回了一个实现了接口Contents的类的对象，看上去的确十分简洁。

在java的事件处理的匿名适配器中，匿名内部类被大量的使用。例如在想关闭窗口时加上这样一句代码: 





frame.addWindowListener(new WindowAdapter(){

public void windowClosing(WindowEvent e){

System.exit(0);

}

});

有一点需要注意的是，匿名内部类由于没有名字，所以它没有构造函数 (但是如果这个匿名内部类继承了一个只含有带参数构造函数的父类，创建它的时候必须带上这些参数，并在实现的过程中使用super关键字调用相应的内容) 。如果你想要初始化它的成员变量，有下面几种方法: 

如果是在一个方法的匿名内部类，可以利用这个方法传进你想要的参数，不过记住，这些参数必须被声明为final。

将匿名内部类改造成有名字的局部内部类，这样它就可以拥有构造函数了。

在这个匿名内部类中使用初始化代码块。

为什么需要内部类？

java内部类有什么好处？为什么需要内部类？

首先举一个简单的例子，如果你想实现一个接口，但是这个接口中的一个方法和你构想的这个类中的一个方法的名称，参数相同，你应该怎么办？这时候，你可以建一个内部类实现这个接口。由于内部类对外部类的所有内容都是可访问的，所以这样做可以完成所有你直接实现这个接口的功能。

不过你可能要质疑，更改一下方法的不就行了吗？

的确，以此作为设计内部类的理由，实在没有说服力。

真正的原因是这样的，java中的内部类和接口加在一起，可以的解决常被C++程序员抱怨java中存在的一个问题 没有多继承。实际上，C++的多继承设计起来很复杂，而java通过内部类加上接口，可以很好的实现多继承的效果。
  
http://book.51cto.com/art/201202/317517.htm
  
http://blog.csdn.net/ilibaba/article/details/3866537