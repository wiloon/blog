---
title: java vs javaw vs javaws
author: wiloon
type: post
date: 2015-01-22T12:17:18+00:00
url: /?p=7283
categories:
  - Uncategorized
tags:
  - Java

---
http://javapapers.com/core-java/java-vs-javaw-vs-javaws/

This article gives an awareness tip. Do you know the difference between java, javaw and javaws tools. All these three are java application launchers. We know well about java.exe which we use quite often. Our command line friend, mostly we use it for convenience to execute small java programs. javaw is rare for us. Sometimes we have seen that in running application list in windows task manager. javaws is web start utility.

jvm.dll
  
We need to know about jvm.dll also. This is the actual java virtual machine implementation in windows environment and it is part of the JRE. A 'C' program can use this jvm.dll directly to run the jvm.

java.exe
  
java.exe is a Win32 console application. This is provided as a helper so that, instead of using jvm.dll we can execute java classes. As it is a Win32 console application, obviously it is associated with a console and it launches it when executed.


javaw.exe
  
javaw.exe is very similar to java.exe. It can be considered as a parallel twin. It is a Win32 GUI application. This is provided as a helper so that application launches its own GUI window and will not launch a console. Whenever we want to run a GUI based application and don't require a command console, we can use this as application launcher. For example to launch Eclipse this javaw.exe is used. Write a small java hello world program and run it as “javaw HelloWorld” using a command prompt. Silence! nothing happens then how do I ensure it. Write the same using Swing and execute it you will see the GUI launched. For the lazy to ensure that it is same as java.exe (only difference is console) “javaw HelloWorld >> output.txt”. It silently interprets and pushes the output to the text file.

import javax.swing.*;

public class HelloWorldSwing {
  
private static void createAndShowGUI() {
  
JFrame jFrame = new JFrame("HelloWorld Swing");
  
jFrame.setDefaultCloseOperation(JFrame.EXIT\_ON\_CLOSE);
  
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
  
javaws.exe is used to launch a java application that is distributed through web. We have a jnlp\_url associated with such application. We can use as “javaws jnlp\_url” to launch the application. It downloads the application from the url and launches it. It is useful to distribute application to users and gives central control to provide updates and ensures all the users are using the latest software. When the application is invoked, it is cached in the local computer. Every time it is launched, it checks if there is any update available from the distributor.

This Core Java tutorial was added on 07/08/2012.