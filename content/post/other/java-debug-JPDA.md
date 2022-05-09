---
title: 'JAVA 调试, JPDA'
author: "-"
date: 2012-06-07T07:22:32+00:00
url: java/remote/debugging
categories:
  - Java
tags:
  - reprint
---
## JAVA 调试, JPDA

远程调试
远程调试分为主动连接调试，和被动连接调试。这里以Eclipse为例。

主动连接调试：服务端配置监控端口，本地IDE连接远程监听端口进行调试，一般调试问题用这种方式。

被动连接调试：本地IDE监听某端口，等待远程连接本地端口。一般用于远程服务启动不了，启动时连接到本地调试分析。

主动连接调试
首先需要远程服务配置启动脚本:

JAVA_OPTS="$JAVA_OPTS -Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=5005"
如果是启动jar包，指令：

java -Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=y,address=8000 -jar test.jar

JAVA 自身支持调试功能，并提供了一个简单的调试工具 - JDB, 类似于功能强大的 GDB，JDB 也是一个字符界面的调试环境，并支持设置断点，支持线程线级的调试。

JAVA的调试方法如下:
首先设置JVM，并设置参数，使之工作在 DEBUG 模式下，加入参数: -Xdebug -Xrunjdwp,transport=dt_socket,server=y,address=5432,suspend=n,onthrow=java.io.IOException,launch=/sbin/echo

- -Xdebug: 通知 JVM 工作在 DEBUG 模式下  
- -Xrunjdwp 是通知 JVM 使用 (java debug wire protocol) 来运行调试环境。该参数提供了一系列的调试选项:
  - transport 指定调试数据的传送方式，dt_socket 是指用 SOCKET 模式，另有 dt_shmem 指用共享内存方式，其中，dt_shmem 只适用于 Windows 平台。  
  - server 参数是指是否支持在 server 模式的 JVM 中.
  - onthrow 当产生该类型的 Exception 时，JVM 就会中断下来，进行调式。(可选参数)
  - launch 当JVM被中断下来时，执行的可执行程序。(可选参数)
  - suspend: y/n 指明，是否在调试客户端建立起来后，再执行JVM。  
  - onuncaught (=y或n) 指明出现 uncaught exception 后， 是否中断JVM的执行.  
  - address 端口

启动调试工具。  
最简单的调试工具就是上面提到的JDB，以上述调试用JVM为例，可以用下面的命运行启动JDB:

    jdb -connect com.sun.jdi.SocketAttach:port=5432,hostname=192.168.11.213
  
另外，还有好多的可视化调试工具，如 IDEA, eclipse, jsawt 等等。Eclipses 可用 ant debug 来建立一个调试方法。  
其实就是使用了JDK的 JPDA，在启动服务器 (Jboss或者Tomcat等) 的命令行参数里面加上:
-Xdebug -Xrunjdwp:transport=dt_socket,address=8787,server=y,suspend=n

## tomcat

何为远程调试？我们一般调试一个 web项目的java代码时，需要将你的tomcat服务器和你的开发工具 (比如Jbuilder) 集成，或需要工具的一些插件支持(比如Eclipse 下的myclipse等)，这些方式都是在本地进行，即你的开发工具和tomcat运行在同一台服务器上，如果你的开发工具和服务器不再一台机器上那就需要实现远程调试功能了。

在tomcat/bin下的catalina.sh上边添加下边的 JPDA 参数

    CATALINA_OPTS="-Xdebug -Xrunjdwp:transport=dt_socket,address=5005,suspend=n,server=y"

## IDEA设置

Edit Configuration > Add new configuration > remote jvm debug  
command line arguments for remote JVM: -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005

#### use module classpath

    选择源码所在的工程

注意防火墙要开启相关端口

