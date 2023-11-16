---
title: java vs javaw vs javaws
author: "-"
date: 2015-01-22T12:17:18+00:00
url: javaws
categories:
  - Java
tags:
  - Java

---
## java vs javaw vs javaws

[http://javapapers.com/core-java/java-vs-javaw-vs-javaws/](http://javapapers.com/core-java/java-vs-javaw-vs-javaws/)

This article gives an awareness tip. Do you know the difference between java, javaw and javaws tools. All these three are java application launchers.
We know well about java.exe which we use quite often. Our command line friend, mostly we use it for convenience to execute small java programs. javaw is rare for us. Sometimes we have seen that in running application list in windows task manager. javaws is web start utility.

### jvm.dll

We need to know about jvm.dll also. This is the actual java virtual machine implementation in windows environment and it is part of the JRE. A 'C' program can use this jvm.dll directly to run the jvm.

java.exe
  
java.exe is a Win32 console application. This is provided as a helper so that, instead of using jvm.dll we can execute java classes. As it is a Win32 console application, obviously it is associated with a console and it launches it when executed.

javaw.exe
  
javaw.exe is very similar to java.exe. It can be considered as a parallel twin. It is a Win32 GUI application. This is provided as a helper so that application launches its own GUI window and will not launch a console. Whenever we want to run a GUI based application and don't require a command console, we can use this as application launcher. For example to launch Eclipse this javaw.exe is used. Write a small java hello world program and run it as "javaw HelloWorld" using a command prompt. Silence! nothing happens then how do I ensure it. Write the same using Swing and execute it you will see the GUI launched. For the lazy to ensure that it is same as java.exe (only difference is console) "javaw HelloWorld >> output.txt". It silently interprets and pushes the output to the text file.

import javax.swing.*;

public class HelloWorldSwing {
  
private static void createAndShowGUI() {
  
JFrame jFrame = new JFrame("HelloWorld Swing");
  
jFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
  
JLabel helloLabel = new JLabel("Hello World!");
  
jFrame.getContentPane().add(helloLabel);
  
jFrame.pack();
  
jFrame.setVisible(true);
  
}

public static void main(String[] args) {
  
javax.swing.SwingUtilities.invokeLater(new Runnable() {
  
public void run() {
  
createAndShowGUI();
  
}
  
});
  
}
  
}
  
We can execute the above GUI application using both java.exe and javaw.exe If we launch using java.exe, the command-line waits for the application response till it closes. When launched using javaw, the application launches and the command line exits immediately and ready for next command.

javaws.exe
  
javaws.exe is used to launch a java application that is distributed through web. We have a jnlp_url associated with such application. We can use as "javaws jnlp_url" to launch the application. It downloads the application from the url and launches it. It is useful to distribute application to users and gives central control to provide updates and ensures all the users are using the latest software. When the application is invoked, it is cached in the local computer. Every time it is launched, it checks if there is any update available from the distributor.

This Core Java tutorial was added on 07/08/2012.

### JNLP

JNLP (Java Network Launching Protocol ）是java提供的一种可以通过浏览器直接执行java应用程序的途径，它使你可以直接通过一个网页上的url连接打开一个java应用程序。
Java桌面应用程序以JNLP 的方式发布，如果版本升级后，不需要再向所有用户发布版本，只需要更新服务器的版本，这就相当于让java应用程序有了web应用的优点。

JNLP (全称Java Network Launch Protocol）意为Java网络装载协议。JNLP是一为Java Web Start应用程序提供基本的元素和描述的XML文件。JNLP是Java Web Start的核心。
JNLP应用程序能使应用程序像标准的JAVA Applet一样通过WEB浏览器访问，并且在客户机主机上JNLP可以限制为一个安全的“沙箱(sandbox)”.不像Applets，JNLP应用程序不运行的客户的浏览器内部；相反，WEB浏览器只作为应用程序的一个起点或安装工具。
JAVA桌面应用程序以JNLP 的方式发布，如果版本升级后，不需要再向所有用户发布版本，只需要更新服务器的版本，这就相当于让java应用程序有了web应用的优点。

>[https://www.cnblogs.com/bro-ma/p/10684789.html](https://www.cnblogs.com/bro-ma/p/10684789.html)

### Java Web Start

Java Web Start是帮助客户机端应用程序开发的一个新技术，该技术的独特之处在于将你关心客户机是如何启动 (从Web浏览器或是桌面）中解放出来。并且，该技术提供了一个使Web服务器能独立发布和更新客户机代码的集合部署方案。
Java Web Start是一个软件技术，它包含了applet的可移植性、Servlet和Java Server Pages (JSP）的可维护性以及象XML和HTML这样的标记语言的简易性。它是基于Java的应用程序，允许从标准的Web服务器启动、部署和更新功能完成的Java 2客户机应用程序。
Java Web Start自身是一个Java应用程序，所以该软件是平台独立的，并且支持Java2平台的任何客户机系统都支持该软件。当客户机应用程序启动时，Java Web Start自动执行更新，在从原来的高速缓存装入应用程序的同时，从Web下载罪行的版本。Java Web Start还提供了一个Java应用程序管理器 (Java Application Manager）实用程序，即提供了多种选项，如清除下载的应用程序的高速缓存、指定多种JRE的使用，设置HTTP代理、还允许最终用户组织他们的Java应用程序。
Java Web Start站点：
[http://java.sun.com/javase/technologies/desktop/javawebstart/index.jsp](http://java.sun.com/javase/technologies/desktop/javawebstart/index.jsp)
JNPL规范：[http://jcp.org/en/jsr/detail?id=056](http://jcp.org/en/jsr/detail?id=056)
