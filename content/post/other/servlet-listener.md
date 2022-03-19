---
title: servlet listener
author: "-"
date: 2012-06-10T13:32:56+00:00
url: /?p=3509
categories:
  - Java
  - Web
tags:
  - Servlet

---
## servlet listener
Listener是一种观察者模式的实现: 我们在web.xml中配置listener的时候就是把一个被观察者放入的观察者的观察对象队列中，当被观察者触发了注册事件时观察者作出相应的反应。在jsp/servlet中具体的实现是在web.xml中注册Listener，由Container在特定事件发生时呼叫特定的实现Listener的类。
  
总体上说servlet中有主要有3类事件既: 

Servlet上下文事件、

会话事件与请求事件总共有8个listener接口，我们在web.xml中注册时对应上自己对相应接口的实现类即可: 
  
Servlet中的Listener和Event:
  
在JSP 2.0/Servlet 2.4中，共有八个Listener接口，六个Event类别。


  
    
      Listener接口
    
    
    
      Event类
    
  
  
  
    
      ServletContextListener
    
    
    
      ServletContextEvent
    
  
  
  
    
      ServletContextAttributeListener
    
    
    
      ServletContextAttributeEvent
    
  
  
  
    
      HttpSessionListener
    
    
    
      HttpSessionEvent
    
  
  
  
    
      HttpSessionActivationListener
    
  
  
  
    
      HttpSessionAttributeListener
    
    
    
      HttpSessionBindingEvent
    
  
  
  
    
      HttpSessionBindingListener
    
  
  
  
    
      ServletRequestListener
    
    
    
      ServletRequestEvent
    
  
  
  
    
      ServletRequestAttributeListener
    
    
    
      ServletRequestAttributeEvent
    
  


分别介绍: 

**１.ServletContextListener**

[接口方法] contextInitialized(), contextDestroyed()

[接收事件] ServletContextEvent

[触发场景] 在Container加载Web应用程序时 (例如启动 Container之后) ，会呼叫contextInitialized()，而当容器移除Web应用程序时，会呼叫contextDestroyed()方法。
  
**2. ServletContextAttributeListener**

[接口方法] attributeAdded()、 attributeReplaced()、attributeRemoved()

[接收事件] ServletContextAttributeEvent

[触发场景] 若有对象加入为application (ServletContext) 对象的属性，则会呼叫attributeAdded()，同理在置换属性与移除属性时，会分别呼叫attributeReplaced()、attributeRemoved()。
  
**3. HttpSessionListener**

[接口方法] sessionCreated(), sessionDestroyed ()

[接收事件] HttpSessionEvent

[触发场景] 在session  (HttpSession) 对象被创建或被消毁时，会分别调用这两个方法。
  
**4. HttpSessionAttributeListener**

[接口方法] attributeAdded()、 attributeReplaced()、attributeRemoved()

[接收事件] HttpSessionBindingEvent

[触发场景] 若有对象加入为session (HttpSession) 对象的属性，则会呼叫attributeAdded()，同理在置换属性与移除属性时，会分别呼叫attributeReplaced()、 attributeRemoved()。
  
**5. HttpSessionActivationListener**

[接口方法] sessionDidActivate(), sessionWillPassivate()

[接收事件] HttpSessionEvent

[触发场景] Activate与Passivate是用于置换对象的动作，当session对象为了资源利用或负载平衡等原因而必须暂时储存至硬盘或其它储存器时 (通过对象序列化) ，所作的动作称之为Passivate，而硬盘或储存器上的session对象重新加载JVM时所采的动作称之为Activate，所以容易理解的，sessionDidActivate()与 sessionWillPassivate()分别于Activeate后与将Passivate前呼叫。
  
**6. ServletRequestListener**

[接口方法] requestInitialized()与 requestDestroyed()

[接收事件] RequestEvent

[触发场景] 在request (HttpServletRequest) 对象被创建或被消毁时，会分别调用这两个方法。
  
**7. ServletRequestAttributeListener**

[接口方法] attributeAdded()、 attributeReplaced()、attributeRemoved()

[接收事件] HttpSessionBindingEvent

[触发场景] 若有对象加入为request (HttpServletRequest) 对象的属性，则会呼叫attributeAdded()，同理在置换属性与移除属性时，会分别呼叫attributeReplaced()、 attributeRemoved()。
  
**8. HttpSessionBindingListener**

[接口方法] valueBound()与valueUnbound()

[接收事件] HttpSessionBindingEvent

[触发场景] 实现HttpSessionBindingListener接口的类别，其实例如果被加入至session (HttpSession) 对象的属性中，则会呼叫 valueBound()，如果被从session (HttpSession) 对象的属性中移除，则会呼叫valueUnbound()，实现 HttpSessionBindingListener接口的类别不需在web.xml中设定。

具体使用方法: 在web.xml中添加如下语句: 

```xml
   

  
 com.servlet.listener.YouAchieveListener </listener-class>
  
</listener >
  
```

其中YouAchieveListener 为你实现的某个Listener接口的实现类com.servlet.listener.为你的包名。

```java

import javax.servlet.ServletContextListener;
  
import javax.servlet.*;

public class TigerListen implements ServletContextListener {
   
public void contextInitialized(ServletContextEvent sce) {
   
System.out.print("context listener.context initialized....Init");
   
}

public void contextDestroyed(ServletContextEvent sce) {
   
System.out.print("context listener.context initialized....Destroved");
   
}
  
}

```
  
```xml


   
com.wiloon.servlet.listener.TigerListen</listener-class>
   
</listener>

```

##