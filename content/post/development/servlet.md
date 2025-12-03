---
title: Servlet
author: "-"
date: 2011-10-16T07:17:29+00:00
url: /?p=1048
categories:
  - Java
tags:
  - Java
  - Servlet

---
## Servlet

      servlet的由来
  
自从计算机软件开发进入网络时代，就开始涉及到通讯问题。在客户/服务器 (C/S) 时期，每个软件都有自己的客户端和服务器端软件。并且客户端和服务器端之间的通讯协议差别也很大。后来随着互联网的发展，基于浏览器/服务器(B/S)的应用逐渐成为主流，通讯协议也统一到HTTP协议。但是，在HTTP协议之上，如何处理来自客户端的请求信息，以及如何对请求进行回应，则经历了很长时间也没有统一下来。目前，对于这个问题的解决方案主要有两种，一个是CGI，另一个是Servlet。

servlet是在服务器上运行的小程序。这个词是在Java applet的环境中创造的，Java applet是一种当作单独文件跟网页一起发送的小程序，它通常用于在客户端运行，结果得到为用户进行运算或者根据用户互作用定位图形等服务。服务器上需要一些程序，常常是根据用户输入访问数据库的程序。这些通常是使用公共网关接口 (CGI(Common Gateway Interface)) 应用程序完成的。然而，在服务器上运行Java，这种程序可使用Java编程语言实现。在通信量大的服务器上，servlet的优点在于它们的执行速度更快于CGI程序。各个用户请求被激活成单个程序中的一个线程，而无需创建单独的进程，这意味着服务器端处理请求的系统开销将明显降低。最早支持Servlet技术的是JavaSoft的Java Web Server。此后，一些其它的基于Java的WebServer开始支持标准的ServletAPI。

Servlet最初是在1995年由James Gosling 提出的，因为使用该技术需要复杂的Web服务器支持，所以当时并没有得到重视，也就放弃了。后来随着Web应用复杂度的提升，并要求提供更高的并发处理能力，Servlet被重新捡起，并在Java平台上得到实现，现在提起Servlet，指的都是Java Servlet。Java Servlet要求必须运行在Web服务器当中，与Web服务器之间属于分工和互补关系。确切的说，在实际运行的时候Java Servlet与Web服务器会融为一体，如同一个程序一样运行在同一个Java虚拟机 (JVM) 当中。与CGI不同的是，Servlet对每个请求都是单独启动一个线程，而不是进程。这种处理方式大幅度地降低了系统里的进程数量，提高了系统的并发处理能力。另外因为Java Servlet是运行在虚拟机之上的，也就解决了跨平台问题。

在Servlet出现之后，随着使用范围的扩大，人们发现了它的一个很大的一个弊端。那就是为了能够输出HTML格式内容，需要编写大量重复代码，造成不必要的重复劳动。为了解决这个问题，基于Servlet技术产生了Java Server Pages (JSP) 。 Servlet和JSP两者分工协作，Servlet侧重于解决运算和业务逻辑问题，JSP则侧重于解决展示问题。Servlet与JSP一起为Web应用开发带来了巨大的贡献，后来出现的众多Java Web应用开发框架都是基于这两种技术的，更确切的说，都是基于Servlet技术的。

Servlet与Web容器之间的关系

Java是一种动态加载和运行的语言。也就是说当应用程序持有一个类的地址 (CLASSPATH) 和名称 (包名和类名) 的情况下，可以在程序运行期间任何时候加载这个类，并创建和使用该类的对象。Servlet就是基于这个机制与Web容器融合在一起的。目前已知的所有支持Java Servlet的Web容器都是采用Java开发的。当Web容器接收到来自客户端的请求信息之后，会根据URL中的Web元件地址信息到Servlet队列中查找对应的Servlet对象，如果找到则直接使用，如果没有找到则加载对应的类，并创建对象。也就是说，Servlet对象是在第一次被使用的时候才创建的，并且一旦创建就会被反复使用，不再创建新的对象。所有创建出的Servlet对象会在Web服务器停止运行的时候统一进行垃圾回收。

为了解决客户端请求地址与 Servlet之间对应关系问题，Web容器需要一个用来描述这种对应关系的文件，一般是web.xml文件。如果一个Web应用程序中存在很多个Servlet，那么web.xml会变得非常庞大。在Servlet 3.0规范推出之后，允许在Servlet代码中使用声明式语法(annotation)来代替web.xml中的描述信息，这才让web.xml瘦身下来.

