---
title: JAR	WAR EAR
author: "-"
date: 2012-04-08T12:17:35+00:00
url: /?p=2879
categories:
  - Java

tags:
  - reprint
---
## JAR	WAR EAR
### jar: Java Archive file  
扩展名为.Jar 包含Java类的普通库(class)、资源 (resources) 、辅助文件 (auxiliary files) , properties 等部署文件 application-client.xml

JAR: Software developers generally use .jar files to distribute Java applications or libraries, in the form. of classes and associated metadata and resources (text, images, etc.) JAR files build on the ZIP file format.


#### 查看jar归档目录
    jar -vtf xxx.jar


### war: Web Archive file/web application archive
扩展名为.War, 包含全部Web应用程序, Servlet、JSP、JSP标记库、JAR库文件、HTML/XML文档和其他公用资源文件,图片、音频. 一个Web应用程序被定义为单独的一组文件、类和资源，用户可以对jar文件进行封装，并把它作为小型服务程序 (servlet) 来访问。

部署文件: web.xml

ear: Enterprise Archive file

扩展名为.Ear 包含全部企业应用程序:  JAR、WAR，EJB组件。一个企业应用程序被定义为多个jar文件、资源、类和Web应用程序的集合。

部署文件: application.xml

jar:封装类
  
war:封装web站点
  
ear:可以封装ejb

    jar <war <ear


  
WAR: In computing, a WAR file (which stands for "web application archive" ) is a JAR file used to distribute a collection of JavaServer Pages, servlets, Java classes, XML files, tag libraries and static Web pages (HTML and related files) that together constitute a Web application.
  
EAR: An Enterprise Archive, or EAR, is a file format used by Java EE for packaging one or more modules into a single archive so that the deployment of the various modules onto an application server happens simultaneously and coherently. It also contains XML files called deployment descriptors which describe how to deploy the modules. Maven or Ant can be used to build EAR files.
  
RAR: A Resource Adapter is an archive file format defined in the J2EE Connector Architecture (JCA) specification. A Resource Adapter aRchive (RAR) file is the valid format for deployment of resource adapters on application servers. J2EE RAR files may also be called connectors.

EJB: Enterprise JavaBeans (EJB) is a managed, server-side component architecture for modular construction of enterprise applications. The EJB specification is one of several Java APIs in the Java EE. EJB is a server-side model that encapsulates the business logic of an application.
  
JavaBean: JavaBeans are reusable software components for Java that can be manipulated visually in a builder tool. Practically, they are classes written in the Java programming language conforming to a particular convention. They are used to encapsulate many objects into a single object (the bean), so that they can be passed around as a single bean object instead of as multiple individual objects. A JavaBean is a Java Object that is serializable, has a nullary constructor, and allows access to properties using getter and setter methods.
  
Metadata: Metadata is a means to describe the data files.It provides information about a certain item's content, such as: means of creation, purpose of the data, time and date of creation, creator or author of data, placement on a network (electronic form) where the data was created, what standards used (ISO9000), etc.

-

### JAR
EJB modules which contains enterprise java beans class files and EJB deployment descriptor are packed as JAR files with .jar extenstion
  
### WAR
Web modules which contains Servlet class files,JSP FIles,supporting files, GIF and HTML files are packaged as JAR file with .war( web achive) extension
  
### EAR
All above files(.jar and .war) are packaged as JAR file with .ear ( enterprise archive) extension and deployed into Application Server.

如果想生成war文件: 可以使用如下命令: jar -cvf web1.war *
  
如果想查看web1.war中都有哪些文件，可以使用命令: jar -tf web1.war
  
如果想直接解压web1.war文件，可以使用命令: jar -xvf web1.war
  
另外，也可使用winrar软件选择zip压缩方式，并将压缩文件后缀名改为war即可压缩生成war文件；同样使用winrar软件可以强行打开war 文件，或者强行解压war文件
  
使用jar命令与winrar软件的区别在于前者在压缩文件的同时会生成MetaINF文件夹，内包含MANIFEST.MF文件。

Every one knows, what you mean when you talk about a zip file. It is an archive for the stuff you want to compress and save or give to someone else. And, the fancy ones, allow you to maintain the directory structure of you multiple directories of files, when it gets to the other end.

Along the lines of evolution, the java community discovered that it would be easier to deploy their beloved lines of code, if they could pack it into a single compressed file format.

Their evolution created these terms that you have heard of:

#### <!-mstheme->
  
JAR files = collection of class files
  
WAR files = collection of class, JSP, XML files
  
EAR files = collection of JAR, WAR, and EJBs
  
<!-mstheme->

## JAR (Java ARchives)

It is really straight forward.
  
The JAR file is a Java Archive. The WAR file is a Web Archive. And finally, in the 21st century, the EAR file is, what else, and Enterprise Archive.

Very plain, and un-esoteric, when you really think about it. But, it is strange the first time through.

This world actually uses the terms archive and library interchangeably. All of the formats, are your program zipped with a directory structure. So, that if you give it to your friend or your friendly server, they both know where things belong, and your program will still run as it did on your computer.

