---
title: JAVA读取文件的两种方法 JAVA.IO和JAVA.LANG.CLASSLOADER
author: "-"
date: 2013-01-03T03:40:04+00:00
url: /?p=4961
categories:
  - Java
tags:
  - reprint
---
## java 文件 

    Files.exists()：检测文件路径是否存在。

    Files.createFile()：创建文件。

    Files.createDirectory()：创建文件夹。

    Files.delete()：删除一个文件或目录。

    Files.copy()：复制文件。

    Files.move()：移动文件。

    Files.size()：查看文件个数。

    Files.read()：读取文件。

    Files.write()：写入文件。

## JAVA读取文件的两种方法 JAVA.IO和JAVA.LANG.CLASSLOADER
http://www.blogjava.net/flysky19/articles/93280.html

java读取文件的两种方法: java.io和java.lang.ClassLoader什么时候使用java.io,什么时候使用java.lang.ClassLoader呢？

 (注: 要是之前读xml文件时清晰知道java读取文件有这两种方法就好了！可以少走很多去理解相对路径的弯路！) 

自己的总结: 
  
*java.io:相对于当前用户目录的相对路径读取；注重与磁盘文件打交道或者纯java project中使用。
  
 (虽然ClassLoader方式更通用,但是如果不是javaEE环境,要定位到classpath路径下去读文件是不合理的。) 

*java.lang.ClassLoader:相对于classpath的相对路径读取；建议在javaEE环境中都使用这种方式。

整理资料一: http://www.code168.com/bbs/html/2005-12-9/23554625833.html
  
问: 
  
java打成jar包的后续问题！！！！如何在读取jar包里面的配置文件？
  
答1: 
  
如果用java.util.ResourceBundle就不用担心什么,它本来就是从class loader folder/jar文件里找
  
properties文件。
  
如果你已经注意到了,java取文件有两种方法,java.util.io和java.lang.ClassLoader两种。
  
java.io:

File file = new File("...");
   
FileInputStream fis = new FileInputStream("...");
   
FileReader fr = new FileReader("...");

ClassLoader:
  
ClassLoader loader = XXXClass.class.getClassLoader();
   
ClassLoader loader = Thread.currentThread().getContextClassLoader();
   
URL url = loader.getResource("...");
   
File file = new File(url.getFile());
   
InputStream input = loader.getResourceAsStream("...");

这两种,一种是从project loader folder取,一种是从class loader folder取,class loader
  
folder包括jar文件。
  
我想你应该明白了吧？自己写个程序test一下就知道了。

答2: 
  
File file = new File(url.getFile());不是用在你这种情况的。
  
一般情况既然classloader已经拿到resource,就没有必要画蛇添足地再转成File.
  
转成File事实上是为了拿到绝对路径,我们碰到过这么一种情况。
  
一个Web application,用tomcat启动,tomcat会建一个application folder,folder下面有一个web-inf

folder,再下面是classes目录,classes目录下面是所有的java classes.程序需要用一个property文件记录数据,用io package只能定位到绝对路径,用class loader可以是相对路径,不管tomcat在客户电

脑上任何位置,但是,如果写文件在classes folder下面,tomcat会reload web server,页面会重载。为了定位到application folder,与web-inf并列,先用classloader,再转成file拿到全路径,去掉后

面不需要的folder,就可以拿到 tomecat建的web application的绝对路径。
  
与你的情况不同的是,classloader定位到的文件,不在jar里头。我认为用java io不可以定到jar里面。

整理资料二: 
  
Java路径问题最终解决方案
  
http://www.matrix.org.cn/thread.shtml?topicId=6d0bbeed-9157-11db-ab77-2bbe780ebfbf&forumId=19

一、相对于当前用户目录的相对路径
  
就是相对于System.getProperty("user.dir")返回的路径。
  
对于一般项目,这是项目的根路径。对于JavaEE服务器,这可能是服务器的某个路径。这个并没有统一的

规范！
  
所以,绝对不要使用"相对于当前用户目录的相对路径"。然而: 
  
默认情况下,java.io 包中的类总是根据当前用户目录来分析相对路径名。此目录由系统属性 user.dir指定,通常是 Java 虚拟机的调用目录。
  
这就是说,在使用java.io包中的类时,最好不要使用相对路径。否则,虽然在J2SE应用程序中可能还算正常,但是到了J2EE程序中,一定会出问题！而且这个路径,在不同的服务器中都是不同的！

二、相对于classpath的相对路径
  
如: 相对于
  
file:/D:/java/eclipse32/workspace/jbpmtest3/bin/这个路径的相对路径。其中,bin是本项目的classpath。所有的Java源文件编译后的.class文件复制到这个目录中。

三、相对路径最佳实践
  
推荐使用相对于当前classpath的相对路径
  
因此,我们在使用相对路径时,应当使用相对于当前classpath的相对路径。
  
ClassLoader类的getResource(String name),getResourceAsStream(String name)等方法,使用相对于当

前项目的classpath的相对路径来查找资源。
  
读取属性文件常用到的ResourceBundle类的getBundle(String path)也是如此。
  
通过查看ClassLoader类及其相关类的源代码,我发现,它实际上还是使用了URI形式的绝对路径。通过得

到当前classpath的URI形式的绝对路径,构建了相对路径的URI形式的绝对路径。 (这个实际上是猜想,因为JDK内部调用了SUN的源代码,而这些代码不属于JDK,不是开源的。) 

四、相对路径本质上还是绝对路径
  
因此,归根结底,Java本质上只能使用绝对路径来寻找资源。所有的相对路径寻找资源的方法,都不过是

一些便利方法。不过是API在底层帮助我们构建了绝对路径,从而找到资源的！