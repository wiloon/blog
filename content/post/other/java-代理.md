---
title: java 代理模式
author: "-"
date: 2011-09-13T07:13:59+00:00
url: /?p=765
categories:
  - Java
tags:$
  - reprint
---
## java 代理模式
http://blog.csdn.net/dyh8818/article/details/314668

### 代理模式
  
代理模式的作用是: 为其他对象提供一种代理以控制对这个对象的访问。在某些情况下，一个客户不想或者不能直接引用另一个对象，而代理对象可以在客户端和目标对象之间起到中介的作用。
  
代理模式一般涉及到的角色有: 
  
抽象角色: 声明真实对象和代理对象的共同接口；
  
代理角色: 代理对象角色内部含有对真实对象的引用，从而可以操作真实对象，同时代理对象提供与真实对象相同的接口以便在任何时刻都能代替真实对象。同时，代理对象可以在执行真实对象操作时，附加其他的操作，相当于对真实对象进行封装。
  
真实角色: 代理角色所代表的真实对象，是我们最终要引用的对象。(参见文献1)
  
以下以《Java与模式》中的示例为例: 
  
抽象角色: 
  
abstract public class Subject
  
{
      
abstract public void request();
  
}
  
真实角色: 实现了Subject的request()方法。
  
public class RealSubject extends Subject
  
{
         
public RealSubject()
         
{
         
}

public void request()
         
{
                
System.out.println("From real subject.");
         
}
  
}
  
代理角色: 
  
public class ProxySubject extends Subject
  
{
      
private RealSubject realSubject; //以真实角色作为代理角色的属性

public ProxySubject()
         
{
         
}

public void request() //该方法封装了真实对象的request方法
         
{
          
preRequest();
                
if( realSubject == null )
          
{
                       
realSubject = new RealSubject();
                
}
          
realSubject.request(); //此处执行真实对象的request方法
          
postRequest();
         
}

private void preRequest()
      
{
          
//something you want to do before requesting
      
}

private void postRequest()
      
{
          
//something you want to do after requesting
      
}
  
}
  
客户端调用: 
  
Subject sub=new ProxySubject();
  
Sub.request();
         
由以上代码可以看出，客户实际需要调用的是RealSubject类的request()方法，现在用ProxySubject来代理RealSubject类，同样达到目的，同时还封装了其他方法(preRequest(),postRequest())，可以处理一些其他问题。
         
另外，如果要按照上述的方法使用代理模式，那么真实角色必须是事先已经存在的，并将其作为代理对象的内部属性。但是实际使用时，一个真实角色必须对应一个代理角色，如果大量使用会导致类的急剧膨胀；此外，如果事先并不知道真实角色，该如何使用代理呢？这个问题可以通过Java的动态代理类来解决。

2.动态代理类
         
Java动态代理类位于Java.lang.reflect包下，一般主要涉及到以下两个类: 
  
(1). Interface InvocationHandler: 该接口中仅定义了一个方法Object: invoke(Object obj,Method method, Object[] args)。在实际使用时，第一个参数obj一般是指代理类，method是被代理的方法，如上例中的request()，args为该方法的参数数组。这个抽象方法在代理类中动态实现。

(2).Proxy: 该类即为动态代理类，作用类似于上例中的ProxySubject，其中主要包含以下内容: 
  
Protected Proxy(InvocationHandler h): 构造函数，估计用于给内部的h赋值。
  
Static Class getProxyClass (ClassLoader loader, Class[] interfaces): 获得一个代理类，其中loader是类装载器，interfaces是真实类所拥有的全部接口的数组。
  
Static Object newProxyInstance(ClassLoader loader, Class[] interfaces, InvocationHandler h): 返回代理类的一个实例，返回后的代理类可以当作被代理类使用(可使用被代理类的在Subject接口中声明过的方法)。

所谓Dynamic Proxy是这样一种class: 它是在运行时生成的class，在生成它时你必须提供一组interface给它，然后该class就宣称它实现了这些interface。你当然可以把该class的实例当作这些interface中的任何一个来用。当然啦，这个Dynamic Proxy其实就是一个Proxy，它不会替你作实质性的工作，在生成它的实例时你必须提供一个handler，由它接管实际的工作。(参见文献3)
      
在使用动态代理类时，我们必须实现InvocationHandler接口，以第一节中的示例为例: 
  
抽象角色(之前是抽象类，此处应改为接口): 
  
public interface Subject
  
{
      
abstract public void request();
  
}
  
具体角色RealSubject: 同上；

代理角色: 
  
import java.lang.reflect.Method;
  
import java.lang.reflect.InvocationHandler;

public class DynamicSubject implements InvocationHandler {
    
private Object sub;

public DynamicSubject() {
    
}

public DynamicSubject(Object obj) {
      
sub = obj;
    
}

public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
      
System.out.println("before calling " + method);

method.invoke(sub,args);

System.out.println("after calling " + method);
      
return null;
    
}

}

该代理类的内部属性为Object类，实际使用时通过该类的构造函数DynamicSubject(Object obj)对其赋值；此外，在该类还实现了invoke方法，该方法中的
  
method.invoke(sub,args);
  
其实就是调用被代理对象的将要被执行的方法，方法参数sub是实际的被代理对象，args为执行被代理对象相应操作所需的参数。通过动态代理类，我们可以在调用之前或之后执行一些相关操作。
  
客户端: 
  
import java.lang.reflect.InvocationHandler;
  
import java.lang.reflect.Proxy;
  
import java.lang.reflect.Constructor;
  
import java.lang.reflect.Method;

public class Client
  
{

static public void main(String[] args) throws Throwable
         
{
        
RealSubject rs = new RealSubject(); //在这里指定被代理类
        
InvocationHandler ds = new DynamicSubject(rs); //初始化代理类
           
Class cls = rs.getClass();
        
//以下是分解步骤
        
/*
        
Class c = Proxy.getProxyClass(cls.getClassLoader(),cls.getInterfaces()) ;
        
Constructor ct=c.getConstructor(new Class[]{InvocationHandler.class});
        
Subject subject =(Subject) ct.newInstance(new Object[]{ds});
       
*/
       
//以下是一次性生成
        
Subject subject = (Subject) Proxy.newProxyInstance(cls.getClassLoader(),
                                   
cls.getInterfaces(),ds );

subject.request();
  
}
         
通过这种方式，被代理的对象(RealSubject)可以在运行时动态改变，需要控制的接口(Subject接口)可以在运行时改变，控制的方式(DynamicSubject类)也可以动态改变，从而实现了非常灵活的动态代理关系(参见文献2)。

参考文献: 
  
>阎宏，《Java 与模式》
>透明,《动态代理的前世今生》 
>Forest Hou，《Dynamic Proxy 在 Java RMI 中的应用》