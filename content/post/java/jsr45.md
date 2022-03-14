---
title: JSR45
author: "-"
date: 2012-06-07T13:08:20+00:00
url: /?p=3447
categories:
  - Java

tags:
  - reprint
---
## JSR45
JAVA Debug(eclipse debug) 和 JSR-45 的基本原理 (2007-02-07 11:07:13)转载▼
  
分类:  Java的一些问题
  
JAVA 调试框架 (JPDA) 简介

JPDA 是一个多层的调试框架，包括 JVMDI、JDWP、JDI 三个层次。JAVA 虚拟机提供了 JPDA 的实现。其开发工具作为调试客户端，可以方便的与虚拟机通讯，进行调试。Eclipse 正是利用 JPDA 调试 JAVA 应用，事实上，所有 JAVA 开发工具都是这样做的。SUN JDK 还带了一个比较简单的调试工具以及示例。
  
JVMDI 定义了虚拟机需要实现的本地接口
  
JDWP 定义了JVM与调试客户端之间的通讯协议

调试客户端和JVM 既可以在同一台机器上，也可以远程调试。JDK 会包含一个默认的实现 jdwp.dll，JVM 允许灵活的使用其他协议代替 JDWP。SUN JDK 有两种方式传输通讯协议: Socket 和共享内存(后者仅仅针对 Windows)，一般我们都采用 Socket 方式。

你可以用下面的参数，以调试模式启动JVM
   
-Xdebug -Xnoagent -Xrunjdwp:transport=dt_socket,address=8000,server=y,suspend=n
    
-Xrunjdwp JVM 加载 jdwp.dll
     
transport=dt_socket 使用 Socket 传输
     
address 表示调试端口号
     
server=y 表示 JVM 作为服务器，建立 Socket
     
suspend=n 表示启动过程中，JVM 不会挂起去等待调试客户端连接
  
JDI 则是一组JAVA接口

如果是一个 JAVA 的调试客户端，只要实现 JDI 接口，利用JDWP协议，与虚拟机通讯，就可以调用JVMDI了。
  
下图为 JPDA 的基本架构: 
                            
Components Debugger Interface

/ |--------|
                 
/ | VM |
  