#### Java远程调试 {#subjcns!30EBEBD8BCD440DC!158}

    -Xdebug -Xnoagent -Djava.compiler=NONE -Xrunjdwp:transport=dt_socket,server=y,address=3999,suspend=n
  
  
      -XDebug               启用调试。
      -Xnoagent             禁用默认sun.tools.debug调试器。
      -Djava.compiler=NONE  禁止 JIT 编译器的加载。
      -Xrunjdwp             加载JDWP的 JPDA 参考执行实例。
      transport             用于在调试程序和 VM 使用的进程之间通讯。
      dt_socket              socket 传输。
      dt_shmem              共享内存传输，仅限于 Windows。
      server=y/n            VM 是否需要作为调试服务器执行。
      address=3999          调试服务器的端口号，客户端用来连接服务器的端口号。
      suspend=y/n           是否在调试客户端建立连接之后启动 VM 。
  
  
    Resin:
 RESIN_HOMEbinhttpd.exe -Xdebug -Xrunjdwp:transport=dt_socket,address=5005,server=y,suspend=n
  
    Tomcat:
 在catalina.sh/bat 的最上面加上: SET CATALINA_OPTS=-server -Xdebug -Xnoagent -Djava.compiler=NONE -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=5005 即可。
  
    Weblogic:
 在startWebLogic.bat加上: set JAVA_OPTIONS=-Xdebug -Xnoagent -Djava.compiler=NONE -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=5005
  
    启动App server后，在ide下通过debug remote java application并侦听相应的debug端口
  
  
    Eclipse Rcp:
  
  
    java -Xdebug -Xnoagent -Djava.compiler=NONE -Xrunjdwp:transport=dt_socket,suspend=y,server=y,address=8000 -cp F:/rcp/plugins/org.eclipse.equinox.launcher_1.0.0.v20070606.jar org.eclipse.equinox.launcher.Main -application rcp.application -data F:/rcp/workspace -os win32 -ws win32 -arch x86 -nl en_US
  
  
    -Xdebug -Xnoagent等参数需要放在main class前面

## mvnDebug

在maven上debug，经常跟jetty或tomcat插件在一起使用。如运行mvnDebug jetty:run命令后再通过eclipse远程连接调试。

```bash
mvnDebug jetty:run
# 默认调试端口8000
```

maven 的安装目录下存在 mvnDebug.bat 文件，打开可以看到具体的配置项如下:

set MAVEN_DEBUG_OPTS=-Xdebug -Xnoagent -Djava.compiler=NONE -Xrunjdwp:transport=dt_socket,server=y,suspend=y,address=8000

这里对几个参数进行说明:
  
- -Xdebug :   启动debug模式
  
- -Xnoagent:   禁用默认sun.tools.debug调试器
  
- -Djava.compiler: 指定编译器类型，可方便优化 jitc jitc_de等
  
- -Xrunjdwp: 启动调试协议JDWP，全称是Java Debug Wire Protocol，它定义了JPDA front-end和JPDA back-end之间通讯信息的二进制格式。这里的通讯信息主要包括两种: 调试器发送给JVM的请求信息和JVM发送给调试器的调试信息。有如下子项:

- -transport: JPDA front-end和back-end之间的传输方法。dt_socket表示使用 socket 传输。

- -server: y/n 该jvm是被调试者还是调试器

- -suspend: y/n 是否等待外部调试器的连接，如jetty启动时候，是否等待eclipse的远程连接后在进行jetty的初始化工作。在调试web容器的时候用的很多

- -address: 监听端口

mvnDebug 默认配置 -suspend:y , 启动jetty:run 之后命令行会显示

```bash
application prints "Listening for transport dt_socket at address: 8000" and does not halt
```

此时在idea中启动调试连接到8000端口即可.

### mvn debug

```bash
# linux
export MAVEN_OPTS="-Xdebug -Xnoagent -Djava.compiler=NONE -Xrunjdwp:transport=dt_socket,address=5005,server=y,suspend=n"
# windows
set MAVEN_OPTS="-Xdebug -Xnoagent -Djava.compiler=NONE -Xrunjdwp:transport=dt_socket,address=5005,server=y,suspend=n"

# 在命令行导入以上参数然后执行
mvn jetty:run
```