Servlet是一种服务器端的Java应用程序，具有独立于平台和协议的特性,可以生成动态的Web页面。 它担当客户请求 (Web浏览器或其他HTTP客户程序) 与服务器响应 (HTTP服务器上的数据库或应用程序) 的中间层。 Servlet是位于Web 服务器内部的服务器端的Java应用程序，与传统的从命令行启动的Java应用程序不同，Servlet由Web服务器进行加载，该Web服务器必须包含支持Servlet的Java虚拟机。

Servlet的主要功能在于交互式地浏览和修改数据，生成动态Web内容。这个过程为:

客户端发送请求至服务器端；
 服务器将请求信息发送至Servlet ；
 Servlet生成响应内容并将其传给Server。响应内容动态生成，通常取决于客户端的请求；
 服务器将响应返回给客户端；
 Servlet看起来像是通常的Java程序。Servlet导入特定的属于Java ServletAPI的包。因为是对象字节码，可动态地从网络加载，可以说Servlet对Server就如同Applet对Client一样，但是，由于Servlet运行于Server中，它们并不需要一个图形用户界面。从这个角度讲，Servlet也被称为FacelessObject。
 一个servlet就是Java编程语言中的一个类，它被用来扩展服务器的性能，服务器上驻留着可以通过"请求-响应"编程模型来访问的应用程序。虽然servlet可以对任何类型的请求产生响应，但通常只用来扩展Web服务器的应用程序。
 目前最新版本为3.0草案命名:  Server + Applet =Servlet 意为服务器端的小程序  
  
Servlet生命周期
    装载Servlet。这项操作一般是动态执行的。然而，Server通常会提供一个管理的选项，用于在Server启动时强制装载和初始化特定的Servlet。
 Server创建一个Servlet的实例
 Server调用Servlet的init()方法
 一个客户端的请求到达Server
 Server创建一个请求对象
 Server创建一个响应对象
 Server激活Servlet的service()方法，传递请求和响应对象作为参数
 service()方法获得关于请求对象的信息，处理请求，访问其他资源，获得需要的信息
 service()方法使用响应对象的方法，将响应传回Server，最终到达客户端。service()方法可能激活其它方法以处理请求，如doGet()或doPost()或程序员自己开发的新的方法。
 对于更多的客户端请求，Server创建新的请求和响应对象，仍然激活此Servlet的service()方法，将这两个对象作为参数传递给它。如此重复以上的循环，但无需再次调用init()方法。一般Servlet只初始化一次(只有一个对象),当Server不再需要Servlet时(一般当Server关闭时)，Server调用Servlet的Destroy()方法。
  
    servlet的工作模式
  
  
  
    客户端发送请求至服务器
  
  
  
    服务器启动并调用Servlet，Servlet根据客户端请求生成响应内容并将其传给服务器
  
  
     服务器将响应返回客户端
  
  
    Servlet 与 Applet: 
  
  
    相似之处: 

* 它们不是独立的应用程序，没有main()方法。
* 它们不是由用户或程序员调用，而是由另外一个应用程序(容器)调用。
* 它们都有一个生存周期，包含init()和destroy()方法。
 不同:
* Applet具有图形界面(AWT)，与浏览器一起，在客户端运行。
* Servlet 则没有图形界面，运行在服务器端。
  
    与传统CGI的比较
  
