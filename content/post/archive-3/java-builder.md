---
title: 'Java   Builder'
author: "-"
date: 2019-05-13T10:59:45+00:00
url: /?p=14333
categories:
  - Inbox
tags:
  - reprint
---
## 'Java   Builder'
https://juejin.im/entry/5b83fe1851882542e16bfcf6

Java 中的 Builder 模式和协变返回类型
  
阅读 735
  
收藏 45
  
2018-08-27
  
原文链接: www.codebelief.com
  
阅读这篇文章大约需要五到十分钟时间。

Builder 模式是一种创建型的设计模式，即解决对象的创建问题。

在 Java、C++ 这类语言中，如果一个类在创建时存在可选参数，那么可以通过函数重载来实现，但是如果可选参数非常多的话，构造函数的数量也会变得非常多，并且可能因为不同可选参数类型相同而没法重载，我们接下来通过例子来说明。

一、可选参数带来的问题
  
不可重载的情况
  
//学号、姓名是必须参数，身高、体重可选
  
public Student(int id, String name) {}
  
public Student(int id, String name, float height, float weight) {}
  
public Student(int id, String name, float height) {} //只填身高
  
public Student(int id, String name, float weight) {} //只填体重 (签名重复，无法重载) 
  
虽然最后两个构造方法参数名不同，但是它们类型相同，方法签名也就相同，因此没办法重载，只能保留一个。

构造方法数量过多
  
接着考虑这么一个场景，你正在设计一个 Person 类，这个类存放了 name、age、sex 等信息，其中 name 是必要信息，而 age 和 sex 是可选信息，那么你可能会编写如下的构造方法: 

public class Person {
      
private String name;
      
private int age;
      
private String sex;

    public Person(String name) {}
    public Person(String name, int age) {}
    public Person(String name, String sex) {}
    public Person(String name, int age, int sex) {}
    

}
  
我们利用 Java 方法的重载，来实现参数的"可选"，但我们也因此不得不设计很多的构造方法，来应对不同的对象创建需求。而且，上面的例子中只有两个可选参数，当我们需要更多的可选参数时，这种实现方式几乎不可行。

在某些语言中，可以通过"命名可选参数"来解决这个问题，例如 Python 中可以这么实现: 

class Person:
      
def **init**(self, name, age = 0, sex = "unknown"):
          
self.name = name
          
self.age = age
          
self.sex = sex
  
其中 self 和 Java 中的 this 类似，指代当前对象。我们将必须的参数写在前面，将可选参数写在后面 (通过给参数赋默认值的方式来表示该参数是可选参数) 。

当我们创建 Person 对象时，可以有以下几种写法: 

Tom = Person("Tom", age=18)
  
John = Person("John", sex="male")
  
Lily = Person("Lily", age=20, sex="female")
  
Python 在语言层面已经有了很优雅的解决方法，而 Java 语言层面只有重载的方式，在上面的分析中，我们已经看到了这种方式的弊端。

为什么不用 set 方法？
  
可能你会说，我们只需要一个构造函数，要求提供必要的参数。

剩下的可选参数，我们提供对应的 set 方法，让使用者在创建对象后选择性地设置不就可以了吗？

确实，有些情况可以这么实现。

但是，这种方式相当于将对象的创建过程拆分成了很多步骤，对象在这个创建过程中暴露给了外界，却又尚未创建完毕，导致其处于一种不连续的状态，在多线程环境下存在风险。

此外，很多时候我们需要创建不可变的对象 (immutable object) ，这种方法由于允许随时改变对象的属性，因此没办法保证对象的不可变。

为了解决这一问题，就有了 Builder 模式。

二、使用 Builder 模式
  
我们可以将对象可选参数的设置过程单独拿出来，交给 Builder 来完成，等参数设置好了之后，再根据这些参数创建 Person 对象，得到不可变的 Person 对象。

Person 类及嵌套的 Builder 类: 

public class Person {
      
private String name;
      
private int age;
      
private String sex;

    protected Person(Builder builder) {
        this.name = builder.name;
        this.age = builder.age;
        this.sex = builder.sex;
    }
    
    public static class Builder {
        private String name;
        private int age;
        private String sex;
    
        public Builder(String name) {
            this.name = name;
        }
    
        public Builder age(String age) {
            this.age = age;
            return this;
        }
    
        public Builder sex(String sex) {
            this.sex = sex;
            return this;
        }
    
        public Person build() {
            return new Person(this);
        }
    }
    

}
  
创建 Person 对象: 

Person person = new Person.Builder("John")
          
.age(20)
          
.sex("male")
          
.build();
  
我们通过 Builder 的链式调用来模拟"命名可选参数"，设置完成后，调用 build 方法创建一个 Person 对象，如此一来，既有了 set 方法的简便，又能得到不可变的 Person 对象。

三、Builder 继承时的返回类型问题
  
