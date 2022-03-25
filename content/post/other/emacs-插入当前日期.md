---
title: java
author: "-"
date: 2012-07-05T07:24:47+00:00
url: java
categories:
  - java

tags:
  - reprint
---
## java
### Package
关于包的使用，只需注意一点：在一个项目中，不可以有相同的两个包名，也就是说，包名不能和项目中其他的包名重复，这里不但包括自定义包名也包括项目所引用的类库的包名。

### 访问控制修饰符
Java中，可以使用访问控制符来保护对类、变量、方法和构造方法的访问。Java 支持 4 种不同的访问权限。

default (即默认，什么也不写）: 在同一包内可见，不使用任何修饰符。使用对象：类、接口、变量、方法。

private : 被 private 修饰的类成员只能在定义它的类中被访问，其他类都访问不到。 使用对象：变量、方法, 内部类. 注意：不能修饰外部类

public : 对所有类可见。使用对象：类、接口、变量、方法

### protected
protected : 使用对象：内部类、变量、方法。 注意：不能修饰类 (外部类）。
基类的protected成员是包内可见的，并且对子类可见；

若子类与基类不在同一包中，那么在子类中，子类实例可以访问其从基类继承而来的protected方法，而不能访问基类实例的protected方法。

```java
//示例一
package p1;
public class Father1 {
    protected void f() {}    // 父类Father1中的protected方法
}

package p1;
public class Son1 extends Father1 {}

package p11;
public class Son11 extends Father1{}

package p1;
public class Test1 {
    public static void main(String[] args) {
        Son1 son1 = new Son1();
        son1.f(); // Compile OK     ---- (1）
        // son1.clone(); // Compile Error     ---- (2）

        Son11 son11 = new Son11();
        son11.f(); // Compile OK     ---- (3）
        // son11.clone(); // Compile Error     ---- (4）
    }
}

```

对于上面的示例，首先看(1)(3)，其中的f()方法从类Father1继承而来，其可见性是包p1及其子类Son1和Son11，而由于调用f()方法的类Test1所在的包也是p1，因此 (1）(3)处编译通过。其次看(2)(4)，其中的clone()方法的可见性是java.lang包及其所有子类，对于语句“son1.clone();”和“son11.clone();”，二者的clone()在类Son1、Son11中是可见的，但对Test1是不可见的，因此 (1）(3)处编译不通过。
————————————————
版权声明：本文为CSDN博主「书呆子Rico」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/justloveyou_/article/details/61672133