Java Servlet 与 CGI(Common Gateway Interface 公共网关接口) 的比较:与传统的CGI和许多其他类似CGI的技术相比，Java Servlet具有更高的效率，更容易使用，功能更强大，具有更好的可移植性，更节省投资。在未来的技术发展过程中，Servlet有可能彻底取代CGI。 在传统的CGI中，每个请求都要启动一个新的进程，如果CGI程序本身的执行时间较短，启动进程所需要的开销很可能反而超过实际执行时间。而在Servlet中，每个请求由一个轻量级的Java线程处理(而不是重量级的操作系统进程)。在传统CGI中，如果有N个并发的对同一CGI程序的请求，则该CGI程序的代码在内存中重复装载了N次；而对于Servlet，处理请求的是N个线程，只需要一份Servlet类代码。在性能优化方面，Servlet也比CGI有着更多的选择。
  
    * 方便 
  
  
  
    Servlet提供了大量的实用工具例程，例如自动地解析和解码HTML表单数据、读取和设置HTTP头、处理Cookie、跟踪会话状态等。 
  
  
  
    * 功能强大
  
  
  
    在Servlet中，许多使用传统CGI程序很难完成的任务都可以轻松地完成。例如，Servlet能够直接和Web服务器交互，而普通的CGI程序不能。Servlet还能够在各个程序之间共享数据，使得数据库连接池之类的功能很容易实现。 
  
  
    * 可移植性好
 Servlet用Java编写，Servlet API具有完善的标准。因此，为IPlanet Enterprise Server写的Servlet无需任何实质上的改动即可移植到Apache、Microsoft IIS或者WebStar。几乎所有的主流服务器都直接或通过插件支持Servlet。
  
    * 节省投资 
 不仅有许多廉价甚至免费的Web服务器可供个人或小规模网站使用，而且对于现有的服务器，如果它不支持Servlet的话，要加上这部分功能也往往是免费的(或只需要极少的投资)。
  
    Java Servlet 与 JSP: 
  
  
    JavaServer Pages(JSP)是一种实现普通静态HTML和动态HTML混合编码的技术，JSP并没有增加任何本质上不能用Servlet实现的功能。但是，在JSP中编写静态HTML更加方便，不必再用println语句来输出每一行HTML代码。更重要的是，借助内容和外观的分离，页面制作中不同性质的任务可以方便地分开: 比如，由页面设计者进行HTML设计，同时留出供Servlet程序员插入动态内容的空间。
  
  
    Servlet各个版本升级后新增功能
  
  
    Servlet 2.2新增功能
  
  
    :引入了self-contained Web applications的概念。
  
  
    servlet 2.3 新增功能
  
  
    : 2000年10月推出
 Servlet API 2.3中最重大的改变是增加了filters
 Servlet 2.3增加了filters和filter chains的功能。引入了context和session listeners的概念，当context 或session被初始化或者被将要被释放的时候，和当向context或session中绑定属性或解除绑定的时候，可以对类进行监测。
  
    servlet 2.4 新增功能
  
  
    : 2003年11月推出 
  
  
    Servlet 2.4加入了几个引起关注的特性，没有特别突出的新内容，而是在推敲和阐明以前存在的一些特性上花费了更多的功夫,对一些不严谨的地方进行了校验。 
  
  
    Servlet 2.4增加了新的最低需求，监测request的新方法，处理response的新方法，新的国际化支持，RequestDispatcher的几个处理，新的request listener类，session的描述，和一个新的基于Schema的并拥有J2EE元素的发布描述符。这份文档规范全面而严格的进行了修订，除去了一些可能会影响到跨平台发布的模糊不清的因素。总而言之，这份规范增加了四个新类，七个新方法，一个新常量，不再推荐使用一个类。
 1、web.xml DTD改用了XML Schema;
 Servlet 2.3之前的版本使用DTD作为部署描述文件的定义，其web.xml的格式为如下所示:
 <?xml version="1.0" encoding="IS0-8859-1"?>
 <!DOCTYPE web-app
 PUBLIC "-//sunMicrosystems,Inc.//DTD WebApplication 2.3f//EN"
 "http://java.sun.com/j2ee/dtds/web-app_2.3.dtd">
 <web-app>
 </web-app>
 Servlet 2.4版首次使用XML Schema定义作为部署描述文件，这样Web容器更容易校验web.xml语法。同时XML Schema提供了更好的扩充性，其web.xml中的格式如下所示:
 <?xml version="1.0" encoding="UTF-8"?>
 <web-app version="2.4" xmlns=http://java.sun.com/xml/ns/j2ee
 xmlns:workflow=http://www.workflow.com
 xmins:xsi="http://www.w3.org/2001/XMLSchema-instance"        xsi:schemaLocation="http://java.sun.com/xml/ns/j2ee
 http://java.sun.com/xml/ns/j2ee/web-app_2_4.xsd">
  
    .........
  
  
    </web-app>
 注意: 改为Schema后主要加强了两项功能:
 (1) 元素不依照顺序设定
 (2) 更强大的验证机制
 主要体现在:
 a.检查元素的值是否为合法的值
 b.检查元素的值是否为合法的文字字符或者数字字符
 c.检查Servlet,Filter,EJB-ref等等元素的名称是否唯一
 2.新增Filter四种设定: REQUEST、FORWARD、INCLUDE和ERROR。
 3.新增Request Listener、Event和Request Attribute Listener、Event。
 4.取消SingleThreadModel接口。当Servlet实现SingleThreadModel接口时，它能确保同时间内，只能有一个thread执行此Servlet。
 5.<welcome-file-list>可以为Servlet。
 6.ServletRequest接口新增一些方法。
 public String getLocalName()
 public String getLocalAddr()
 public int getLocalPort()
 public int getRemotePort()
  
    Servlet 2.5的新特征
 2005年9月发布Servlet 2.5
  
    Servlet2.5一些变化的介绍: 

 1) 基于最新的J2SE 5.0开发的。
 2) 支持annotations 。
 3) web.xml中的几处配置更加方便。
 4) 去除了少数的限制。
 5) 优化了一些实例
 servlet的各个版本对监听器的变化有:
 (1)servlet2.2和jsp1.1
 新增Listener:HttpSessionBindingListener
 新增Event: HttpSessionBindingEvent
 (2)servlet2.3和jsp1.2
 新增Listener:ServletContextListener,ServletContextAttributeListener
 ,HttpSessionListener,HttpSessionActivationListener,HttpSessionAttributeListener
 新增Event: ServletContextEvent,ServletContextAttributeEvent,HttpSessionEvent
 (3)servlet2.4和jsp2.0
 新增Listener:ServletRequestListener,ServletRequestAttribureListener
 新增Event: ServletRequestEvent,ServletRequestAttributeEvent
  
    HTTPServlet应用编程接口
  
    HTTP Servlet 使用一个 HTML 表单来发送和接收数据。要创建一个 HTTP Servlet，请扩展 HttpServlet 类， 该类是用专门的方法来处理 HTML 表单的 GenericServlet 的一个子类。 HTML 表单是由 <FORM> 和 </FORM> 标记定义的。表单中典型地包含输入字段(如文本输入字段、复选框、单选按钮和选择列表)和用于提交数据的按钮。当提交信息时，它们还指定服务器应执行哪一个Servlet(或其它的程序)。 HttpServlet 类包含 init()、destroy()、service() 等方法。其中 init() 和 destroy() 方法是继承的。
 (1) init() 方法
 在 Servlet 的生命期中，仅执行一次 init() 方法。它是在服务器装入 Servlet 时执行的。 可以配置服务器，以在启动服务器或客户机首次访问 Servlet 时装入 Servlet。 无论有多少客户机访问 Servlet，都不会重复执行 init() 。
 缺省的 init() 方法通常是符合要求的，但也可以用定制 init() 方法来覆盖它，典型的是管理服务器端资源。 例如，可能编写一个定制 init() 来只用于一次装入 GIF 图像，改进 Servlet 返回 GIF 图像和含有多个客户机请求的性能。另一个示例是初始化数据库连接。缺省的 init() 方法设置了 Servlet 的初始化参数，并用它的 ServletConfig 对象参数来启动配置， 因此所有覆盖 init() 方法的 Servlet 应调用 super.init() 以确保仍然执行这些任务。在调用 service() 方法之前，应确保已完成了 init() 方法。
 (2) service() 方法
 service() 方法是 Servlet 的核心。每当一个客户请求一个HttpServlet 对象，该对象的service() 方法就要被调用，而且传递给这个方法一个"请求"(ServletRequest)对象和一个"响应"(ServletResponse)对象作为参数。 在 HttpServlet 中已存在 service() 方法。缺省的服务功能是调用与 HTTP 请求的方法相应的 do 功能。例如， 如果 HTTP 请求方法为 GET，则缺省情况下就调用 doGet() 。Servlet 应该为 Servlet 支持的 HTTP 方法覆盖 do 功能。因为 HttpServlet.service() 方法会检查请求方法是否调用了适当的处理方法，不必要覆盖 service() 方法。只需覆盖相应的 do 方法就可以了。
 Servlet的响应可以是下列几种类型:
 一个输出流，浏览器根据它的内容类型(如text/HTML)进行解释。
 一个HTTP错误响应, 重定向到另一个URL、servlet、JSP。
 (3)doGet()方法
 当一个客户通过HTML 表单发出一个HTTP GET请求或直接请求一个URL时，doGet()方法被调用。与GET请求相关的参数添加到URL的后面，并与这个请求一起发送。当不会修改服务器端的数据时，应该使用doGet()方法。
 (4)doPost()方法
 当一个客户通过HTML 表单发出一个HTTP POST请求时，doPost()方法被调用。与POST请求相关的参数作为一个单独的HTTP 请求从浏览器发送到服务器。当需要修改服务器端的数据时，应该使用doPost()方法。
 (5) destroy() 方法
 destroy() 方法仅执行一次，即在服务器停止且卸载Servlet 时执行该方法。典型的，将 Servlet 作为服务器进程的一部分来关闭。缺省的 destroy() 方法通常是符合要求的，但也可以覆盖它，典型的是管理服务器端资源。例如，如果 Servlet 在运行时会累计统计数据，则可以编写一个 destroy() 方法，该方法用于在未装入 Servlet 时将统计数字保存在文件中。另一个示例是关闭数据库连接。
 当服务器卸装 Servlet 时，将在所有 service() 方法调用完成后，或在指定的时间间隔过后调用 destroy() 方法。一个Servlet 在运行service() 方法时可能会产生其它的线程，因此请确认在调用 destroy() 方法时，这些线程已终止或完成。
 (6) GetServletConfig()方法
 GetServletConfig()方法返回一个 ServletConfig 对象，该对象用来返回初始化参数和ServletContext。ServletContext 接口提供有关servlet 的环境信息。
 (7) GetServletInfo()方法
 GetServletInfo()方法是一个可选的方法，它提供有关servlet 的信息，如作者、版本、版权。
 当服务器调用sevlet 的Service()、doGet()和doPost()这三个方法时，均需要 "请求"和"响应"对象作为参数。"请求"对象提供有关请求的信息，而"响应"对象提供了一个将响应信息返回给浏览器的一个通信途径。
 javax.servlet 软件包中的相关类为ServletResponse和ServletRequest，而javax.servlet.http 软件包中的相关类为HttpServletRequest 和 HttpServletResponse。Servlet 通过这些对象与服务器通信并最终与客户机通信。Servlet 能通过调用"请求"对象的方法获知客户机环境，服务器环境的信息和所有由客户机提供的信息。Servlet 可以调用"响应"对象的方法发送响应，该响应是准备发回客户机的。
  
    Servlet和JSP规范版本对应关系:
  
         Servlet规范版本
      
      
      
         JSP版本
      
      
      
         JSF版本
      
      
      
         JAVA EE版本
      
    
    
    
      
         Servlet2.3
      
      
      
         JSP1.2、JSP1.1
      
      
      
      
      
      
         J2EE1.3
      
    
    
    
      
         Servlet2.4
      
      
      
         JSP2.0
      
      
      
         JSF1.1
      
      
      
         J2EE1.4
      
    
    
    
      
         Servlet2.5
      
      
      
         JSP2.1
      
      
      
         JSF1.2、JSF2.0
      
      
      
         Java EE5
      
    
    
    
      
         Servlet3.0
      
      
      
         JSP2.2
      
      
      
      
      
      
         Java EE6
      
    
  
  
  
    
      
        Servlet 3.0
      
      
      
        December 2009
      
      
      
        JavaEE 6, JavaSE 6
      
      
      
        Pluggability, Ease of development, Async Servlet, Security, File Uploading
      
    
    
    
      
        Servlet 2.5
      
      
      
        September 2005
      
      
      
        JavaEE 5, JavaSE 5
      
      
      
        Requires JavaSE 5, supports annotations
      
    
    
    
      
        Servlet 2.4
      
      
      
        November 2003
      
      
      
        J2EE 1.4, J2SE 1.3
      
      
      
        web.xml
      
    
    
    
      
        Servlet 2.1
      
      
      
        November 1998
      
      
      
        Unspecified
      
      
      
        First official specification, added RequestDispatcher, ServletContext
      
    
    
    
      
        Servlet 2.0
      
      
      
      
      
      
        JDK 1.1
      
      
      
        Part of Java Servlet Development Kit 2.0
      
    
    
    
      
        Servlet 1.0
      
      
      
        June 1997
      
      
      
        undefined

    [http://www.admin10000.com/document/208.html](http://www.admin10000.com/document/208.html)
  
    [http://quqtalk.iteye.com/blog/819451](http://quqtalk.iteye.com/blog/819451)
  