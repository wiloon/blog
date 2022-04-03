---
title: web.xml
author: "-"
date: 2012-06-10T03:23:19+00:00
url: /?p=3459
categories:
  - Java
  - Web
tags:
  - JavaEE
  - Servlet

---
## web.xml
web.xml template

servlet 2.5

```xml
  
<?xml version="1.0" encoding="UTF-8"?>

<web-app xmlns="http://java.sun.com/xml/ns/javaee"
  
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  
xsi:schemaLocation="http://java.sun.com/xml/ns/javaee http://java.sun.com/xml/ns/javaee/web-app_2_5.xsd"
  
version="2.5">

```

web.xml 3.0: http://www.wiloon.com/?p=3484

```xml

<?xml version="1.0" encoding="UTF-8"?>

<web-app
  
xmlns="http://xmlns.jcp.org/xml/ns/javaee"
  
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  
xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee http://xmlns.jcp.org/xml/ns/javaee/web-app_3_1.xsd"
  
version="3.1"
  
metadata-complete="false">

<display-name>Servlet 3.x Demo</display-name>

<description>A demo for servlet 3.x</description>

<servlet>
  
<servlet-name>HelloWorld</servlet-name>
  
<servlet-class>com.wiloon.test.servlet.HelloWorld</servlet-class>
  
</servlet>

<servlet-mapping>
  
<servlet-name>HelloWorld</servlet-name>
  
<url-pattern>/servlet/HelloWorld</url-pattern>
  
</servlet-mapping>

</web-app>

```

web.xml是传统的部署描述文件。

servlet 3.x 中web.xml 变为可选配置.

