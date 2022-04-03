---
title: 'JAVA远程调试'
author: "-"
date: 2012-06-07T07:22:32+00:00
url: /?p=3435
categories:
  - Java

tags:
  - reprint
---
## 'JAVA远程调试'
JAVA自身支持调试功能，并提供了一个简单的调试工具－－JDB，类似于功能强大的GDB，JDB也是一个字符界面的调试环境，并支持设置断点，支持线程线级的调试。

JAVA的调试方法如下:     
首先设置JVM，并设置参数，使之工作在DEBUG模式下，加入参数: -Xdebug -Xrunjdwp,transport=dt_socket,server=y,address=5432,suspend=n,onthrow=java.io.IOException,launch=/sbin/echo    
-Xdebug 是通知JVM工作在DEBUG模式下  
-Xrunjdwp 是通知JVM使用(java debug wire protocol)来运行调试环境。该参数同时了一系列的调试选项:   
transport 指定了调试数据的传送方式，dt_socket是指用SOCKET模式，另有dt_shmem指用共享内存方式，其中，dt_shmem只适用于Windows平台。  
server 参数是指是否支持在server模式的JVM中.    
onthrow 指明，当产生该类型的Exception时，JVM就会中断下来，进行调式。该参数可选。  
launch 指明，当JVM被中断下来时，执行的可执行程序。该参数可选  
suspend 指明，是否在调试客户端建立起来后，再执行JVM。  
onuncaught(=y或n) 指明出现uncaught exception 后，是否中断JVM的执行.  

启动调试工具。  
最简单的调试工具就是上面提到的JDB，以上述调试用JVM为例，可以用下面的命运行启动JDB:   

    jdb -connect com.sun.jdi.SocketAttach:port=5432,hostname=192.168.11.213
  
另外，还有好多的可视化调试工具，如 IDEA, eclipse,jsawt等等。Eclipses可用 ant debug来建立一个调试方法。  
其实就是使用了JDK的JPDA，在启动服务器 (Jboss或者Tomcat等) 的命令行参数里面加上:   
-Xdebug -Xrunjdwp:transport=dt_socket,address=8787,server=y,suspend=n

## tomcat
何为远程调试？我们一般调试一个 web项目的java代码时，需要将你的tomcat服务器和你的开发工具 (比如Jbuilder) 集成，或需要工具的一些插件支持(比如Eclipse 下的myclipse等)，这些方式都是在本地进行，即你的开发工具和tomcat运行在同一台服务器上，如果你的开发工具和服务器不再一台机器上那就需要实现远程调试功能了。

### tomcat
在tomcat/bin下的catalina.sh上边添加下边的JPDA参数

    CATALINA_OPTS="-Xdebug -Xrunjdwp:transport=dt_socket,address=5005,suspend=n,server=y"

### IDEA设置
      Edit Configuration > Add new configuration > remote
      command line arguments for remote JVM: -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005

#### use module classpath:
    选择源码所在的工程

**注意防火墙要开启相关端口**


#### Java远程调试 {#subjcns!30EBEBD8BCD440DC!158}


  
    -Xdebug -Xnoagent -Djava.compiler=NONE -Xrunjdwp:transport=dt_socket,server=y,address=3999,suspend=n
  
  
      -XDebug               启用调试。
      -Xnoagent             禁用默认sun.tools.debug调试器。
      -Djava.compiler=NONE  禁止 JIT 编译器的加载。
      -Xrunjdwp             加载JDWP的JPDA参考执行实例。
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

https://developer.ibm.com/zh/articles/j-lo-jpda1/#
https://juejin.im/post/6844903855029747725
https://www.jianshu.com/p/f902ac5d29e4
https://blog.csdn.net/xlgen157387/article/details/50268457
<http://blog.csdn.net/cchaha/article/details/3962502>
http://hi.baidu.com/huamarco/blog/item/75c3f2a411e3ebf29152ee34.html
http://blog.csdn.net/zmxj/
<http://www.blogjava.net/yongbing/articles/221179.html>

作者: 用户112986583106
链接: https://juejin.im/post/6844903813141233671
来源: 掘金
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
  
http://dn.codegear.com/cn/article/33654">http://dn.codegear.com/cn/article/33654
http://www.eclipsezone.com/eclipse/forums/t53459.html
http://articles.techrepublic.com.com/5100-10878_11-6139512.html
http://www.lifevv.com/tenyo/doc/20070918003423784.html
