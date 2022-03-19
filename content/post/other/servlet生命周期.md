---
title: Servlet生命周期
author: "-"
date: 2011-10-30T08:25:36+00:00
url: /?p=1398
categories:
  - Java
tags:
  - Servlet

---
## Servlet生命周期
Servlet运行在Servlet容器中，其生命周期由容器来管理。Servlet的生命周期通过javax.servlet.Servlet接口中的init()、service()和destroy()方法来表示。

Servlet的生命周期包含了下面4个阶段: 

 (1) 加载和实例化

Servlet容器负责加载和实例化Servlet。当Servlet容器启动时，或者在容器检测到需要这个Servlet来响应第一个请求时，创建Servlet实例。当Servlet容器启动后，它必须要知道所需的Servlet类在什么位置，Servlet容器可以从本地文件系统、远程文件系统或者其他的网络服务中通过类加载器加载Servlet类，成功加载后，容器创建Servlet的实例。因为容器是通过Java的反射API来创建Servlet实例，调用的是Servlet的默认构造方法 (即不带参数的构造方法) ，所以我们在编写Servlet类的时候，不应该提供带参数的构造方法。

 (2) 初始化

在Servlet实例化之后，容器将调用Servlet的init()方法初始化这个对象。初始化的目的是为了让Servlet对象在处理客户端请求前完成一些初始化的工作，如建立数据库的连接，获取配置信息等。对于每一个Servlet实例，init()方法只被调用一次。在初始化期间，Servlet实例可以使用容器为它准备的ServletConfig对象从Web应用程序的配置信息 (在web.xml中配置) 中获取初始化的参数信息。在初始化期间，如果发生错误，Servlet实例可以抛出ServletException异常或者UnavailableException异常来通知容器。ServletException异常用于指明一般的初始化失败，例如没有找到初始化参数；而UnavailableException异常用于通知容器该Servlet实例不可用。例如，数据库服务器没有启动，数据库连接无法建立，Servlet就可以抛出UnavailableException异常向容器指出它暂时或永久不可用。

 (3) 请求处理

Servlet容器调用Servlet的service()方法对请求进行处理。要注意的是，在service()方法调用之前，init()方法必须成功执行。在service()方法中，Servlet实例通过ServletRequest对象得到客户端的相关信息和请求信息，在对请求进行处理后，调用ServletResponse对象的方法设置响应信息。在service()方法执行期间，如果发生错误，Servlet实例可以抛出ServletException异常或者UnavailableException异常。如果UnavailableException异常指示了该实例永久不可用，Servlet容器将调用实例的destroy()方法，释放该实例。此后对该实例的任何请求，都将收到容器发送的HTTP 404 (请求的资源不可用) 响应。如果UnavailableException异常指示了该实例暂时不可用，那么在暂时不可用的时间段内，对该实例的任何请求，都将收到容器发送的HTTP 503 (服务器暂时忙，不能处理请求) 响应。

 (4) 服务终止

当容器检测到一个Servlet实例应该从服务中被移除的时候，容器就会调用实例的destroy()方法，以便让该实例可以释放它所使用的资源，保存数据到持久存储设备中。当需要释放内存或者容器关闭时，容器就会调用Servlet实例的destroy()方法。在destroy()方法调用之后，容器会释放这个Servlet实例，该实例随后会被Java的垃圾收集器所回收。如果再次需要这个Servlet处理请求，Servlet容器会创建一个新的Servlet实例。

在整个Servlet的生命周期过程中，创建Servlet实例、调用实例的init()和destroy()方法都只进行一次，当初始化完成后，Servlet容器会将该实例保存在内存中，通过调用它的service()方法，为接收到的请求服务。下面给出Servlet整个生命周期过程的UML序列图，
  

  
如果需要让Servlet容器在启动时即加载Servlet，可以在web.xml文件中配置元素。

>https://skydrive.live.com/embed?cid=37BA55E5B510EC35&resid=37BA55E5B510EC35%21107&authkey=AFYH6_pw58KDkUM