The most basic archive is the JAR file. Normally is it is simply a compressed set of your java class files. When you run your java application, it knows were to find its parts, by referencing the structure. The normal.com.cezwright.myapp.starthere and the such. So, a JAR is either a complete application or it is just a set of utilities that you can call from your application.

The JAR file, is a bit more evolved that a plain archive or library, because it also can contain meta-data about the configuration of your application or even include a library that you want to or need to distribute with it.

The good news, is that you can call or access the classes in the JAR without needing to decompress them to the harddrive. They will run as is, by the magic of the java engine!

So, for simple classes you can use this format, which was the beginning of it all.

## <!-mstheme->WAR (Web ARchives) <!-mstheme->

Then, inorder to keep people from seeing your code, by viewing the source in your browser, someone invented JSPs. You write the JavaScript, but it is only visible on the server and not on the HTML page( that is why JSP was born).

This meant that you now hard more complicated information, that needed to be placed inside of the JAR. So, this gave birth to the next format on the evolutionary scale. The WAR file.

Now we have a structure that support JavaServer Pages and servlets. And, by the way, those things need to have HTML and some XML in them too. Oh, a web application archive structure.

Here we can upgrade the structure of the WAR file, and maintain a more complex conglomeration of things. And, the configuration information that a java server (container) would need to run it.

Then someone said, "Here lets keep the deployment stuff in there, and the application can self-deploy!"

technology came along, the need arose to package additional application objects such as JSPs, servlets, and HTML and XML files. Also, Java Web applications require more complex configuration information.

These new objects and complex configuration made the WAR file, the standard way to go. And things like Tomcat and Websphere were taught how to read and deploy them. No more long nights putting things together and placing them on the server, and pushing the (or clicking) the buttons.

Unlike the JAR file application, the server can not simply run the compressed file. And, the server **deploys** your application. So, when the server detects that either a new or updated war file has been saved to its special place, it will **extract** (_**expand**_) your entire application from the WAR archive to the server's web applications directory. And the directory structure, will look just like it did on your computer when you first created it. And now we are ready to run. The magic of auto deploy.

So now your entire web application is in one file. The WAR. The war is won.

## <!-mstheme->EAR (Enterprise ARchive) <!-mstheme->

Until, enter the enterprise!

These comparatively giant applications with a development environment called Java 2 Enterprise Edition. So, the EAR was born!

Now we can have Enterprise Java Beans, in the archive as well. Plus, we can still include multiple WAR and JAR files in this one single file.

No wonder, the java community loves ANT.


一、java的打包jar,war,ear包的作用，区别，打包方式.

a)         作用与区别

  1.                          i.              jar: 通常是开发时要引用通用(JAVA)类，打成包便于存放管理
  2.                        ii.              war: 是做好一个(web)应用后，通常是网站，打成包部署到容器中
  3.                       iii.              ear: 企业级应用，实际上EAR包中包含WAR包和几个企业级项目的配置文件而已，一般服务器选择WebSphere等，都会使用EAR包。通常是EJB打成ear包。

b)         打包方式

  1.                          i.              所有的包都是用jar打的，只不过目标文件的扩展名不一样
  2.                        ii.              也可以用Ant来安成构建

c)         JET编译成EXE

  1.                          i.              JET   是要用钱买的，而且据说   JET   也不是能把所有的   Java   程序都编译成执行文件，性能也要打些折扣。所以，使用制作可执行   JAR   文件包的方法就是最佳选择了，何况它还能保持   Java   的跨平台特性。

二、实例

方法一: 我现在有test/A.java
  
道理虽然简单，但是在这过程中还是有很多细节需要注意的，哪一个细节注意不到，操作都不会成功。


  
    
      package test;
 public class A{
 public static void main(String args[]){
 System.out.println("test java");
 }
 }
  

写好后，保存为A.java，存在D:Javajdk1.6test_jartest目录下面，打开cmd，进入这个目录，即D:Javajdk1.6test_jartest然后用javac命令编译，会生成一个A.class文件，此时类的编写工作已经完成。

2，在D:Javajdk1.6test_jar目录下新建一个文件夹META-INF，再新建mainclass.mf文件，在其中写入下面一行信息
  
Main-Class: com/hp/HelloWorld
  
这一句有两个注意的地方，首先行尾要有回车换行；其次":"和"com"之间要有一个空格。
  
这一行信息的作用是标明主类。

3，最后就是生成jar包并测试了，在cmd中进入D:Javajdk1.6test_jar目录，输入下列命令
  
jar cvfm test.jar META-INF/mainclass.mf test/A.class(**这是指定文件，当然也可以test指向文件夹)
  
**     上述命令执行成功的话，会提示"标明清单 (manifest) ..."，
  
然后再在当前目录下输入java -jar test.jar 命令，可以看到"test java"。

方法二: 
  
用简单的jar -cvf test.jar    test目录,jar会自动生成META-INF/mainclass.mf，我们只需要在里面去加一句 Main-Class: com/hp/HelloWorld
  
就可以了

方法三: myeclipse工具 (**推荐**) 
  
右击项目-Export-Jar File-要选择Main-Class

方法四: ant


http://www.blogjava.net/junky/archive/2006/05/21/47284.aspx

http://apps.hi.baidu.com/share/detail/30355098

<http://www.blogjava.net/xcp/archive/2012/02/01/351761.html>