debuggee --( |--------| <\---\---- JVMDI - Java VM Debug Interface | back-end | |\---\---\---\---\---\---\-----| / | comm channel -( | <\---\---\---\---\--- JDWP - Java Debug Wire Protocol | |\---\---\---\---\---\---\---| | front-end | |\---\---\---\---\---\---\---| <\---\---- JDI - Java Debug Interface | UI | |\---\---\---\---\---\---\---| 参见: http://java.sun.com/j2se/1.4.2/docs/guide/jpda/architecture.html Eclipse作为一个基于 JAVA 的调试客户端，利用 org.eclipse.jdt.debug Plugin 提供了JDI 的具体实现。JDI 接口主要包含下面 4 个包 com.sun.jdi com.sun.jdi.connect com.sun.jdi.event com.sun.jdi.request 本文不对 JDI 进行深入阐述，这里重点介绍 JDI 中与断点相关的接口。 com.sun.jdi 主要是JVM(VirtualMachine) 线程(ThreadReference) 调用栈(StackFrame) 以及类型、实例的描述。利用这组接口，调试客户端可以用类似类反射的方式，得到所有类型的定义，动态调用 Class 的方法。 com.sun.jdi.event 封装了JVM 产生的事件， JVM 正是将这些事件通知给调试客户端的。例如 BreakpointEvent 就是 JVM 执行到断点的时候，发出的事件；ClassPrepareEvent就是 Class 被加载时发出的事件。 com.sun.jdi.request 封装了调试客户端可以向 JVM发起的请求。例如 BreakpointRequest 向 JVM 发起一个添加断点的请求；ClassPrepareRequest 向 JVM 注册一个类加载请求，JVM 在加载指定 Class 的时候，就会发出一个 ClassPrepareEvent 事件。 JSR-45规范 JSR-45(Debugging Support for Other Languages)为那些非 JAVA 语言写成，却需要编译成 JAVA 代码，运行在 JVM 中的程序，提供了一个进行调试的标准机制。也许字面的意思有点不好理解，什么算是非 JAVA 语言呢？其实 JSP 就是一个再好不过的例子，JSR-45 的样例就是一个 JSP。 JSP的调试一直依赖于具体应用服务器的实现，没有一个统一的模式，JSR-45 针对这种情况，提供了一个标准的模式。我们知道，JAVA 的调试中，主要根据行号作为标志，进行定位。但是 JSP 被编译为 JAVA 代码之后，JAVA 行号与 JSP 行号无法一一对应，怎样解决呢？ JSR-45 是这样规定的: JSP 被编译成 JAVA 代码时，同时生成一份 JSP 文件名和行号与 JAVA 行号之间的对应表(SMAP)。JVM 在接受到调试客户端请求后，可以根据这个对应表(SMAP)，从 JSP 的行号转换到 JAVA 代码的行号；JVM 发出事件通知前, 也根据对应表(SMAP)进行转化，直接将 JSP 的文件名和行号通知调试客户端。 我们用 Tomcat 5.0 做个测试，有两个 JSP，Hello.jsp 和 greeting.jsp，前者 include 后者。Tomcat会将他们编译成 JAVA 代码(Hello_jsp.java)，JAVA Class(Hello_jsp.class) 以及 JSP 文件名/行号和 JAVA 行号之间的对应表(SMAP)。 Hello.jsp: 1 
            
2 
            
5 
            
6 <%@ include file="greeting.jsp" %>
            
7 
            
8 
  
greeting.jsp:

1 Hello There!

2 Goodbye on <%= new java.util.Date() %>

JSP 编译后产生的Hello_jsp.java 如下:
  
Hello_jsp.java: 1 package org.apache.jsp; 2 3 import javax.servlet.\*; 4 import javax.servlet.http.\*; 5 import javax.servlet.jsp.*; 6 7 public final class Hello_jsp extends org.apache.jasper.runtime.HttpJspBase 8 implements org.apache.jasper.runtime.JspSourceDependent { 9 10 private static java.util.Vector _jspx_dependants; 11 12 static { 13 _jspx_dependants = new java.util.Vector(1); 14 _jspx_dependants.add("/greeting.jsp"); 15 } 16 17 public java.util.List getDependants() { 18 return _jspx_dependants; 19 } 20 21 public void _jspService(HttpServletRequest request,
  
HttpServletResponse response) 22 throws java.io.IOException, ServletException { 23 24 JspFactory _jspxFactory = null; 25 PageContext pageContext = null; 26 HttpSession session = null; 27 ServletContext application = null; 28 ServletConfig config = null; 29 JspWriter out = null; 30 Object page = this; 31 JspWriter _jspx_out = null; 32 33 34 try { 35 _jspxFactory = JspFactory.getDefaultFactory(); 36 response.setContentType("text/html"); 37 pageContext = _jspxFactory.getPageContext(this, request, response, 38 null, true, 8192, true); 39 application = pageContext.getServletContext(); 40 config = pageContext.getServletConfig(); 41 session = pageContext.getSession(); 42 out = pageContext.getOut(); 43 _jspx_out = out; 44 45 out.write(" rn"); 46 out.write(" rn"); 50 out.write(" rn"); 51 out.write("Hello There!"); 52 out.write(" 

rnGoodbye on "); 53 out.write(String.valueOf( new java.util.Date() )); 54 out.write(" rn"); 55 out.write(" rn"); 56 out.write("</body> rn"); 57 out.write("</html> rn"); 58 } catch (Throwable t) { 59 if (!(t instanceof javax.servlet.jsp.SkipPageException)){ 60 out = _jspx_out; 61 if (out != null && out.getBufferSize() != 0) 62 out.clearBuffer(); 63 if (pageContext != null) pageContext.handlePageException(t); 64 } 65 } finally { 66 if (_jspxFactory != null) _jspxFactory.releasePageContext ( pageContext); 67 } 68 } 69 }
  
Tomcat 又将这个 JAVA 代码编译为 Hello_jsp.class，他们位于:  $Tomcat_install_path$workStandalonelocalhost_ 目录下。但是 JSP 文件名/行号和 JAVA 行号的对应表(以下简称SMAP) 在哪里呢？答案是，它保存在 Class 中。如果用 UltraEdit 打开这个 Class 文件，就可以找到 SourceDebugExtension 属性，这个属性用来保存 SMAP。

JVM 规范定义了 ClassFile 中可以包含 SourceDebugExtension 属性，保存 SMAP: 
  
SourceDebugExtension_attribute { u2 attribute_name_index; u4 attribute_length; u1 debug_extension[attribute_length]; }

我用 javassist 做了一个测试(javassist可是一个好东西，它可以动态改变Class的结构，JBOSS 的 AOP就利用了javassist，这里我们只使用它读取ClassFile的属性)
  
public static void main(String[] args) throws Exception{
     
String[]files = {
  
"E:\Tomcat5_0_5\work\Catalina\localhost_\org\apache\jsp\Hello_jsp.class",
     
};

for(int k = 0; k < files.length; k++){  String file = files[k];  System.out.println("Class : " + file);  ClassFile classFile = new ClassFile(new DataInputStream(new FileInputStream(file)));   AttributeInfo attributeInfo = classFile.getAttribute("SourceDebugExtension");  System.out.println("attribute name :" + attributeInfo.getName() + "]nn");  byte[]bytes = attributeInfo.get();  String str = new String(bytes);  System.out.println(str); } } 这段代码显示了SourceDebugExtension 属性，你可以看到SMAP 的内容。编译JSP后，SMAP 就被写入 Class 中, 你也可以利用 javassist 修改 ClassFile 的属性。 下面就是 Hello_jsp.class 中保存的 SMAP 内容: SMAP E:Tomcat5_0_5workCatalinalocalhost_orgapachejspHello_jsp.java JSP \*S JSP \*F + 0 Hello.jsp /Hello.jsp + 1 greeting.jsp /greeting.jsp \*L 1:45 2:46 3:47 3:48 4:49 5:50 1#1:51 1:52 2:53 7#0:56 8:57 \*E 首先注明JAVA代码的名称: Hello_jsp.java，然后是 stratum 名称:  JSP。随后是两个JSP文件的名称 : Hello.jsp、greeting.jsp。两个JSP文件共10行，产生的Hello_jsp共69行代码。最后也是最重要的内容就是源文件文件名/行号和目标文件行号的对应关系(\*L 与 \*E之间的部分) 在规范定义了这样的格式:  源文件行号 # 源文件代号,重复次数 : 目标文件开始行号,目标文件行号每次增加的数量 (InputStartLine # LineFileID , RepeatCount : OutputStartLine , OutputLineIncrement) 源文件行号(InputStartLine) 目标文件开始行号(OutputStartLine) 是必须的。下面是对这个SMAP具体的说明:  1:45 2:46 3:47 3:48 4:49 5:50(没有源文件代号，默认为Hello.jsp) 开始行号 结束行号 Hello.jsp: 1 -> Hello_jsp.java: 45
                
2 -> 46
                
3 -> 47 48
                
4 -> 49
                
5 -> 50

1#1:51 1:52 2:53(1#1表示 greeting.jsp 的第1行)
  
greeting.jsp: 1 -> Hello_jsp.java: 51 52
                   
2 -> 53

7#0:56 8:57(7#0表示 Hello.jsp 的第7行)