---
title: Hsqldb
author: "-"
date: 2013-02-23T07:07:54+00:00
url: /?p=5235
categories:
  - DataBase
tags:$
  - reprint
---
## Hsqldb
Hsqldb是一个开放源代码的JAVA数据库，其具有标准的SQL语法和JAVA接口，

  在HSQLDB中,有三种比较常用模式:

### 服务器模式

  Server模式提供了最大的可访问性。应用程序 (客户端) 通过Hsqldb的JDBC驱动连接服务器。在服务器模式中，服务器在运行的时候可以被指定为最多10个数据库。根据客户端和服务器之间通信协议的不同，Server模式可以分为以下三种: 


  1、 Hsqldb Serve


  这种模式是首选的也是最快的。它采用HSQLDB专有的通信协议。启动服务器需要编写批处理命令。Hsqldb提供的所有工具都能以java class归档文件(也就是jar)的标准方式运行。假如hsqldb.jar位于相对于当前路径的../lib下面。我们的命令将这样写: 


  java -cp ../lib/hsqldb.jar org.hsqldb.Server -database.0 mydb -dbname.0 demoDB


  现在你可能会疑惑，[-database.0 ]、 [dbname.0]为什么在后面加[0]。_... ...我们不是在前面说服务模式运行的时候可以指定10个数据库吗，如有多个数据库，则继续写命令行参数-database.1 aa -dbname.1 aa -database.2 bb-dbname.2 bb ... ...


  新建文本文件保存上面命令，文件名可以随意，将后缀名改成bat，然后直接执行批处理文件即可。在以后介绍的执行启动工具的命令采用同样方法。


  上面启动服务器的命令启动了带有一个 (默认为一个数据库) 数据库的服务器，这个数据库是一个名为"mydb.*"文件，这些文件就是mydb.Properties、mydb.script、mydb.log等文件。其中demoDB是mydb的别名，可在连接数据库时使用。


  2、 Hsqldb Web Server


  这种模式只能用在通过HTTP协议访问数据库服务器主机，采用这种模式唯一的原因是客户端或服务器端的防火墙对数据库对网络连接强加了限制。其他情况下，这种模式不推荐被使用。


  运行web服务器的时候，只要将刚才命令行中的主类 (main class) 替换成: org.hsqldb.WebServer


  3、 Hsqldb Servlet


  这种模式和Web Server一样都采用HTTP协议，当如Tomcat或Resin等servlet引擎 (或应用服务器) 提供数据库的访问时，可以使用这种模式。但是Servlet模式不能脱离servlet引擎独立启动。为了提供数据库的连接，必须将HSQLDB.jar中的hsqlServlet类放置在应用服务器的相应位置。


  Web Server和Servlet模式都只能在客户端通过JDBC驱动来访问。Servlet模式只能启动一个单独的数据库。请注意做为应用程序服务器的数据库引擎通常不使用这种模式。


  连接到以Server模式运行的数据库


  当HSQLDB服务器运行时，客户端程序就可以通过hsqldb.jar中带有的HSQLDB JDBC Driver连接数据库。


  java 代码


  try{


  Class.forName("org.hsqldb.jdbcDriver") ;


  }catch(ClassNotFoundException e){


  e.printStackTrace();


  }


  Connection c = DriverManager.getConnection("jdbc:hsqldb:hsql://localhost/xdb", "sa", "");


  注: hsqldb的默认用户是sa密码为空。修改默认密码的方法我们将在工具使用部分做出介绍。

### In-Process模式

  In-Process模式又称Standalone模式。这种模式下，数据库引擎作为应用程序的一部分在同一个JVM中运行。对于一些应用程序来说， 这种模式因为数据不用转换和通过网络的传送而使得速度更快一些。其主要的缺点就是默认的不能从应用程序外连接到数据库。所以当应用程序正在运行的时候，你不能使用类似于Database Manager的外部工具来查看数据库的内容。在1.8.0版本中，你可以从同一个JVM的一个线程里面来运行一个服务器实例，从而可以提供外部连接来访问你的In-Process数据库。


  推荐的使用In-Process模式方式是: 开发的时候为数据库使用一个HSQLDB 服务器实例，然后在部属的时候转换到In-Process内模式。


  一个In-Process模式数据库是从JDBC语句开始启动的，在连接URL中带有指定的数据库文件路径作为JDBC的一部分。例如，假如数据库名称为testdb，它的数据库文件位于与确定的运行应用程序命令相同的目录下，下面的代码可以用来连接数据库: 


  Connection c = DriverManager.getConnection("jdbc:hsqldb:file:testdb ", "sa", "");


  数据库文件的路径格式在Linux主机和Windows主机上都被指定采用前斜线("/") 。所以相对路径或者是相对于相同分区下相同目录路径的表达方式是一致的。使用相对路径的时候，这些路径表示的是相对于用于启动JVM的shell命令的执行路径。

### Memory-Only数据库

  Memory-Only数据库不是持久化的而是全部在随机访问的内存中。因为没有任何信息写在磁盘上。这种模式通过mem:协议的方式来指定: 


  Connection c = DriverManager.getConnection("jdbc:hsqldb:mem:dbName", "sa", "");


  你也可以在server.properties中指定相同的URL来运行一个Memory-Only (仅处于内存中) 服务器实例。


  注意事项: 当一个服务器实例启动或者建立一个in-process数据库连接的时候，如果指定的路径没有数据库存在，那么就会创建一个新的空的数据库。这个特点的副作用就是让那些新用户产生疑惑。在指定连接已存在的数据库路径的时候，如果出现了什么错误的话，就会建立一个指向新数据库的连接。为了解决这个问题，你可以指定一个连接属性ifexists=true只允许和已存在的数据库建立连接而避免创建新的数据库，如果数据库不存在的话，getConnection()方法将会抛出异常。


  Memory-only 也有成为in memory 模式。在server模式或者in process 下可以使用，可看作前述2种模式的一个选项，已验证。如在在server模式下统一用 connection = DriverManager.getConnection("jdbc:hsqldb:hsql://x.x.x.x:port/xdb", "sa", "");


  而服务器端具体是file，mem模式又服务端启动参数决定，对客户端透明 
  
    HSqlDB 是由 Tomas Muller 的 Hypersonic SQL 后续开发出来的项目 
    
    
    
    
    
      , [2]hypersonic db 是纯 java 所开发的数据库, 可以透过 jdbc driver 来存取, 支持 ANSI-92 标准的 SQL 语法, 而且他占的空间很小, 大约只有 160K, 拥有快速的数据库引擎, 也提供了一些工具, 例如 web-server, 缓冲查询, 及一些管理工具. 他是属于 BSD 的 license, 可以自由下载, 并且可以安装使用在商业产品之上。 
      
      
        HSqlDB非常适合在用于快速的测试和演示的Java程序中。做单元测试也非常理想。
      
      
      
        HSqlDB不适合管理大型数据，例如百万数量级记录的数据库应用。HSQLDB简介它具有Server模式，进程内模式(In-Process)和内存模式(Memory-Only)三种。运行Hsqldb需要hsqldb.jar包, 它包含了一些组件和程序。
      
      
      
        在其官网可以获得最新的程序源代码及jar包文件([2])。
      
      
      
        Hsqldb2.2 支持多线程,提供更改的高性能，提供并发事物控制模型 (mvcc) 。
      
      
      
        HSQLDB具有11年的开发历史，并在1700多个开源项目中被广泛使用。
       
      
      
        in process 模式下按此访问 connection = DriverManager.getConnection("jdbc:hsqldb:mem:aname", "sa", "");
      