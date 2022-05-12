---
title: JSP
author: "-"
date: 2012-09-22T07:32:25+00:00
url: /?p=4176
categories:
  - Java
tags:$
  - reprint
---
## JSP
Java EE 7 (June 12, 2013)   JavaServer Pages (JSP) 2.3


## 

### JSP指令

JSP指令控制JSP编译器如何去生成[servlet][1]{.mw-redirect}，以下是可用的指令: 

  * 包含指令include –包含指令通知JSP编译器把另外一个文件完全包含入当前文件中。效果就好像被包含文件的内容直接被粘贴到当前文件中一样。这个功能和C[预处理器][2]所提供的很类似。被包含文件的扩展名一般都是"jspf" (即JSP **Fragment**，JSP碎片) :


  
    <%@ include file="somefile.jsp" %>

    
    
      
        页面指令page –页面指令有以下几个选项: 
      
    
    
    
      
        
          import
        
        
        
          使一个JAVA导入声明被插入到最终页面文件。
        
      
      
      
        
          contentType
        
        
        
          规定了生成内容的类型。当生成非HTML内容或者当前字符集character set并非默认字符集时使用。
        
      
      
      
        
          errorPage
        
        
        
          处理HTTP请求时，如果出现异常则显示该错误提示信息页面。
        
      
      
      
        
          isErrorPage
        
        
        
          如果设置为TRUE，则表示当前文件是一个错误提示页面。
        
      
      
      
        
          isThreadSafe
        
        
        
          表示最终生成的servlet是否线程安全 (thread safe) 。
        
      
    
    
    
      
        <%@ page import="java.util.*" %> //example import导入样例
<%@ page contentType="text/html" %> //example contentType页面类型样例
<%@ page isErrorPage=false %> //example for non error page无错页面样例
<%@ page isThreadSafe=true %> //example for a thread safe JSP线程安全JSP样例

      
    
    
    
      注意: 在同一个JSP文件中只有"import"导入页面指令可以被多次使用。
    
    
    
      
        标签库指令taglib –标签库指令描述了要使用的JSP标签库。该指令需要指定一个前缀prefix (和C++的命名空间很类似) 和标签库的描述URI:
      
    
    
    
      
        <%@ taglib prefix="myprefix" uri="taglib/mytag.tld" %>
      
    
    
    
  

JSP (Java Server Pages)是由Sun Microsystems公司倡导、许多公司参与一起建立的一种动态网页技术标准。