我们发现 Builder 模式很好地解决了带有可选参数的对象创建问题，既能保证对象创建时是连续的，又能保证创建的对象不可被改变。

我们继续假设另一个场景，给外卖系统设计一个 Customer 类，由于我们已经有了 Person 类，所以可以直接继承该类，进行扩展。

外卖系统中的 Customer 有三个信息是必须的: 姓名、手机号、地址。

可选信息: 昵称、个人介绍。

所以 Customer 类设计如下: 

public class Customer extends Person {
      
private long phone;
      
private String address;
      
private String alias;
      
private String intro;

    private Customer(Builder builder) {
        super(builder);
        this.phone = builder.phone;
        this.alias = builder.alias;
        this.intro = builder.intro;
    }
    
    public static class Builder extends Person.Builder {
        private long phone;
        private String address;
        private String alias;
        private String intro;
    
        public Builder(String name, long phone, String address) {
            super(name);
            this.phone = phone;
            this.address = address;
        }
    
        public Builder alias(String alias) {
            this.alias = alias;
            return this;
        }
    
        public Builder intro(String intro) {
            this.intro = intro;
            return this;
        }
    
        @Override
        public Customer build() {
            return new Customer(this);
        }
    }
    

}
  
我们给 Customer 类增加了四个成员变量，也在 Customer.Builder 当中进行了相应的扩展，但是，当我们尝试调用参数设置方法时就会发现问题: 

Customer customer = new Customer.Builder("Tom", 13999999999L, "北京市XXX")
          
.age(20) //此处返回类型为 Person.Builder
          
.alias("用户昵称") //错误，不存在该方法
          
.intro("用户自我介绍");
  
我们发现，这么继承父类 Builder 是有问题的。Java 不存在"自身类型"这个概念，也就是说，当一个子类继承了父类之后，原先父类中返回值为父类类型的方法，仍旧返回父类类型，并不会变成子类类型。

所以之前定义的方法返回类型仍旧是父类 Person.Builder，而不是当前的 Customer.Builder，因此还需要解决继承后，方法返回类型的问题。

解决方法有两种，在介绍之前，我们先理解什么是协变返回类型。

协变返回类型
  
协变返回类型 (Covariant Return Type) ，指的是当一个类被继承之后，该类中方法的返回类型变成子类对应的类型，这个改变后的返回类型就叫协变返回类型。

以 Java 中的 Object.clone() 方法为例，该方法在 Object 类中返回的类型是 Object 类型。我们知道，所有类都继承自 Object 类，所以我们在定义类时可以覆写类中的 clone() 方法: 

public class MyClass {
      
@Override
      
public MyClass clone() {
          
//...
      
}
  
}
  
我们将返回类型改为了当前类的类型，而不是父类中的 Object 类型，这就是协变返回类型，返回的类型变成了子类对应的类型。

协变返回类型并不局限于和类本身相同的类型，只要是存在对应关系，也可以认为是协变返回类型。

下面是 StackOverflow 上的一个例子: 

public class Animal {
      
protected Food seekFood() {
          
return new Food();
      
}
  
}
  
定义一个继承自 Animal 的 Dog 类: 

public class Dog extends Animal {
      
@Override
      
protected DogFood seekFood() {
          
return new DogFood();
      
}
  
}
  
我们看到，在 Dog 类继承 Animal 类之后，对应的寻找食物的方法，返回值也由 Food 变成了其子类 DogFood，这里的 DogFood 就是协变返回类型。

Override + 强制类型转换
  
我们知道，方法的签名只包括方法名、参数名、参数顺序，不包含返回类型。

所以我们可以覆写父类 Builder 的方法，让方法签名相同，但是返回类型改为子类 Customer.Builder，并将父类方法的返回值强制转换为 Customer.Builder，这样就能让所有方法都返回子类 Builder。

public class Customer extends Person {
      
//...
      
public static class Builder extends Person.Builder {
          
//...
          
@Override
          
public Builder age(int age) {
              
return (Builder) super.age(age);
          
}

        @Override
        public Builder sex(String sex) {
            return (Builder) super.sex(sex);
        }
        //...
    }
    //...
    

}
  
通过覆写父类方法，并对返回值进行强制类型转换，现在 Customer.Builder 类已经可以正常使用了。

这种方式的缺点也很明显，你需要覆写父类 Builder 的所有方法，并对返回值进行强制类型转换，这无疑会使代码变得很冗长。

接下来，我们看看另一种解决方法。

使用泛型模拟子类的自身类型
  
我们可以利用 Java 中的泛型，来模拟子类的自身类型 (self-type) 。

也就是说，我们想要在定义父类 Builder 时所指定的返回类型，可以在该类被继承时，自动变成子类的自身类型。

不过，这里使用的泛型参数列表不是简单的 <T>，而是递归的 <T extends Builder<T>>。

