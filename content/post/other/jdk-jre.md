---
title: JRE和JDK的区别
author: "-"
date: 2013-10-20T04:59:53+00:00
url: jdk-jre
categories:
  - java
tags:
  - java

---
## JRE和JDK的区别

### JDK

JDK 是整个Java的核心,包括了Java运行环境(JRE) (Java Runtime Envirnment), 一堆Java工具和Java基础的类库 (rt.jar) 。不论什么Java应用服务器实质都是内置了某个版本的JDK.最主流的JDK是Sun公司发布的JDK,除了Sun之外,还有很多公司和组织都开发了自己的JDK,例如IBM公司开发的JDK,BEA公司的Jrocket,还有GNU组织开发的JDK等等。其中IBM的JDK包含的JVM (Java Virtual Machine) 运行效率要比Sun JDK包含的JVM高出许多。而专门运行在x86平台的Jrocket在服务端运行效率也要比Sun JDK好很多。但不管怎么说,我们还是需要先把Sun JDK掌握好。

JDK一般有三种版本: SE (J2SE) ,standard edition,标准版,是我们通常用的一个版本EE (J2EE) ,enterpsise edtion,企业版,使用这种JDK开发J2EE应用程序,ME (J2ME) ,micro edtion,主要用于移动设备、嵌入式设备上的java应用程序Java开发工具 (JDK) 是许多Java专家最初使用的开发环境。尽管许多编程人员已经使用第三方的开发工具,但JDK仍被当作Java开发的重要工具。JDK由一个标准类库和一组建立,测试及建立文档的Java实用程序组成。其核心Java API是一些预定义的类库,开发人员需要用这些类来访问Java语言的功能。Java API包括一些重要的语言结构以及基本图形,网络和文件I/O.一般来说,Java API的非I/O部分对于运行Java的所有平台是相同的,而I/O部分则仅在通用Java环境中实现。

作为JDK实用程序,工具库中有七种主要程序。

◆Javac: Java编译器,将Java源代码转换成字节码。

◆Java: Java解释器,直接从类文件执行Java应用程序字节代码。

◆appletviewer: 小程序浏览器,一种执行HTML文件上的Java小程序的Java浏览器。 (chrome, firefox 不再支持NPAPI) 

◆Javadoc: 根据Java源码及说明语句生成HTML文档。

◆Jdb: Java调试器,可以逐行执行程序,设置断点和检查变量。

◆Javah: 产生可以调用Java过程的C过程,或建立能被Java程序调用的C过程的头文件。
javah命令主要用于在JNI开发的时,把java代码声明的JNI方法转化成C\C++头文件,以便进行JNI的C\C++端程序的开发。

但是需要注意的是javah命令对Android编译生成的类文件并不能正常工作。如果对于Android的JNI要想生成C\C++头文件的话,可能只有先写个纯的java代码来进行JNI定义,接着用JDK编译,然后再用javah命令生成JNI的C\C++头文件。当然你也可以不用javah命令,直接手写JNI的C\C++头文件。

使用javah或javah -help将看到javah命令的语法信息。
◆Javap: Java反汇编器,显示编译类文件中的可访问功能和数据,同时显示字节代码含义。

### JRE

JRE (Java Runtime Environment,Java运行环境) ,运行JAVA程序所必须的环境的集合,包含JVM标准实现及Java核心类库。是Sun的产品,包括两部分: JavaRuntimeEnvironment和JavaPlug-inJavaRuntimeEnvironment (JRE) 是可以在其上运行、测试和传输应用程序的Java平台。它包括Java虚拟机、Java平台核心类和支持文件。它不包含开发工具——编译器、调试器和其它工具。JRE需要辅助软件 ——JavaPlug-in——以便在浏览器中运行applet.J2RE是Java2 Runtime Environment,即Java运行环境,有时简称JRE.如果你只需要运行Java程序或Applet,下载并安装它即可。如果你要自行开发 Java软件,请下载JDK.在JDK中附带有JRE.注意由于Microsoft对Java的支持不完全,请不要使用IE自带的虚拟机来运行 Applet,务必安装一个JRE或JDK.