————————————————
  
版权声明: 本文为CSDN博主「wxy_fighting」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
  
原文链接: <https://blog.csdn.net/wxyFighting/article/details/9408153>

### Java JPDA

JPDA 全称: Java Platform Debugger Architecture (Java调试器架构)。是一套Java虚拟机自带的调试体系。
JPDA 定义了一个完整独立的体系，它由三个相对独立的层次共同组成，而且规定了它们三者之间的交互方式，或者说定义了它们通信的接口。这三个层次由低到高分别是 Java 虚拟机工具接口 (JVMTI) ，Java 调试线协议 (JDWP) 以及 Java 调试接口 (JDI) 。这三个模块把调试过程分解成几个很自然的概念: 调试者 (debugger) 和被调试者 (debuggee) ，以及他们中间的通信器。被调试者运行于我们想调试的 Java 虚拟机之上，它可以通过 JVMTI 这个标准接口，监控当前虚拟机的信息；调试者定义了用户可使用的调试接口，通过这些接口，用户可以对被调试虚拟机发送调试命令，同时调试者接受并显示调试结果。在调试者和被调试着之间，调试命令和调试结果，都是通过 JDWP 的通讯协议传输的。所有的命令被封装成 JDWP 命令包，通过传输层发送给被调试者，被调试者接收到 JDWP 命令包后，解析这个命令并转化为 JVMTI 的调用，在被调试者上运行。类似的，JVMTI 的运行结果，被格式化成 JDWP 数据包，发送给调试者并返回给 JDI 调用。而调试器开发人员就是通过 JDI 得到数据，发出指令

#### Java 虚拟机工具接口 (JVMTI)

定义VM(虚拟机)的调试服务 JVM TI(Java VM Tool Interface)。该组件提供了查看Java所有状态的职责。包括但不限于: JVM分析，监控，调试，线程分析，以及覆盖率分析等功能。其由JVM提供，与具体语言无关.  
JVMTI (Java Virtual Machine Tool Interface) 即指 Java 虚拟机工具接口，它是一套由虚拟机直接提供的 native 接口，它处于整个 JPDA 体系的最底层，所有调试功能本质上都需要通过 JVMTI 来提供。通过这些接口，开发人员不仅调试在该虚拟机上运行的 Java 程序，还能查看它们运行的状态，设置回调函数，控制某些环境变量，从而优化程序性能。我们知道，JVMTI 的前身是 JVMDI 和 JVMPI，它们原来分别被用于提供调试 Java 程序以及 Java 程序调节性能的功能。在 J2SE 5.0 之后 JDK 取代了 JVMDI 和 JVMPI 这两 socket ，JVMDI 在最新的 Java SE 6 中已经不提供支持，而 JVMPI 也计划在 Java SE 7 后被彻底取代。

#### Java 调试线协议 (JDWP)

定义调试器与调试者通信协议的 JDWP - Java Debug Wire Protocol。定义的主要是调试者与调试器通信时的传输信息以及请求数据格式。但不限制其传输机制。例如: 有的使用socket，有的使用serial line，有的使用share money 等等。
JDWP (Java Debug Wire Protocol) 是一个为 Java 调试而设计的一个通讯交互协议，它定义了调试器和被调试程序之间传递的信息的格式。在 JPDA 体系中，作为前端 (front-end) 的调试者 (debugger) 进程和后端 (back-end) 的被调试程序 (debuggee) 进程之间的交互数据的格式就是由 JDWP 来描述的，它详细完整地定义了请求命令、回应数据和错误代码，保证了前端和后端的 JVMTI 和 JDI 的通信通畅。比如在 Sun 公司提供的实现中，它提供了一个名为 jdwp.dll (jdwp.so) 的动态链接库文件，这个动态库文件实现了一个 Agent，它会负责解析前端发出的请求或者命令，并将其转化为 JVMTI 调用，然后将 JVMTI 函数的返回值封装成 JDWP 数据发还给后端。  