首先，将 Person.Builder 定义为泛型类: 

public class Person {
      
public static class Builder<T extends Builder<T>> {
          
//...
      
}
  
}
  
解释一下上述泛型中的递归类型参数，通常，简单的泛型只有一个类型参数 T，而这里的类型参数变成了递归的 T extends Builder<T>，为了方便解释，我们不妨写成 T1 extends Builder<T2>。

该递归参数表示类型 T1 是 Builder<T2> 的子类，由于 T 可以表示任意类型，所以 T2 可以表示 T extends Builder<T>，因此此处的 Builder<T2> 等价于当前泛型类 Builder<T extends Builder<T>>，所以 T1 就可以表示当前泛型类 Person.Builder 的子类。

定义完泛型之后，我们就可以在 Person.Builder 的方法中将 T 作为返回值: 

public class Person {
      
public static class Builder<T extends Builder<T>> {
          
//...
          
public T age(int age) {
              
this.age = age;
              
return (T) this;
          
}

        public T sex(String sex) {
            this.sex = sex;
            return (T) this;
        }
        //...
    }
    

}
  
定义子类 Customer.Builder 时，将当前 Builder 类型传入泛型参数中: 

public class Customer {
      
public static class Builder extends Person.Builder<Builder> {
          
//...
      
}
  
}
  
这样就能让父类中的类型参数 T 对应到当前子类 Customer.Builder，让方法返回当前的子类类型，也就不需要再覆写父类的设置参数方法了。

当然，由于最后的 build()方法要返回 Customer 类型，所以还需要覆写 build()。

我们注意到，父类 Builder 在返回子类类型时，需要将当前的 this 强制转换成子类类型。

我们也可以编写一个 self() 方法，来获得子类类型的实例: 

public class Person {
      
public static class Builder<T extends Builder<T>> {
          
public T age(int age) {
              
this.age = age;
              
return self();
          
}

        public T sex(String sex) {
            this.sex = sex;
            return self();
        }
    
        private T self() {
            return (T) this;
        }
    }
    

}
  
这样就无需在每一个方法中进行类型转换了。

假设我们不会直接用到 Person 类，使用的都是它的子类，于是我们决定将 Person 声明为一个抽象类，那么可以将 self() 方法声明为抽象方法，让子类去实现它，返回对应的子类实例: 

public abstract class Person {
      
public abstract static class Builder<T extends Builder<T>> {
          
public T age(int age) {
              
this.age = age;
              
return self();
          
}

        public T sex(String sex) {
            this.sex = sex;
            return self();
        }
    
        abstract protected T self(); //子类需要覆写该方法，返回对应的 this。
    }
    

}
  
四、总结
  
Java 中创建对象时如果存在可选参数，可以使用重载来实现不同参数的构造方法，但是这种方式会有可能在可选参数类型相同的情况下，无法完成重载，此外，在可选参数很多的时候，还会导致构造方法急剧增加的情况。

通过为可选参数提供 set 方法，可以让使用者在创建完对象后，手动设置感兴趣的参数，但这种方式会导致对象的实际创建过程被分散成很多步骤，处于一种不连续的状态，如果是在并发环境下，可能会出现问题。此外，这种方式没办法创建不可变对象，而很多情况下，我们希望得到的是不可变对象。

于是，我们使用 Builder 模式来创建对象，将要设置的参数先提供给 Builder，然后再调用 build() 方法获得一个目标对象，既方便设置可选参数，又能得到不可变对象。

之后，我们在文章中讨论了继承 Builder 时，返回的是父类类型的问题。因为在 Builder 模式中，我们是使用链式调用让设置参数的过程更简便，因此必须得返回子类的类型。

子类继承父类之后，将原先方法的返回类型变成该子类对应的类型，这个类型就叫做协变返回类型。

返回子类类型有两种方法，一种是在实现子类时，覆写父类的所有参数设置方法，将返回值改成子类类型，并强制将返回值转换成子类类型。

另一种是通过带递归类型参数的泛型，来模拟子类的自身类型。即我们将父类 Builder 声明为泛型类，然后将方法的返回类型用泛型参数 T 来代替，并将返回的 this 强制转换成类型 T。在实现子类时，将子类类型传入到父类的泛型参数列表中，这样父类中的参数设置方法就会自动返回子类类型。我们还可以将强制转换 this 为 T 类型的操作单独提取到 self() 方法中，通过这种方式，可以支持抽象类的定义，子类只需要覆写 self() 方法来返回对应的子类实例即可。

相关文章
  
Java 多线程下载器的设计与实现
  
Java 是如何利用接口避免函数回调的
  
Java 多线程的竞争条件、互斥和同步
  
Java GUI: Awt/Swing 实现图片的缩放与滚动查看
  
Java Swing 编写数据库增删改查 GUI 程序
  
Java Lambda 表达式的常见应用场景