JSP一种使软件开发者可以响应客户端请求，而动态生成```html[3]、```xml[4]或其他格式文档的[Web][5]{.mw-redirect}网页的技术标准。JSP技术是以```java[6]语言作为[脚本语言][7]的，JSP网页为整个服务器端的Java库单元提供了一个接口来服务于[HTTP][8]{.mw-redirect}的应用程序。JSP被JSP编译器编译成Java Servlets。一个JSP编译器可以把JSP编译成JAVA代码写的servlet然后再由JAVA编译器来编译成机器码，也可以直接编译成二进制码。

JSP技术有点类似ASP技术，它是在传统的网页HTML文件(\*.htm,\*.html)中插入Java程序段(Scriptlet)和JSP标记(tag)，从而形成JSP文件(*.jsp)。 用JSP开发的Web应用是跨平台的，既能在Linux下运行，也能在其他操作系统上运行。

JSP技术使用Java编程语言编写类XML的tags和scriptlets，来封装产生动态网页的处理逻辑。网页还能通过tags和scriptlets访问存在于服务端的资源的应用逻辑。JSP将网页逻辑与网页设计和显示分离，支持可重用的基于组件的设计，使基于Web的应用程序的开发变得迅速和容易。

Web服务器在遇到访问JSP网页的请求时，首先执行其中的程序段，然后将执行结果连同JSP文件中的HTML代码一起返回给客户。插入的Java程序段可以操作数据库、重新定向网页等，以实现建立动态网页所需要的功能。

JSP与JavaServlet一样，是在服务器端执行的，通常返回给客户端的就是一个HTML文本，因此客户端只要有浏览器就能浏览。

JSP的1.0规范的最后版本是1999年9月推出的，12月又推出了1.1规范。目前较新的是JSP1.2规范，JSP2.0规范的征求意见稿也已出台。

JSP页面由HTML代码和嵌入其中的Java代码所组成。服务器在页面被客户端请求以后对这些Java代码进行处理，然后将生成的HTML页面返回给客户端的浏览器。Java Servlet是JSP的技术基础，而且大型的Web应用程序的开发需要Java Servlet和JSP配合才能完成。JSP具备了Java技术的简单易用，完全的面向对象，具有平台无关性且安全可靠，主要面向因特网的所有特点。

自JSP推出后，众多大公司都支持JSP技术的服务器，如IBM、Oracle、Bea公司等，所以JSP迅速成为商业应用的服务器端语言。

JSP可用一种简单易懂的等式表示为: HTML+Java+JSP标记=JSP。

新的JSP规范版本包括新的用于提升程序员工作效率功能，主要有:  JSPAn Expression Language (EL)

允许开发者创建 Velocity-样式 templates (among other things).更快更简单的创建新标签的方法。

Hello, ${param.visitor} <%- same as: Hello, <%=request.getParameter("visitor")%> -%>

MVC 模式

为了把表现层presentation从请求处理request processing 和数据存储data storage中分离开来，SUN公司推荐在JSP文件中使用一种"模型-视图-控制器"Model-view-controller 模式。规范的SERVLET或者分离的JSP文件用于处理请求。当请求处理完后，控制权交给一个只作为创建输出作用的JSP页。有几种平台都基于服务于网络层的模-视图-控件 模式(比如Struts 和Spring framework)。

一 JSP2.0与JSP1.2比较

JSP 2.0是对JSP 1.2的升级，新增功能: 

1. Expression Language

2. 新增Simple Tag和Tag File

3.web.xml新增<jsp:config>元素

二 特别说明web.xml.

web.xml新增<jsp:config>元素

<jsp-config> 元素主要用来设定JSP相关配置，<jsp-config> 包括<taglib>和<jsp-property-group>

子元素。

(1)其中<taglib>以前的Jsp1.2中就有的，taglib主要作用是作为页面taglib标签中的uri和tld文件的一个映射关系

(2)其中<jsp-property-group>是JSP2.0种新增的元素。

<jsp-property-group> 主要包括8个子元素，它们分别是: 

<jsp-property-group>

<description>

设定的说明

</description>

<display-name>设定名称</display-name>

<url-pattern>设定值所影响的范围</url-pattern>

<el-ignored>若为true则不支持EL语法</el-ignored>

<page-encoding>ISO-8859-1</page-encoding>

<scripting-invalid> 若为true则不支持<% scripting%> 语法</scripting-invalid>

<include-prelude>设置JSP网页的抬头,扩展名为.jspf </include-prelude>

<include-coda>设置JSP网页的结尾,扩展名为.jspf</include-coda>

</jsp-property-group>

 (1) 一次编写，到处运行。除了系统之外，代码不用做任何更改。

 (2) 系统的多平台支持。基本上可以在所有平台上的任意环境中开发，在任意环境中进行系统部署，在任意环境中扩展。相比ASP/.net的局限性是显而易见的。

 (3) 强大的可伸缩性。从只有一个小的Jar文件就可以运行Servlet/JSP，到由多台服务器进行集群和负载均衡，到多台Application进行事务处理，消息处理，一台服务器到无数台服务器，Java显示了一个巨大的生命力。 JSP (4) 多样化和功能强大的开发工具支持。这一点与ASP很像，Java已经有了许多非常优秀的开发工具，而且许多可以免费得到，并且其中许多已经可以顺利的运行于多种平台之下。

(5)支持服务器端组件。web应用需要强大的服务器端组件来支持，开发人员需要利用其他工具设计实现复杂功能的组件供web页面调用，以增强系统性能。JSP可以使用成熟的JAVA BEANS 组件来实现复杂商务功能。


现在就让我们开始动手帮助你建立一个可执行JSP范例网站。

一、安装好你的机器来使用JSP

二、JSP语法的基本原理

三、JSP与JavaBean

四、JSP的内部对象

五、JSP其他相关资源

JSP开发入门2

安装好你的机器来使用JSP

你将会需要Java 2软件开发工具(JSDK)，它原来的名称是Java开发工具(JDK)以及JavaServer网站开发工具(JSWDK)，Tomcat，或是其它支持JSP的网络服务器。Sun免费提供JSDK与JSWDK来供Windows，Solaris，以及Linux平台使用。

如果你想要在你目前的网络服务器上使用JSP，但服务器本身并不支持JSP与Java servlets，你可以试试看Allaire的Jrun，它的作用就像是针对Netscape企业版与FastTrack服务器、微软的网际网络信息服务器(IIS)与个人网络服务器(PWS)、Apache、以及其它服务器的网络服务器附加设备。你也可以使用Apache网络服务器的Java版本，最新的JSWDK里有提供。

下载与安装你需要的组件

目前发布的1.2.2-001，JSDK可下载的版本是以可安装的压缩形式。下载的文件大约是20MB，可提供完整的Java发展环境，让你能建立利用标准API为核心的Java解决之道。然而，你的网络服务器需要应用到JSP的唯一一件事是Java编译器。要让网络服务器知道编译器的位置，将环境变量JAVA.HOME设到JSDK的安装目录。如果你是在Windows上安装并且接受预设目录，将这行程序代码set JAVA.HOME=C:1.2.2加到你的autoexec.bat档案并且重新开机。

在安装好JSDK之后，下载并且安装JSWDK或beta版的Tomcat，以Java为主的Apache网络服务器。安装在哪里并不重要，重要的是你可以找到它。一般而言，它会放在上层目录，这种方式可以让你取代JSWDK或 JSDK的网络服务器，不需要移动其它的网络服务器。在你安装好这个档案之后，你就可以准备发展JSP了。

在你正确的安装JSWDK之后，执行startserver指令文件来激活网络服务器，预设通讯端口 为 8080。要看你在激活服务器之后是均C有正确的安装工具，你可以加载范例JSP档案中的任何一个(http://localhost:8080/examples/jsp/)。如果你能够成功的执行一个范例档案，你可以知道你已经正确的设定好软件了。如果你在激活服务器的控制台窗口看到错误讯息，那么你需要解决这个问题。最常发生的问题是没有设定(或者不正确设定)环境变量JAVA.HOME。要检视目前的环境设定，在DOS模式下键入set。

开始

解释JSP语法之前，先建立一个显示目前日期与时间的快速网页并且将它储存成sample.jsp:

<html>

<head>

<title>First Page</title>

</head>

<body>

Today is:

<%= new java.util.Date() %>


</body>

</html>.

将这个档案与你所有的HTML与JSP网页放在你JSWDK安装目录下的网页目录里. 你可以在http://localhost:8080/sample.jsp下载此页.当你第一次参观这个网页时，网站服务器会将JSP翻译成Java servlet程序代码，那你就会看到目前的日期与时间.。

现在你已经下载，安装，并且架构好发展环境，你已经准备好要了解JSP语法与建立你自己的JSP为主的解决之道。

JSP开发入门3

JSP语法的基本原理

安装之后，接下来我们要讨论JSP的语法.如果要偷懒，你可以下载语法卡而如果你不熟悉 Java的程序设计，你可能会想要参考Sun的使用手册；然而，网站建立者不应该做太多的Java发展。除了几个函数调用之外，出现在你JSP网页上的Java程序代码应该将它减到最少;

记住这点之后，现在让我们先来看看JSP的编译器指引与指令组件，之后我们将解释JavaBeans与内部对象. JSP编译器指引与指令组件有五种型态.JSP 1.0之后，大部分的JSP是包含在以<% 作为开始%>作为结束的单一卷标里.新的 JSP 1.1规格已经发表了，它同时也与XML兼容.

JSP的编译器指引与指令组件

编译器指示<%@ 编译器指示 %>

声明<%! 声明 %>

表达式 <%= 表达式 %>

程序代码片段/小型指令<% 程序代码片段 %>

注释<%- 注释 -%>

编译器指示

JSP的编译器指示是针对JSP引擎。它们并不会直接产生任何看得见的输出；相反的，它们是在告诉引擎如何处理其它的JSP网页。它们永远包含在 <%@ ?%>卷标里。两个主要的指引是 page与include。我们不会讨论taglib编译器指引但它可以在JSP1.1里用来建立自订卷标。

你几乎可以在你所有的JSP网页最上面找到page编译器指示。虽然这不是必须的，但它可以让你指定到哪里可以找到支持的Java类别这类的事: 

<%@ page import="java.util.Date" %>，

当发生Java问题的事件时应该将讯息传送到哪里: 

<%@ page errorPage="errorPage.jsp" %>，

以及你是?需要为使用者管理通话期的信息，可能存取多个网页(稍后在JavaBeans里会有更多通话期的讨论):

<%@ page session="true" %>。

include编译器指示让你将你的内容分成几个可管理的组件，就像那些有表头或脚注的网页。所包含的网页可以是固定格式的HTML网页或者是JSP内容的网页:

<%@ include file="filename.jsp" %>。

宣告

JSP声明让你定义网页层的变量，来储存信息或定义支持的函式，让JSP网页的其余部分能够使用。如果你发现自己有太多的程序代码，你最好将它们放在不同的Java类别里。你可以在 <%! ?%>卷标里找到声明。记住要在变量声明的后面加上分号，就跟任何有效的Java叙述的形式一样: <%! int i=0; %>。

表达式

JSP里有表达式，评估表达式的结果可以转换成字符串并且直接使用在输出网页上。JSP运算是属于 <%= ?%> 卷标里，并不包含分号，加引号字符串的无用部分。

<%= i %>

<%= "Hello" %> 。

程序代码片段/小型指令文件

JSP程序代码片段或小型指令文件是包含在<% ?%> 卷标里。当网络服务器接受这段请求时，这段Java程序代码会执行。小型指令文件可以是原始的HTML或XML，其内部的程序代码片段可以让你建立有条件的执行程序代码，或者只是一些使用另一块程序代码的东西。举例来说，下列的程序代码结合了表达式与小型指令文件，在H1，H2，H3，以及H4卷标里显示字符串"Hello"。小型指令文件不限于一行的原始程序代码 :

<% for (int i=1; i<=4; i++) { %>

<H<%=i%>>Hello</H<%=i%>>

<% } %>。

注释

最后一个主要JSP组件是嵌入式注释。虽然你可以在你的档案里包含HTML注释，如果使用者检视网页的原始码，他们也会看到这些注释。如果你不要让使用者看到你的批注，你可以将它放在<%- ?-%>卷标里:

<%- 针对服务器端的注释 -%>。

JSP开发入门4

JSP与JavaBean

虽然你可以在小型指令文件里放入一大块的程序代码，但是大多数的Java程序代码是属于可以重复使用的组件，称为JavaBean。JavaBean就跟ActiveX控件一样:它们提供已知的功能，并且是为了可随时重复使用的目的而设计的。

JavaBean的价值在于它可以经由一组特性来使用，而这些特性则提供对JavaBean设定的存取。以人来作范例，此人就是JavaBean，而他的姓名，社会福利安全号码，以及住址可以是特性。对于JSP网站，基本上你是将'JavaBean'动态的连接到你的网站。

假设JavaBean是在建立网站之前建好的，你要做的第一件事是告诉JSP网页它所需要使用JavaBean.这工作可以用<jsp:useBean>卷标来完成: <jsp:useBean id="localName" class="com.jguru.Person" scope="application" />.

<jsp:useBean>卷标需要你以id 属性来辨识JavaBean.在这里，你提供一个名称让JSP网页来辨识JavaBean，除了id 属性之外，你也必须告诉网页要到哪里去找这个JavaBean，或者是它的Java类别名称。类别属性提供如何在各式方法之中找到它，最后一个需要的组件是scope 属性.有了范围属性的帮助，你可以告诉JavaBean，要它为单一网页(预设)[scope="page"]；为一个被请求的网页[scope="request"]；为通话期[scope="session"]；或为整个应用程序[scope="application"]来维护它自己的信息.对于通话期范围，你可以很容易的维护JSP网页里的项目，例如购物车。

一但你宣告了JavaBean之后，你就可以存取它的特性来订定它。要取得一特性的值，使用<jsp:getProperty>卷标。有了<jsp:getProperty>卷标，你可以指定要使用的JavaBean名称(从useBean的id字段)，以及你要取得值的特性。接着，真正的值就会放在输出里: <jsp:getProperty id="localName" property="name" />.

要更改JavaBean的特性，你需要使用<jsp:setProperty>卷标.对这个卷标，你也需要辨认JavaBean以及要修正的特性，除此之外，你还需要提供新值.如果命名正确，这些可以直接经由规定的格式取得: <jsp:setProperty id="localName" property="*" />;

要从一参数取得，你必须直接命名此特性以及参数: <jsp:setProperty id="localName" property="address" param="parameterName" />;

或是直接以名称与值来设定: <jsp:setProperty id="localName" property="serialNumber" value="string" /> or <jsp:setProperty id="localName" property="serialNumber" value= <%= expression %> />.

有关JavaBean的最后一点:要让网络服务器可以找到JavaBean，你需要将它们的类别档案放在特别位置。对JSWDK而言，最简单的地方是在安装目录里的类别目录，例如 jswdk-1.0.1classes.

JSP开发入门5

JSP的内部对象

最后一个与JSP语法有关的组件叫做内部对象.在JSP小型指令文件内，你可以存取这些内部对象来与执行JSP网页的servlet环境相互作用。许多对内部对象的存取应该要简化。然而，这些是范例，它们的存取都是可接受的，要完整的利用内部对象设定则需要对最新的Java Servlet API有所了解。

下表列出你可以使用的内部对象。

内部对象说明

request 客户端请求，此请求会包含来自GET/POST请求的参数

response网页传回客户端的响应

pageContext 网页的属性是在这里管理

session 与请求有关的会话

application servlet正在执行的内容

out 用来传送响应的输出流

config代码片段配置对象

pageJSP网页本身

exception针对错误网页，未捕捉的例外

那么，这些是做什么的，而你应该如何使用它们呢?基本上，在你的小型指令文件里，你可以使用它们来存取执行JSP程序代码的servlet。为了避免谈论到太多Servlet API 的细节，让我们来检视一些你可以利用它们来做的事: 

不必使用表达式，你可以直接存取内部out对象来打印一些东西到response:

<% out.println("Hello"); %>.

不必直接传送参数到JavaBean，你可以藉由请求对象来取得参数的值:

<% String name=request.getParameter("name"); out.println(name); %>。

当你以JSP写了许多的应用程序之后，如果你建立了JavaBeans或者发现你自己将太多的Java原始码放入你的JSP档案，你需要建立支持的Java类别，这样可以鼓励重复使用并且降低JSP网页转换时所需要的时间。当你需要建立Java类别时，你必须:

将JDSWK的安装目录in目录加到你的PATH。在你的autoexec.bat档案的PATH行的最后，加入C:1.2.2in; 。

以下面的指令将JAR档案复制到jrelibext目录: 

copy c:jswdk-1.0.1libservlet.jar c:jdk1.2.2jrelibext.

jsp-与ASP的比较

JSP(Java Server Page)与ASP(Active Server Page)两者都是常用的动态网页技术，也都是可以嵌入HTML中的程序，但两者是有着本质的不同，主要从以下几个方面对其进行比较: 

1.Web服务器的支持: 大多数通用的 Web服务器如: Apache、Netscape和Microsoft IIS都支持JSP页面，只有微软本身的Microsoft IIS和Personal Web Server可以支持ASP。

2.平台的支持: JSP具有平台独立性，只要是一般的Java程序可以运行的平台，都支持JSP程序。Windows平台可以很好的支持ASP,但ASP对于基于Win32逐渐模型的依赖，使得它难于移植到其它平台上。

3.组件模型: JSP是建立在可重用的、跨平台的组件 (如: JavaBeans、Enterprises JavaBeans和用户定制的标签库等组件) 之上的，而ASP使用的是基于Win32的COM组件模型。

4.脚本语言: JSP可以使用Java编程语言或JavaScript作为脚本语言，而ASP使用VBScript或Jscript作为脚本语言。

5.安全性: JSP使用Java安全模型，而ASP使用Windows NT的安全结构。

6.与Access数据库的连接: JSP使用JDBC建立与Access数据库的连接，而ASP对Access数据库使用Data Active Objects。

7.用户定制的标签: JSP可以使用用户定制标签库进行扩充，而ASP中没有用户定制标签库，ASP是不能扩充的。


http://zh.wikipedia.org/zh-cn/JSP

http://en.wikipedia.org/wiki/Java_EE_version_history

 [1]: http://zh.wikipedia.org/wiki/Servlet "Servlet"
 [2]: http://zh.wikipedia.org/wiki/%E9%A2%84%E5%A4%84%E7%90%86%E5%99%A8 "预处理器"
 [3]: http://zh.wikipedia.org/wiki/HTML "HTML"
 [4]: http://zh.wikipedia.org/wiki/XML "XML"
 [5]: http://zh.wikipedia.org/wiki/Web "Web"
 [6]: http://zh.wikipedia.org/wiki/Java "Java"
 [7]: http://zh.wikipedia.org/wiki/%E8%84%9A%E6%9C%AC%E8%AF%AD%E8%A8%80 "脚本语言"
 [8]: http://zh.wikipedia.org/wiki/HTTP "HTTP"