另外，这里需要注意的是 JDWP 本身并不包括传输层的实现，传输层需要独立实现，但是 JDWP 包括了和传输层交互的严格的定义，就是说，JDWP 协议虽然不规定我们是通过 EMS 还是快递运送货物的，但是它规定了我们传送的货物的摆放的方式。在 Sun 公司提供的 JDK 中，在传输层上，它提供了 socket 方式，以及在 Windows 上的 shared memory 方式。当然，传输层本身无非就是本机内进程间通信方式和远端通信方式，用户有兴趣也可以按 JDWP 的标准自己实现。

#### Java 调试接口 (JDI)

Java实现的Debug Interface 接口 JDI - Java Debug Interface。可以理解为Java语言实现的Debug Inteface，Java程序员可以直接使用其编写远程调试工具，有很多的IDEA的远程调试功能底层就是通过调用JDI接口实现的。  
JDI (Java Debug Interface) 是三个模块中最高层的接口，在多数的 JDK 中，它是由 Java 语言实现的。 JDI 由针对前端定义的接口组成，通过它，调试工具开发人员就能通过前端虚拟机上的调试器来远程操控后端虚拟机上被调试程序的运行，JDI 不仅能帮助开发人员格式化 JDWP 数据，而且还能为 JDWP 数据传输提供队列、缓存等优化服务。从理论上说，开发人员只需使用 JDWP 和 JVMTI 即可支持跨平台的远程调试，但是直接编写 JDWP 程序费时费力，而且效率不高。因此基于 Java 的 JDI 层的引入，简化了操作，提高了开发人员开发调试程序的效率。

对于 Java 虚拟机接口熟悉的人来说，您一定还记得 Java 提供了两个接口体系，JVMPI (Java Virtual Machine Profiler Interface) 和 JVMDI (Java Virtual Machine Debug Interface) ，而它们，以及在 Java SE 5 中准备代替它们的 JVMTI (Java Virtual Machine Tool Interface) ，都是 Java 平台调试体系 (Java Platform Debugger Architecture，JPDA) 的重要组成部分。 Java SE 自 1.2.2 版就开始推出 Java 平台调试体系结构 (JPDA) 工具集，而从 JDK 1.3.x 开始，Java SDK 就提供了对 Java 平台调试体系结构的直接支持。顾名思义，这个体系为开发人员提供了一整套用于调试 Java 程序的 API，是一套用于开发 Java 调试工具的接口和协议。本质上说，它是我们通向虚拟机，考察虚拟机运行态的一个通道，一套工具。理解这一点对于学习 JPDA 非常重要。

---

<https://developer.ibm.com/zh/articles/j-lo-jpda1/>#
<https://juejin.im/post/6844903855029747725>
<https://www.jianshu.com/p/f902ac5d29e4>
<https://blog.csdn.net/xlgen157387/article/details/50268457>
<http://blog.csdn.net/cchaha/article/details/3962502>
<http://hi.baidu.com/huamarco/blog/item/75c3f2a411e3ebf29152ee34.html>
<http://blog.csdn.net/zmxj/>
<http://www.blogjava.net/yongbing/articles/221179.html>

作者: 用户112986583106
链接: <https://juejin.im/post/6844903813141233671>
来源: 掘金
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
  
<http://dn.codegear.com/cn/article/33654>"><http://dn.codegear.com/cn/article/33654>
<http://www.eclipsezone.com/eclipse/forums/t53459.html>
<http://articles.techrepublic.com.com/5100-10878_11-6139512.html>
<http://www.lifevv.com/tenyo/doc/20070918003423784.html>

## JSR45, JPDA

JPDA（Java Platform Debugger Architecture）是Java平台调试体系结构的缩写。由3个规范组成，分别是JVMTI(JVM Tool Interface)，JDWP(Java Debug Wire Protocol)，JDI(Java Debug Interface) 。

