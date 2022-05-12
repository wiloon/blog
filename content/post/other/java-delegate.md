---
title: java Delegate
author: "-"
date: 2012-10-08T09:05:13+00:00
url: /?p=4386
categories:
  - Java
tags:
  - reprint
---
## java Delegate
委派，也可以叫做委托，从字面上来理解的话，应该是委托其他类做事情而自己不做或者只做一部分工作；而回调，就是调用自己的方法。 在 java 中，这两种机制很类似，你姑且可以认为它们就是一码事。 java 中，实现委派和回调都是通过接口来实现的。下面举个小例子吧！

该例子是这样的 (只是一个例子) : 

ProfessionalWorker 、SparetimeWorker 负责发射 Rocket，Rocket 类通过接口 IRocketDelegate 委派 (或者说是回调)  ProfessionalWorker 、SparetimeWorker自己发射。

总之，Rocket不做具体的事情。看实例代码: 

IRocketDelegate.java源码

```java

public interface IRocketDelegate {

public abstract long startAtTime();

public abstract long endAtTime();

public abstract void sendDidFail();

}

```

共有三个方法，分别是用于计算 Rocket 发射时间、计算 Rocket 发射完毕的时间以及发送是否失败的。

Rocket.java源码

```java

public class Rocket {

IRocketDelegate delegate = null;

public Rocket(IRocketDelegate delegate) {

this.delegate = delegate;

}

private long getRocketStartTime() {

long startTime = delegate.startAtTime();

return startTime;

}

private long getRocketEndTime() {

long endTime = delegate.endAtTime();

return endTime;

}

public boolean isOk() {

// 超时0.1秒为失败

if (getRocketEndTime() - getRocketStartTime() >= 100) {

delegate.sendDidFail();

return false;

}

return true;

}
  
}
  
```

在这个类中，声明一个 IRocketDelegate 接口对象，使用该对象调用接口的方法。我们知道，接口不可以直接实例化，换句话说，实例化接口必须实现接口的所有方法。

那么，我们就把这些实现工作交给具体的发射者来完成。实现回调。

ProfessionalWorker.java源码

```java

public class ProfessionalWorker implements IRocketDelegate {

@Override

public long startAtTime() {

System.out.println("startAtTime is call-back inProfessionalWorker!");

return System.currentTimeMillis();

}

@Override

public long endAtTime() {

System.out.println("endAtTime is call-back in ProfessionalWorker!");

return System.currentTimeMillis();

}

@Override

public void sendDidFail() {

System.out.println("ProfessionalWorker send Rocket fail !");

}

public void send() {

if (new Rocket(this).isOk()) {

System.out.println("ProfessionalWorker send Rocket ok !");

}

}

}

```

SparetimeWorker.java源码

```java
  
public class SparetimeWorker {
  
public void send() {
  
boolean isOk = new Rocket(new IRocketDelegate() {
  
@Override
  
public long startAtTime() {
  
System.out.println("startAtTime is call-back in SparetimeWorker !");
  
return System.currentTimeMillis();
  
}

@Override
  
public long endAtTime() {
  
System.out.println("endAtTime is call-back in SparetimeWorker!");
  
return System.currentTimeMillis() + 100L;
  
}

@Override
  
public void sendDidFail() {
  
System.out.println("SparetimeWorker send Rocket fail !");
  
}
  
}).isOk();

if(isOk) {

System.out.println("SparetimeWorker send Rocket ok !");

}
  
}
  
}
  
```

这个类采用内部类的方式完成。

Test.java

```java

public class Test {

public static void main(String[] args) {

new ProfessionalWorker().send();

System.out.println("\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***");

new SparetimeWorker().send();

}

}

```

显示结果

endAtTime is call-back in ProfessionalWorker!

startAtTime is call-back inProfessionalWorker!

ProfessionalWorker send Rocket ok !

\***\***\***\***\***\***\***\***\***\***\***\***\***\***\***

endAtTime is call-back in SparetimeWorker!

startAtTime is call-back in SparetimeWorker !

SparetimeWorker send Rocket fail !

这就体现 Java 中的一句话 Don't call me,I'll call you. 其含义就是回调 (或者委派/委托) 。

android 中很多这样的用法，关于接口的好处还有很多，后续慢慢研究，记住一句话: 面向对象面向接口编程。

<http://blog.csdn.net/androidbluetooth/article/details/6937468>

<http://hbohuan.blog.163.com/blog/static/208489820077132225530/>