Servlet规范中定义了web.xml文件，它是Web应用的配置文件，Web.xml文件是和Web容器无关的。通过Web.xml文件可以配置Servlet类和url的映射、欢迎列表、过滤器以及安全约束条件等。


  
    1 定义头和根元素
  
  
    部署描述符文件就像所有XML文件一样，必须以一个XML头开始。这个头声明可以使用的XML版本并给出文件的字符编码. 
  
  
    
      
        ```xml
 <?xml version="1.0" encoding="UTF-8"?>
 ```
      
    
    
    
      DOCYTPE声明必须立即出现在此头之后。(这个可以没有??)
    
    
    
      
        ```xml
 <!DOCTYPE web-app PUBLIC
 "-//Sun Microsystems, Inc.//DTD Web Application 2.3//EN"
 "http://java.sun.com/dtd/web-app_2_3.dtd" >
 ```
      
      
      
        这个声明告诉服务器适用的servlet规范的版本 (如2.2或2.3) 并指定管理此文件其余部分内容的语法的DTD(Document Type Definition，文档类型定义)。或者可以定义在webapp里,以下是servlet3.0的
      
      
      
        ```xml
 <?xml version="1.0" encoding="UTF-8"?>
      
      
      
        <web-app
 xmlns="http://xmlns.jcp.org/xml/ns/javaee"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee http://xmlns.jcp.org/xml/ns/javaee/web-app_3_1.xsd"
 version="3.1"
 metadata-complete="true">
 ...
 </web-app>
 ```
      
  
  
  
    
      所有部署描述符文件的顶层 (根) 元素为web-app。请注意，XML元素不像HTML，他们是大小写敏感的。因此，web-App和WEB-APP都是不合法的，web-app必须用小写。
    
    
    
      metadata-complete 属性，该属性指定当前的部署描述文件是否是完全的。如果设置为 true，则容器在部署时将只依赖部署描述文件，忽略所有的注解 (同时也会跳过 web-fragment.xml 的扫描，亦即禁用可插性支持，具体请看后文关于 可插性支持的讲解) ；如果不配置该属性，或者将其设置为 false，则表示启用注解支持 (和可插性支持) 。
    
    
    
      2 部署描述符文件内的元素次序
    
    
    
             XML元素不仅是大小写敏感的，而且它们还对出现在其他元素中的次序敏感。例如，XML头必须是文件中的第一项，DOCTYPE声明必须是第二项，而web-app元素必须是第三项。在web-app元素内，元素的次序也很重要。服务器不一定强制要求这种次序，但它们允许 (实际上有些服务器就是这样做的) 完全拒绝执行含有次序不正确的元素的Web应用。这表示使用非标准元素次序的web.xml文件是不可移植的。
    
    
    
            下面的列表给出了所有可直接出现在web-app元素内的合法元素所必需的次序。例如，此列表说明servlet元素必须出现在所有servlet-mapping元素之前。请注意，所有这些元素都是可选的。因此，可以省略掉某一元素，但不能把它放于不正确的位置。 icon: icon元素指出IDE和GUI工具用来表示Web应用的一个和两个图像文件的位置。
    
    
    
      display-name: 
    
    
    
      display-name元素提供GUI工具可能会用来标记这个特定的Web应用的一个名称。如果使用工具编辑部署描述符，display-name元素包含的就是XML编辑器显示的名称。
    
    
    
       description:
    
    
    
      description元素给出与此有关的说明性文本。
    
    
    
      
 context-param:
    
    
    
      context-param元素声明应用范围内的初始化参数。
    
    
    
      
 filter: 
    
    
    
      过滤器元素将一个名字与一个实现javax.servlet.Filter接口的类相关联。
    
    
    
      
 filter-mapping: 
    
    
    
      一旦命名了一个过滤器，就要利用filter-mapping元素把它与一个或多个servlet或JSP页面相关联。
    
    
    
      
 listener: 
    
    
    
      servlet API的版本2.3增加了对事件监听程序的支持，事件监听程序在建立、修改和删除会话或servlet环境时得到通知。Listener元素指出事件监听程序类。
    
    
    
      
 servlet: 
    
    
    
      在向servlet或JSP页面制定初始化参数或定制URL时，必须首先命名servlet或JSP页面。Servlet元素就是用来完成此项任务的。
    
    
    
      
 servlet-mapping: 
    
    
    
      服务器一般为servlet提供一个缺省的URL: http://host/webAppPrefix/servlet/ServletName。但是，常常会更改这个URL，以便servlet可以访问初始化参数或更容易地处理相对URL。在更改缺省URL时，使用servlet-mapping元素。
    
    
    
      
 session-config: 
    
    
    
      如果某个会话在一定时间内未被访问，服务器可以抛弃它以节省内存。可通过使用HttpSession的setMaxInactiveInterval方法明确设置单个会话对象的超时值，或者可利用session-config元素制定缺省超时值。
    
    
    
      
 mime-mapping: 
    
    
    
      如果Web应用有特殊的文件，希望能保证给他们分配特定的MIME类型，则mime-mapping元素提供这种保证。
    
    
    
      
 welcom-file-list: 
    
    
    
      welcome-file-list元素指示服务器在收到引用一个目录名而不是文件名的URL时，使用哪个文件。
    
    
    
      
 error-page: 
    
    
    
      error-page元素使得在返回特定HTTP状态代码时，或者特定类型的异常被抛出时，能够制定将要显示的页面。
    
    
    
      
 taglib: 
    
    
    
      taglib元素对标记库描述符文件 (Tag Libraryu Descriptor file) 指定别名。此功能使你能够更改TLD文件的位置，而不用编辑使用这些文件的JSP页面。
    
    
    
      
 resource-env-ref: resource-env-ref元素声明与资源相关的一个管理对象。
 resource-ref: resource-ref元素声明一个资源工厂使用的外部资源。
 security-constraint: security-constraint元素制定应该保护的URL。它与login-config元素联合使用
 login-config: 用login-config元素来指定服务器应该怎样给试图访问受保护页面的用户授权。它与sercurity-constraint元素联合使用。
 security-role: security-role元素给出安全角色的一个列表，这些角色将出现在servlet元素内的security-role-ref元素的role-name子元素中。分别地声明角色可使高级IDE处理安全信息更为容易。
 env-entry: env-entry元素声明Web应用的环境项。
 ejb-ref: ejb-ref元素声明一个EJB的主目录的引用。
 ejb-local-ref: ejb-local-ref元素声明一个EJB的本地主目录的应用。
    
    
    
            3 分配名称和定制的URL
    
    
    
            在web.xml中完成的一个最常见的任务是对servlet或JSP页面给出名称和定制的URL。用servlet元素分配名称，使用servlet-mapping元素将定制的URL与刚分配的名称相关联。
    
    
    
            3.1 分配名称
    
    
    
            为了提供初始化参数，对servlet或JSP页面定义一个定制URL或分配一个安全角色，必须首先给servlet或JSP页面一个名称。可通过servlet元素分配一个名称。最常见的格式包括servlet-name和servlet-class子元素 (在web-app元素内) ，如下所示: 
    
    
    
      <servlet>
 <servlet-name>Test</servlet-name>
 <servlet-class>moreservlets.TestServlet</servlet-class>
 </servlet>
    
    
    
            这表示位于WEB-INF/classes/moreservlets/TestServlet的servlet已经得到了注册名Test。给servlet一个名称具有两个主要的含义。首先，初始化参数、定制的URL模式以及其他定制通过此注册名而不是类名引用此servlet。其次,可在URL而不是类名中使用此名称。因此，利用刚才给出的定义，URL http://host/webAppPrefix/servlet/Test 可用于 http://host/webAppPrefix/servlet/moreservlets.TestServlet 的场所。
    
    
    
      请记住: XML元素不仅是大小写敏感的，而且定义它们的次序也很重要。例如，web-app元素内所有servlet元素必须位于所有servlet-mapping元素 (下一小节介绍) 之前，而且还要位于5.6节和5.11节讨论的与过滤器或文档相关的元素 (如果有的话) 之前。类似地，servlet的servlet-name子元素也必须出现在servlet-class之前。5.2节"部署描述符文件内的元素次序"将详细介绍这种必需的次序。      例如，程序清单5-1给出了一个名为TestServlet的简单servlet，它驻留在moreservlets程序包中。因为此servlet是扎根在一个名为deployDemo的目录中的Web应用的组成部分，所以TestServlet.class放在deployDemo/WEB-INF/classes/moreservlets中。程序清单5-2给出将放置在deployDemo/WEB-INF/内的web.xml文件的一部分。此web.xml文件使用servlet-name和servlet-class元素将名称Test与TestServlet.class相关联。图5-1和图5-2分别显示利用缺省URL和注册名调用TestServlet时的结果。程序清单5-1 TestServlet.java
 package moreservlets;
    
    
    
      import java.io.*;
 import javax.servlet.*;
 import javax.servlet.http.*;
    
    
    
      /** Simple servlet used to illustrate servlet naming
 * and custom URLs.
 * 
 * Taken from More Servlets and JavaServer Pages
 * from Prentice Hall and Sun Microsystems Press,
 * http://www.moreservlets.com/.
 * © 2002 Marty Hall; may be freely used or adapted.
 */
    
    
    
      public class TestServlet extends HttpServlet {
 public void doGet(HttpServletRequest request,
 HttpServletResponse response)
 throws ServletException, IOException {
 response.setContentType("text/html");
 PrintWriter out = response.getWriter();
 String uri = request.getRequestURI();
 out.println(ServletUtilities.headWithTitle("Test Servlet") +
 "<BODY BGCOLOR=/"#FDF5E6/">/n" +
 "URI: " + uri + "/n" +
 "</BODY></HTML>");
 }
 }
    
    
    
      程序清单5-2 web.xml (说明servlet名称的摘录) 
 <?xml version="1.0" encoding="ISO-8859-1"?>
 <!DOCTYPE web-app
 PUBLIC "-//Sun Microsystems, Inc.//DTD Web Application 2.3//EN"
 "http://java.sun.com/dtd/web-app_2_3.dtd">
    
    
    
      <web-app>
 <!- … ->
 <servlet>
 <servlet-name>Test</servlet-name>
 <servlet-class>moreservlets.TestServlet</servlet-class>
 </servlet>
 <!- … ->
 </web-app>
    
    
    
      3.2 定义定制的URL
    
    
    
      大多数服务器具有一个缺省的serlvet URL: 
 http://host/webAppPrefix/servlet/packageName.ServletName。虽然在开发中使用这个URL很方便，但是我们常常会希望另一个URL用于部署。例如，可能会需要一个出现在Web应用顶层的URL (如，http://host/webAppPrefix/Anyname) ，并且在此URL中没有servlet项。位于顶层的URL简化了相对URL的使用。此外，对许多开发人员来说，顶层URL看上去比更长更麻烦的缺省URL更简短。
    
    
    
      事实上，有时需要使用定制的URL。比如，你可能想关闭缺省URL映射，以便更好地强制实施安全限制或防止用户意外地访问无初始化参数的servlet。如果你禁止了缺省的URL，那么你怎样访问servlet呢？这时只有使用定制的URL了。       为了分配一个定制的URL，可使用servlet-mapping元素及其servlet-name和url-pattern子元素。Servlet-name元素提供了一个任意名称，可利用此名称引用相应的servlet；url-pattern描述了相对于Web应用的根目录的URL。url-pattern元素的值必须以斜杠 (/) 起始。下面给出一个简单的web.xml摘录，它允许使用URL http://host/webAppPrefix/UrlTest而不是http://host/webAppPrefix/servlet/Test或
 http://host/webAppPrefix/servlet/moreservlets.TestServlet。请注意，仍然需要XML头、DOCTYPE声明以及web-app封闭元素。此外，可回忆一下，XML元素出现地次序不是随意的。特别是，需要把所有servlet元素放在所有servlet-mapping元素之前。<servlet>
 <servlet-name>Test</servlet-name>
 <servlet-class>moreservlets.TestServlet</servlet-class>
 </servlet>
 <!- ... ->
 <servlet-mapping>
 <servlet-name>Test</servlet-name>
 <url-pattern>/UrlTest</url-pattern>
 </servlet-mapping>URL模式还可以包含通配符。例如，下面的小程序指示服务器发送所有以Web应用的URL前缀开始，以..asp结束的请求到名为BashMS的servlet。<servlet>
 <servlet-name>BashMS</servlet-name>
 <servlet-class>msUtils.ASPTranslator</servlet-class>
 </servlet>
 <!- ... ->
 <servlet-mapping>
 <servlet-name>BashMS</servlet-name>
 <url-pattern>/*.asp</url-pattern>
 </servlet-mapping>3.3 命名JSP页面因为JSP页面要转换成sevlet，自然希望就像命名servlet一样命名JSP页面。毕竟，JSP页面可能会从初始化参数、安全设置或定制的URL中受益，正如普通的serlvet那样。虽然JSP页面的后台实际上是servlet这句话是正确的，但存在一个关键的猜疑: 即，你不知道JSP页面的实际类名 (因为系统自己挑选这个名字) 。因此，为了命名JSP页面，可将jsp-file元素替换为servlet-calss元素，如下所示: <servlet>
 <servlet-name>Test</servlet-name>
 <jsp-file>/TestPage.jsp</jsp-file>
 </servlet>命名JSP页面的原因与命名servlet的原因完全相同: 即为了提供一个与定制设置 (如，初始化参数和安全设置) 一起使用的名称，并且，以便能更改激活JSP页面的URL (比方说，以便多个URL通过相同页面得以处理，或者从URL中去掉.jsp扩展名) 。但是，在设置初始化参数时，应该注意，JSP页面是利用jspInit方法，而不是init方法读取初始化参数的。例如，程序清单5-3给出一个名为TestPage.jsp的简单JSP页面，它的工作只是打印出用来激活它的URL的本地部分。TestPage.jsp放置在deployDemo应用的顶层。程序清单5-4给出了用来分配一个注册名PageName，然后将此注册名与http://host/webAppPrefix/UrlTest2/anything 形式的URL相关联的web.xml文件 (即，deployDemo/WEB-INF/web.xml) 的一部分。程序清单5-3 TestPage.jsp
 <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
 <HTML>
 <HEAD>
 <TITLE>
 JSP Test Page
 </TITLE>
 </HEAD>
 <BODY BGCOLOR="#FDF5E6">
 URI: <%= request.getRequestURI() %>
 </BODY>
 </HTML>程序清单5-4 web.xml (说明JSP页命名的摘录) 
 <?xml version="1.0" encoding="ISO-8859-1"?>
 <!DOCTYPE web-app
 PUBLIC "-//Sun Microsystems, Inc.//DTD Web Application 2.3//EN"
 "http://java.sun.com/dtd/web-app_2_3.dtd"><web-app>
 <!- ... ->
 <servlet>
 <servlet-name>PageName</servlet-name>
 <jsp-file>/TestPage.jsp</jsp-file>
 </servlet>
 <!- ... ->
 <servlet-mapping>
 <servlet-name> PageName </servlet-name>
 <url-pattern>/UrlTest2/*</url-pattern>
 </servlet-mapping>
 <!- ... ->
 </web-app> 
      
      
        4 禁止激活器servlet      对servlet或JSP页面建立定制URL的一个原因是，这样做可以注册从init (servlet) 或jspInit (JSP页面) 方法中读取得初始化参数。但是，初始化参数只在是利用定制URL模式或注册名访问servlet或JSP页面时可以使用，用缺省URL http://host/webAppPrefix/servlet/ServletName 访问时不能使用。因此，你可能会希望关闭缺省URL，这样就不会有人意外地调用初始化servlet了。这个过程有时称为禁止激活器servlet，因为多数服务器具有一个用缺省的servlet URL注册的标准servlet，并激活缺省的URL应用的实际servlet。有两种禁止此缺省URL的主要方法: 在每个Web应用中重新映射/servlet/模式。
 全局关闭激活器servlet。重要的是应该注意到，虽然重新映射每个Web应用中的/servlet/模式比彻底禁止激活servlet所做的工作更多，但重新映射可以用一种完全可移植的方式来完成。相反，全局禁止激活器servlet完全是针对具体机器的，事实上有的服务器 (如ServletExec) 没有这样的选择。下面的讨论对每个Web应用重新映射/servlet/ URL模式的策略。后面提供在Tomcat中全局禁止激活器servlet的详细内容。4.1 重新映射/servlet/URL模式在一个特定的Web应用中禁止以http://host/webAppPrefix/servlet/ 开始的URL的处理非常简单。所需做的事情就是建立一个错误消息servlet，并使用前一节讨论的url-pattern元素将所有匹配请求转向该servlet。只要简单地使用: <url-pattern>/servlet/*</url-pattern>作为servlet-mapping元素中的模式即可。例如，程序清单5-5给出了将SorryServlet servlet (程序清单5-6) 与所有以http://host/webAppPrefix/servlet/ 开头的URL相关联的部署描述符文件的一部分。程序清单5-5 web.xml (说明JSP页命名的摘录) 
 <?xml version="1.0" encoding="ISO-8859-1"?>
 <!DOCTYPE web-app
 PUBLIC "-//Sun Microsystems, Inc.//DTD Web Application 2.3//EN"
 "http://java.sun.com/dtd/web-app_2_3.dtd"><web-app>
 <!- ... ->
 <servlet>
 <servlet-name>Sorry</servlet-name>
 <servlet-class>moreservlets.SorryServlet</servlet-class>
 </servlet>
 <!- ... ->
 <servlet-mapping>
 <servlet-name> Sorry </servlet-name>
 <url-pattern>/servlet/*</url-pattern>
 </servlet-mapping>
 <!- ... ->
 </web-app>程序清单5-6 SorryServlet.java
 package moreservlets;import java.io.*;
 import javax.servlet.*;
 import javax.servlet.http.*;/** Simple servlet used to give error messages to
 * users who try to access default servlet URLs
 * (i.e., http://host/webAppPrefix/servlet/ServletName)
 * in Web applications that have disabled this
 * behavior.
 * 
 * Taken from More Servlets and JavaServer Pages
 * from Prentice Hall and Sun Microsystems Press,
 * http://www.moreservlets.com/.
 * © 2002 Marty Hall; may be freely used or adapted.
 */public class SorryServlet extends HttpServlet {
 public void doGet(HttpServletRequest request,
 HttpServletResponse response)
 throws ServletException, IOException {
 response.setContentType("text/html");
 PrintWriter out = response.getWriter();
 String title = "Invoker Servlet Disabled.";
 out.println(ServletUtilities.headWithTitle(title) +
 "<BODY BGCOLOR=/"#FDF5E6/">/n" +
 "" + title + "/n" +
 "Sorry, access to servlets by means of/n" +
 "URLs that begin with/n" +
 "http://host/webAppPrefix/servlet//n" +
 "has been disabled./n" +
 "</BODY></HTML>");
 }public void doPost(HttpServletRequest request,
 HttpServletResponse response)
 throws ServletException, IOException {
 doGet(request, response);
 }
 } 
        
        
          4.2 全局禁止激活器: Tomcat      Tomcat 4中用来关闭缺省URL的方法与Tomcat 3中所用的很不相同。下面介绍这两种方法: 1．禁止激活器:  Tomcat 4      Tomcat 4用与前面相同的方法关闭激活器servlet，即利用web.xml中的url-mapping元素进行关闭。不同之处在于Tomcat使用了放在install_dir/conf中的一个服务器专用的全局web.xml文件，而前面使用的是存放在每个Web应用的WEB-INF目录中的标准web.xml文件。因此，为了在Tomcat 4中关闭激活器servlet，只需在install_dir/conf/web.xml中简单地注释出/servlet/* URL映射项即可，如下所示: <!-
 <servlet-mapping>
 <servlet-name>invoker</servlet-name>
 <url-pattern>/servlet/*</url-pattern>
 </servlet-mapping>
 ->再次提醒，应该注意这个项是位于存放在install_dir/conf的Tomcat专用的web.xml文件中的，此文件不是存放在每个Web应用的WEB-INF目录中的标准web.xml。 2．禁止激活器: Tomcat3在Apache Tomcat的版本3中，通过在install_dir/conf/server.xml中注释出InvokerInterceptor项全局禁止缺省servlet URL。例如，下面是禁止使用缺省servlet URL的server.xml文件的一部分。<!-
 <RequsetInterceptor
 className="org.apache.tomcat.request.InvokerInterceptor"
 debug="0" prefix="/servlet/" />
 ->5 初始化和预装载servlet与JSP页面这里讨论控制servlet和JSP页面的启动行为的方法。特别是，说明了怎样分配初始化参数以及怎样更改服务器生存期中装载servlet和JSP页面的时刻。5.1 分配servlet初始化参数      利用init-param元素向servlet提供初始化参数，init-param元素具有param-name和param-value子元素。例如，在下面的例子中，如果initServlet servlet是利用它的注册名 (InitTest) 访问的，它将能够从其方法中调用getServletConfig().getInitParameter("param1")获得"Value 1"，调用getServletConfig().getInitParameter("param2")获得"2"。<servlet>
 <servlet-name>InitTest</servlet-name>
 <servlet-class>moreservlets.InitServlet</servlet-class>
 <init-param>
 <param-name>param1</param-name>
 <param-value>value1</param-value>
 </init-param>
 <init-param>
 <param-name>param2</param-name>
 <param-value>2</param-value>
 </init-param>
 </servlet>在涉及初始化参数时，有几点需要注意: 返回值。GetInitParameter的返回值总是一个String。因此，在前一个例子中，可对param2使用Integer.parseInt获得一个int。
 JSP中的初始化。JSP页面使用jspInit而不是init。JSP页面还需要使用jsp-file元素代替servlet-class。
 缺省URL。初始化参数只在通过它们的注册名或与它们注册名相关的定制URL模式访问Servlet时可以使用。因此，在这个例子中，param1和param2初始化参数将能够在使用URL http://host/webAppPrefix/servlet/InitTest 时可用，但在使用URL http://host/webAppPrefix/servlet/myPackage.InitServlet 时不能使用。
        
      
  
  
  
    web.xml 详解二
  
  
  
    例如，程序清单5-7给出一个名为InitServlet的简单servlet，它使用init方法设置firstName和emailAddress字段。程序清单5-8给出分配名称InitTest给servlet的web.xml文件。程序清单5-7 InitServlet.java
 package moreservlets;import java.io.*;
 import javax.servlet.*;
 import javax.servlet.http.*;/** Simple servlet used to illustrate servlet
 * initialization parameters.
 * 
 * Taken from More Servlets and JavaServer Pages
 * from Prentice Hall and Sun Microsystems Press,
 * http://www.moreservlets.com/.
 * © 2002 Marty Hall; may be freely used or adapted.
 */public class InitServlet extends HttpServlet {
 private String firstName, emailAddress;public void init() {
 ServletConfig config = getServletConfig();
 firstName = config.getInitParameter("firstName");
 emailAddress = config.getInitParameter("emailAddress");
 }public void doGet(HttpServletRequest request,
 HttpServletResponse response)
 throws ServletException, IOException {
 response.setContentType("text/html");
 PrintWriter out = response.getWriter();
 String uri = request.getRequestURI();
 out.println(ServletUtilities.headWithTitle("Init Servlet") +
 "<BODY BGCOLOR=/"#FDF5E6/">/n" +
 "Init Parameters:/n" +
 "/n" +
 "First name: " + firstName + "/n" +
 "Email address: " + emailAddress + "/n" +
 "/n" +
 "</BODY></HTML>");
 }
 }程序清单5-8 web.xml (说明初始化参数的摘录) 
 <?xml version="1.0" encoding="ISO-8859-1"?>
 <!DOCTYPE web-app
 PUBLIC "-//Sun Microsystems, Inc.//DTD Web Application 2.3//EN"
 "http://java.sun.com/dtd/web-app_2_3.dtd"><web-app>
 <!- ... ->
 <servlet>
 <servlet-name>InitTest</servlet-name>
 <servlet-class>moreservlets.InitServlet</servlet-class>
 <init-param>
 <param-name>firstName</param-name>
 <param-value>Larry</param-value>
 </init-param>
 <init-param>
 <param-name>emailAddress</param-name>
 <param-value>Ellison@Microsoft.com</param-value>
 </init-param>
 </servlet>
 <!- ... ->
 </web-app>5.2 分配JSP初始化参数      给JSP页面提供初始化参数在三个方面不同于给servlet提供初始化参数。1) 使用jsp-file而不是servlet-class。因此，WEB-INF/web.xml文件的servlet元素如下所示: <servlet>
 <servlet-name>PageName</servlet-name>
 <jsp-file>/RealPage.jsp</jsp-file>
 <init-param>
 <param-name>...</param-name>
 <param-value>...</param-value>
 </init-param>
 ...
 </servlet>2)几乎总是分配一个明确的URL模式。对servlet，一般相应地使用以http://host/webAppPrefix/servlet/ 开始的缺省URL。只需记住，使用注册名而不是原名称即可。这对于JSP页面在技术上也是合法的。例如，在上面给出的例子中，可用URL http://host/webAppPrefix/servlet/PageName 访问RealPage.jsp的对初始化参数具有访问权的版本。但在用于JSP页面时，许多用户似乎不喜欢应用常规的servlet的URL。此外，如果JSP页面位于服务器为其提供了目录清单的目录中 (如，一个既没有index.html也没有index.jsp文件的目录) ，则用户可能会连接到此JSP页面，单击它，从而意外地激活未初始化的页面。因此，好的办法是使用url-pattern (5.3节) 将JSP页面的原URL与注册的servlet名相关联。这样，客户机可使用JSP页面的普通名称，但仍然激活定制的版本。例如，给定来自项目1的servlet定义，可使用下面的servlet-mapping定义: <servlet-mapping>
 <servlet-name>PageName</servlet-name>
 <url-pattern>/RealPage.jsp</url-pattern>
 </servlet-mapping>3) JSP页使用jspInit而不是init。自动从JSP页面建立的servlet或许已经使用了inti方法。因此，使用JSP声明提供一个init方法是不合法的，必须制定jspInit方法。为了说明初始化JSP页面的过程，程序清单5-9给出了一个名为InitPage.jsp的JSP页面，它包含一个jspInit方法且放置于deployDemo Web应用层次结构的顶层。一般，http://host/deployDemo/InitPage.jsp 形式的URL将激活此页面的不具有初始化参数访问权的版本，从而将对firstName和emailAddress变量显示null。但是，web.xml文件 (程序清单5-10) 分配了一个注册名，然后将该注册名与URL模式/InitPage.jsp相关联。程序清单5-9 InitPage.jsp
 <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
 <HTML>
 <HEAD><TITLE>JSP Init Test</TITLE></HEAD>
 <BODY BGCOLOR="#FDF5E6">
 Init Parameters:
 
 First name: <%= firstName %>
 Email address: <%= emailAddress %>
 
 </BODY></HTML>
 <%!
 private String firstName, emailAddress;public void jspInit() {
 ServletConfig config = getServletConfig();
 firstName = config.getInitParameter("firstName");
 emailAddress = config.getInitParameter("emailAddress");
 }
 %>程序清单5-10 web.xml (说明JSP页面的init参数的摘录) 
 <?xml version="1.0" encoding="ISO-8859-1"?>
 <!DOCTYPE web-app
 PUBLIC "-//Sun Microsystems, Inc.//DTD Web Application 2.3//EN"
 "http://java.sun.com/dtd/web-app_2_3.dtd"><web-app>
 <!- ... ->
 <servlet>
 <servlet-name>InitPage</servlet-name>
 <jsp-file>/InitPage.jsp</jsp-file>
 <init-param>
 <param-name>firstName</param-name>
 <param-value>Bill</param-value>
 </init-param>
 <init-param>
 <param-name>emailAddress</param-name>
 <param-value>gates@oracle.com</param-value>
 </init-param>
 </servlet>
 <!- ... ->
 <servlet-mapping>
 <servlet-name> InitPage</servlet-name>
 <url-pattern>/InitPage.jsp</url-pattern>
 </servlet-mapping>
 <!- ... ->
 </web-app> 
    
    
      5.3 提供应用范围内的初始化参数      一般，对单个地servlet或JSP页面分配初始化参数。指定的servlet或JSP页面利用ServletConfig的getInitParameter方法读取这些参数。但是，在某些情形下，希望提供可由任意servlet或JSP页面借助ServletContext的getInitParameter方法读取的系统范围内的初始化参数。可利用context-param元素声明这些系统范围内的初始化值。context-param元素应该包含param-name、param-value以及可选的description子元素，如下所示: <context-param>
 <param-name>support-email</param-name>
 <param-value>blackhole@mycompany.com</param-value>
 </context-param>可回忆一下，为了保证可移植性，web.xml内的元素必须以正确的次序声明。但这里应该注意，context-param元素必须出现任意与文档有关的元素 (icon、display-name或description) 之后及filter、filter-mapping、listener或servlet元素之前。5.4 在服务器启动时装载servlet假如servlet或JSP页面有一个要花很长时间执行的init (servlet) 或jspInit (JSP) 方法。例如，假如init或jspInit方法从某个数据库或ResourceBundle查找产量。这种情况下，在第一个客户机请求时装载servlet的缺省行为将对第一个客户机产生较长时间的延迟。因此，可利用servlet的load-on-startup元素规定服务器在第一次启动时装载servlet。下面是一个例子。<servlet>
 <servlet-name> … </servlet-name>
 <servlet-class> … </servlet-class> <!- Or jsp-file ->
 <load-on-startup/>
 </servlet>可以为此元素体提供一个整数而不是使用一个空的load-on-startup。想法是服务器应该在装载较大数目的servlet或JSP页面之前装载较少数目的servlet或JSP页面。例如，下面的servlet项 (放置在Web应用的WEB-INF目录下的web.xml文件中的web-app元素内) 将指示服务器首先装载和初始化SearchServlet，然后装载和初始化由位于Web应用的result目录中的index.jsp文件产生的servlet。<servlet>
 <servlet-name>Search</servlet-name>
 <servlet-class>myPackage.SearchServlet</servlet-class> <!- Or jsp-file ->
 <load-on-startup>1</load-on-startup>
 </servlet>
 <servlet>
 <servlet-name>Results</servlet-name>
 <servlet-class>/results/index.jsp</servlet-class> <!- Or jsp-file ->
 <load-on-startup>2</load-on-startup>
 </servlet>6 声明过滤器servlet版本2.3引入了过滤器的概念。虽然所有支持servlet API版本2.3的服务器都支持过滤器，但为了使用与过滤器有关的元素，必须在web.xml中使用版本2.3的DTD。
 过滤器可截取和修改进入一个servlet或JSP页面的请求或从一个servlet或JSP页面发出的相应。在执行一个servlet或JSP页面之前，必须执行第一个相关的过滤器的doFilter方法。在该过滤器对其FilterChain对象调用doFilter时，执行链中的下一个过滤器。如果没有其他过滤器，servlet或JSP页面被执行。过滤器具有对到来的ServletRequest对象的全部访问权，因此，它们可以查看客户机名、查找到来的cookie等。为了访问servlet或JSP页面的输出，过滤器可将响应对象包裹在一个替身对象 (stand-in object) 中，比方说把输出累加到一个缓冲区。在调用FilterChain对象的doFilter方法之后，过滤器可检查缓冲区，如有必要，就对它进行修改，然后传送到客户机。例如，程序清单5-11帝国难以了一个简单的过滤器，只要访问相关的servlet或JSP页面，它就截取请求并在标准输出上打印一个报告 (开发过程中在桌面系统上运行时，大多数服务器都可以使用这个过滤器) 。程序清单5-11 ReportFilter.java
 package moreservlets;import java.io.*;
 import javax.servlet.*;
 import javax.servlet.http.*;
 import java.util.*;/** Simple filter that prints a report on the standard output
 * whenever the associated servlet or JSP page is accessed.
 * 
 * Taken from More Servlets and JavaServer Pages
 * from Prentice Hall and Sun Microsystems Press,
 * http://www.moreservlets.com/.
 * © 2002 Marty Hall; may be freely used or adapted.
 */public class ReportFilter implements Filter {
 public void doFilter(ServletRequest request,
 ServletResponse response,
 FilterChain chain)
 throws ServletException, IOException {
 HttpServletRequest req = (HttpServletRequest)request;
 System.out.println(req.getRemoteHost() +
 " tried to access " +
 req.getRequestURL() +
 " on " + new Date() + ".");
 chain.doFilter(request,response);
 }public void init(FilterConfig config)
 throws ServletException {
 }public void destroy() {}
 } 
      
      
        web.xml 详解三
      
      
      
        一旦建立了一个过滤器，可以在web.xml中利用filter元素以及filter-name (任意名称) 、file-class (完全限定的类名) 和 (可选的) init-params子元素声明它。请注意，元素在web.xml的web-app元素中出现的次序不是任意的；允许服务器 (但不是必需的) 强制所需的次序，并且实际中有些服务器也是这样做的。但这里要注意，所有filter元素必须出现在任意filter-mapping元素之前，filter-mapping元素又必须出现在所有servlet或servlet-mapping元素之前。      例如，给定上述的ReportFilter类，可在web.xml中作出下面的filter声明。它把名称Reporter与实际的类ReportFilter (位于moreservlets程序包中) 相关联。<filter>
 <filter-name>Reporter</filter-name>
 <filter-class>moresevlets.ReportFilter</filter-class>
 </filter>一旦命名了一个过滤器，可利用filter-mapping元素把它与一个或多个servlet或JSP页面相关联。关于此项工作有两种选择。首先，可使用filter-name和servlet-name子元素把此过滤器与一个特定的servlet名 (此servlet名必须稍后在相同的web.xml文件中使用servlet元素声明) 关联。例如，下面的程序片断指示系统只要利用一个定制的URL访问名为SomeServletName的servlet或JSP页面，就运行名为Reporter的过滤器。<filter-mapping>
 <filter-name>Reporter</filter-name>
 <servlet-name>SomeServletName</servlet-name>
 </filter-mapping>其次，可利用filter-name和url-pattern子元素将过滤器与一组servlet、JSP页面或静态内容相关联。例如，相面的程序片段指示系统只要访问Web应用中的任意URL，就运行名为Reporter的过滤器。<filter-mapping>
 <filter-name>Reporter</filter-name>
 <url-pattern>/*</url-pattern>
 </filter-mapping>例如，程序清单5-12给出了将ReportFilter过滤器与名为PageName的servlet相关联的web.xml文件的一部分。名字PageName依次又与一个名为TestPage.jsp的JSP页面以及以模式http://host/webAppPrefix/UrlTest2/ 开头的URL相关联。TestPage.jsp的源代码已经JSP页面命名的谈论在前面的3节"分配名称和定制的URL"中给出。事实上，程序清单5-12中的servlet和servlet-name项从该节原封不动地拿过来的。给定这些web.xml项，可看到下面的标准输出形式的调试报告 (换行是为了容易阅读) 。audit.irs.gov tried to access
 http://mycompany.com/deployDemo/UrlTest2/business/tax-plan.html
 on Tue Dec 25 13:12:29 EDT 2001.程序清单5-12 Web.xml (说明filter用法的摘录) 
 <?xml version="1.0" encoding="ISO-8859-1"?>
 <!DOCTYPE web-app
 PUBLIC "-//Sun Microsystems, Inc.//DTD Web Application 2.3//EN"
 "http://java.sun.com/dtd/web-app_2_3.dtd"><web-app>
 <filter>
 <filter-name>Reporter</filter-name>
 <filter-class>moresevlets.ReportFilter</filter-class>
 </filter>
 <!- ... ->
 <filter-mapping>
 <filter-name>Reporter</filter-name>
 <servlet-name>PageName</servlet-name>
 </filter-mapping>
 <!- ... ->
 <servlet>
 <servlet-name>PageName</servlet-name>
 <jsp-file>/RealPage.jsp</jsp-file>
 </servlet>
 <!- ... ->
 <servlet-mapping>
 <servlet-name> PageName </servlet-name>
 <url-pattern>/UrlTest2/*</url-pattern>
 </servlet-mapping>
 <!- ... ->
 </web-app> 7 指定欢迎页假如用户提供了一个像http://host/webAppPrefix/directoryName/ 这样的包含一个目录名但没有包含文件名的URL，会发生什么事情呢？用户能得到一个目录表？一个错误？还是标准文件的内容？如果得到标准文件内容，是index.html、index.jsp、default.html、default.htm或别的什么东西呢？Welcome-file-list元素及其辅助的welcome-file元素解决了这个模糊的问题。例如，下面的web.xml项指出，如果一个URL给出一个目录名但未给出文件名，服务器应该首先试用index.jsp，然后再试用index.html。如果两者都没有找到，则结果有赖于所用的服务器 (如一个目录列表) 。<welcome-file-list>
 <welcome-file>index.jsp</welcome-file>
 <welcome-file>index.html</welcome-file>
 </welcome-file-list>虽然许多服务器缺省遵循这种行为，但不一定必须这样。因此，明确地使用welcom-file-list保证可移植性是一种良好的习惯。8 指定处理错误的页面现在我了解到，你在开发servlet和JSP页面时从不会犯错误，而且你的所有页面是那样的清晰，一般的程序员都不会被它们的搞糊涂。但是，是人总会犯错误的，用户可能会提供不合规定的参数，使用不正确的URL或者不能提供必需的表单字段值。除此之外，其它开发人员可能不那么细心，他们应该有些工具来克服自己的不足。error-page元素就是用来克服这些问题的。它有两个可能的子元素，分别是: error-code和exception-type。第一个子元素error-code指出在给定的HTTP错误代码出现时使用的URL。第二个子元
      
      
      
        http://blog.csdn.net/Imain/archive/2006/12/28/1465770.aspx
      
      
      
        http://blog.itpub.net/13081368/viewspace-440439
      
      
      
        http://www.ibm.com/developerworks/cn/java/j-lo-servlet30/
      
  