1. JVMTI 定义了虚拟机应该提供的调试服务，包括调试信息（Information譬如栈信息）、调试行为（Action譬如客户端设置一个断点）和通知（Notification譬如到达某个断点时通知客户端），该接口由虚拟机实现者提供实现，并结合在虚拟机中
2. JDWP 定义调试服务和调试器之间的通信，包括定义调试信息格式和调试请求机制
3. JDI 在语言的高层次上定义了调试者可以使用的调试接口以能方便地与远程的调试服务进行交互，Java语言实现，调试器实现者可直接使用该接口访问虚拟机调试服务。 java调试工具jdb，就是sun公司提供的JDI实现。eclipse IDE，它的两个插件org.eclipse.jdt.debug.ui和org.eclipse.jdt.debug与其强大的调试功能密切相关，其中前者是eclipse调试工具界面的实现，而后者则是JDI的一个完整实现。

JAVA Debug 和 JSR-45

JPDA（Java Platform Debugger Architecture）

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
  
HttpServletResponse response) 22 throws java.io.IOException, ServletException { 23 24 JspFactory _jspxFactory = null; 25 PageContext pageContext = null; 26 HttpSession session = null; 27 ServletContext application = null; 28 ServletConfig config = null; 29 JspWriter out = null; 30 Object page = this; 31 JspWriter_jspx_out = null; 32 33 34 try { 35_jspxFactory = JspFactory.getDefaultFactory(); 36 response.setContentType("text/html"); 37 pageContext =_jspxFactory.getPageContext(this, request, response, 38 null, true, 8192, true); 39 application = pageContext.getServletContext(); 40 config = pageContext.getServletConfig(); 41 session = pageContext.getSession(); 42 out = pageContext.getOut(); 43_jspx_out = out; 44 45 out.write(" rn"); 46 out.write(" rn"); 50 out.write(" rn"); 51 out.write("Hello There!"); 52 out.write("

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

## Java 调试器（JDB）

Java™ 调试器 (JDB) 包含在 SDK 中。 该调试器通过 jdb 命令启动；它使用 JPDA 连接到 JVM。

要调试 Java 应用程序：
使用以下选项启动 JVM：
java -agentlib:jdwp=transport=dt_shmem,server=y,address=<port> <class>

JVM 启动，但在它启动 Java 应用程序之前将暂缓执行。
您可以在单独的会话中将调试器连接到 JVM：
jdb -attach <port>

调试器将连接到 JVM，您现在可以发出一系列命令来检查和控制 Java 应用程序；例如，输入 run 可以启动 Java 应用程序。
有关 JDB 选项的更多信息，请输入：
jdb -help

有关 JDB 命令的更多信息：
输入 jdb
在 jdb 提示符下，输入 help
还可以使用 JDB 来调试远程工作站上运行的 Java 应用程序。JPDA 使用 TCP/IP 套接字连接到远程 JVM。
使用以下选项启动 JVM：
java -agentlib:jdwp=transport=dt_shmem,server=y,address=<port> <class>

JVM 启动，但在它启动 Java 应用程序之前将暂缓执行。
将调试器连接到远程 JVM：
jdb -connect com.sun.jdi.SocketAttach:hostname=<host>,port=<port>

Java 虚拟机调试接口（JVMDI）在此发行版中不受支持。已将它替换为 Java 虚拟机工具接口（JVMTI）。

有关 JDB 和 JPDA 及其用法的更多信息，请参阅以下 Web 站点：
<http://www.oracle.com/technetwork/java/javase/tech/jpda-141715.html>
<https://docs.oracle.com/javase/7/docs/technotes/guides/jpda/>
<https://docs.oracle.com/javase/7/docs/technotes/guides/jpda/jdb.html>

<https://www.ibm.com/docs/zh/sdk-java-technology/7?topic=dja-java-debugger-jdb-1>
