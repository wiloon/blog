---
title: Maven OutOfMemory
author: "-"
date: 2012-05-08T03:34:21+00:00
url: /?p=3094
categories:
  - Inbox
tags:
  - reprint
---
## Maven OutOfMemory
  
    http://juvenshun.iteye.com/blog/240257
  


  
    当Maven项目很大，或者你运行诸如 mvn site 这样的命令的时候，maven运行需要很大的内存，在默认配置下，就可能遇到java的堆溢出。如: 
  
  
  
[INFO] Building jar: /home/dl9pf/svn/mindquarry/mindquarry-jcr/mindquarry-jcr-changes/target/mindquarry-migration-with-dependencies.jar
 [INFO] ------------------------
 [ERROR] FATAL ERROR
 [INFO] ------------------------
 [INFO] Java heap space
 [INFO] ------------------------
 [INFO] Trace
 java.lang.OutOfMemoryError: Java heap space
 at java.lang.AbstractStringBuilder.expandCapacity(AbstractStringBuilder.java:99)
 at java.lang.AbstractStringBuilder.append(AbstractStringBuilder.java:518)
 ...
 at org.codehaus.classworlds.Launcher.launchEnhanced(Launcher.java:315)
 at org.codehaus.classworlds.Launcher.launch(Launcher.java:255)
 at org.codehaus.classworlds.Launcher.mainWithExitCode(Launcher.java:430)
 at org.codehaus.classworlds.Launcher.main(Launcher.java:375)
 [INFO] ------------------------
 [INFO] Total time: 7 minutes 14 seconds
 [INFO] Finished at: Wed Sep 05 07:44:55 CEST 2007
 [INFO] Final Memory: 37M/63M
 [INFO] ------------------------
  
  
    解决的方法是调整java的堆大小的值。
  
  
    Windows环境中
  
  
    找到文件%M2_HOME%binmvn.bat ，这就是启动Maven的脚本文件，在该文件中你能看到有一行注释为: 
  
  
    @REM set MAVEN_OPTS=-Xdebug -Xnoagent -Djava.compiler=NONE...
  
  
    它的意思是你可以设置一些Maven参数，我们就在注释下面加入一行: 
  
  
  
    set MAVEN_OPTS= -Xms128m -Xmx512m
  
  
    之后，当你运行Maven命令如 mvn -version 的时候，你会看到如下的输出: 
  
  
  
    E:test>mvn -versionE:test>set MAVEN_OPTS= -Xms128m -Xmx512m
 Maven version: 2.0.9
 Java version: 1.6.0_07
 OS name: "windows 2003" version: "5.2" arch: "x86" Family: "windows"
  
  
    我们看到，配置的Maven选项生效了，OutOfMemoryError也能得以相应的解决。
  
  
    Linux环境中
  
  
    也可以通过设置环境变量解决该问题， 如，编辑文件 /etc/profile 如下
  
  
  
    MAVEN_OPTS=-Xmx512m
 export JAVA_HOME MAVEN_HOME MAVEN_OPTS JAVA_BIN PATH CLASSPATH
  
  
    如果你使用Hudson
  
  
    用 Hudson + Maven做持续集成，并不幸也遇到了类似的错误，那么上述两种方式都将不再起作用了，因为Hudson使用自己的maven-agent来启动Maven，不会去调用Maven的脚本，自然相应的配置也就无效了。
  
  
    好在Hudson也给为我们提供了配置点，在Hudson的项目配置页面中，有一块Build区域，这里我们已经设置了Root Pom和Goals。注意该区域的右下角有一个"Advanced..."按钮，点击会看到JVM Options输入框，这里输入"-Xmx1024m"就OK了。
  
  
    m2eclipse中
  
  
    类似以上的方法都会失效，所幸m2eclipse提供了配置点。步骤如下: 
  
  
    项目上右击 -> Run As -> Run Configurations -> Maven Build 上右击 -> New
  
  
    这时会看到一个maven运行配置对话框，这里面其它的配置我不多解释了，为了解决内存溢出的问题，我们可以选择第二个TAB: JRE，然后在VM arguments中输入配置如: -Xms128m -Xmx512m。
  
