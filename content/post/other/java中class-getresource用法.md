---
title: java中Class.getResource用法
author: "-"
date: 2012-01-02T09:21:16+00:00
url: /?p=642
categories:
  - Java
tags:
  - Java

---
## java中Class.getResource用法

用JAVA获取文件，听似简单，但对于很多像我这样的新人来说，还是掌握颇浅，用起来感觉颇深，大常最经常用的，就是用JAVA的File类，如要取得c:/test.txt文件，就会这样用File file = new File("c:/test.txt");这样用有什么问题，相信大家都知道，就是路径硬编码，对于JAVA精神来说，应用应该一次成型，到处可用，并且从现实应用来讲，最终生成的应用也会部署到Windows外的操作系统中，对于linux来说，在应用中用了c:/这样的字样，就是失败，所以，我们应该尽量避免使用硬编码，即直接使用绝对路径。

在Servlet应用中，有一个getRealPath(String str)的方法，这个方法尽管也可以动态地获得文件的路径，不秘直接手写绝对路径，但这也是一个不被建议使用的方法，那么，我们有什么方法可以更好地获得文件呢?

那就是Class.getResource()与Class.getResourceAsStream()方法，但很多人还是不太懂它的用法，因为很多人 (比如不久前的我) 都不知道应该传怎么样的参数给它，当然，有些人己经用得如火纯青，这些人是不需要照顾的，在此仅给不会或者还不是很熟的人解释一点点。

比如我们有以下目录
  
|-project
  
|-src
  
|-javaapplication
  
|-Test.java
  
|-file1.txt
  
|-file2.txt
  
|-build
  
|-javaapplication
  
|-Test.class
  
|-file3.txt
  
|-file4.txt

在上面的目录中，有一个src目录，这是JAVA源文件的目录，有一个build目录，这是JAVA编译后文件(.class文件等) 的存放目录
  
那么，我们在Test类中应该如何分别获得
  
file1.txt file2.txt file3.txt file4.txt这四个文件呢？

首先讲file3.txt与file4.txt
  
file3.txt:
  
方法一: File file3 = new File(Test.class.getResource("file3.txt").getFile());
  
方法二: File file3 = new File(Test.class.getResource("/javaapplication/file3.txt").getFile());
  
方法三: File file3 = new File(Test.class.getClassLoader().getResource("javaapplication/file3.txt").getFile());

file4.txt:
  
方法一: File file4 = new File(Test.class.getResource("/file4.txt").getFile());
  
方法二: File file4 = new File(Test.class.getClassLoader().getResource("file4.txt").getFile());

很好，我们可以有多种方法选择，但是file1与file2文件呢？如何获得？
  
答案是，你只能写上它们的绝对路径，不能像file3与file4一样用class.getResource()这种方法获得，它们的获取方法如下
  
假如整个project目录放在c:/下，那么file1与file2的获取方法分别为
  
file1.txt
  
方法一: File file1 = new File("c:/project/src/javaapplication/file1.txt");
  
方法二: 。。。没有

file2.txt
  
方法一: File file2 = new File("c:/project/src/file2.txt");
  
方法二: 。。。也没有

总结一下，就是你想获得文件，你得从最终生成的.class文件为着手点，不要以.java文件的路径为出发点，因为真正使用的就是.class，不会拿个.java文件就使用，因为java是编译型语言嘛

至于getResouce()方法的参数，你以class为出发点，再结合相对路径的概念，就可以准确地定位资源文件了，至于它的根目录嘛，你用不同的IDE build出来是不同的位置下的，不过都是以顶层package作为根目录，比如在Web应用中，有一个WEB-INF的目录，WEB-INF目录里面除了web.xml文件外，还有一个classes目录，没错了，它就是你这个WEB应用的package的顶层目录，也是所有.class的根目录"/"，假如clasaes目录下面有一个file.txt文件，它的相对路径就是"/file.txt"，如果相对路径不是以"/"开头，那么它就是相对于.class的路径。。

还有一个getResourceAsStream()方法，参数是与getResouce()方法是一样的，它相当于你用getResource()取得File文件后，再new InputStream(file)一样的结果


```java
    //java getResource

    URL url= Thread.currentThread().getContextClassLoader().getResource("XXX");

    String fileName = this.getClass().getClassLoader().getResource("文件名").getPath();//获取文件路径
    String fileUtl = this.getClass().getResource("文件名").getFile();
     (在项目打成jar后的情况下getPath()与getFile()返回参数及用法的基本相同具体差异大研究) 
    示例路径结果: /E:/idea_work/sofn-qry-web/target/classes/CityJson.js

    //console read

    System.in.read();
```


方式二: 
File directory = new File("");//参数为空
String courseFile = directory.getCanonicalPath()//标准的路径 ;
String author =directory.getAbsolutePath()//绝对路径;
 (在jdk1.1后就有了此方法获取文件路径的方式存在了) 
示例路径结果: E:\idea_work\sofn-qry-web

方式三: 
java.net.URL uri = this.getClass().getResource("/");
 (获取到Class文件存放的路径) 
示例路径结果: file:/E:/idea_work/sofn-qry-web/target/test-classes/


String property =System.getProperty("user.dir");
方式四: 

String property =System.getProperty("user.dir");
 (此方法可以得到该工程项目所有文件的相关路径及环境配置信息) 
示例输出结果: 

