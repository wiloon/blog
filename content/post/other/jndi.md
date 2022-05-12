---
title: JNDI
author: "-"
date: 2011-12-25T03:59:59+00:00
url: jndi
categories:
  - Java
tags:$
  - reprint
---
## JNDI
## JNDI (Java Naming and Directory Interface，Java命名和目录接口)

是一组在Java应用中访问命名和目录服务的API。命名服务将名称和对象联系起来，使得我们可以用名称访问对象。目录服务是一种命名服务，在这种服务里，对象不但有名称，还有属性。


  英文全称是:Java Naming and Directory InterfaceS 
  
  
  
    术语解释: 一组帮助做多个命名和目录服务接口的API。
  
    JNDI(Java Naming and Directory Interface)是SUN公司提供的一种标准的Java命名系统接口，JNDI提供统一的客户端API，通过不同的访问提供者接口JNDI SPI的实现，由管理者将JNDI API映射为特定的命名服务和目录系统，使得Java应用程序可以和这些命名服务和目录服务之间进行交互。集群JNDI实现了高可靠性JNDI[8]，通过服务器的集群，保证了JNDI的负载平衡和错误恢复。在全局共享的方式下，集群中的一个应用服务器保证本地JNDI树的独立性，并拥有全局的JNDI树。每个应用服务器在把部署的服务对象绑定到自己本地的JNDI树的同时，还绑定到一个共享的全局JNDI树，实现全局JNDI和自身JNDI的联系。
  
  
  
    JNDI(Java Naming and Directory Interface)是一个应用程序设计的API，为开发人员提供了查找和访问各种命名和目录服务的通用、统一的接口，类似JDBC都是构建在抽象层上。
  
  
  
    JNDI可访问的现有的目录及服务有: 
  
  
  
    DNS、XNam 、Novell目录服务、LDAP(Lightweight Directory Access Protocol 轻型目录访问协议)、 CORBA对象服务、文件系统、Windows XP/2000/NT/Me/9x的注册表、RMI、DSML v1&v2、NIS。
  
  
     JNDI优点
  
  
    包含了大量的命名和目录服务，使用通用接口来访问不同种类的服务；
  
  
  
    可以同时连接到多个命名或目录服务上；
  
  
  
    建立起逻辑关联，允许把名称同Java对象或资源关联起来，而不必知道对象或资源的物理ID。
  
  
  
    JNDI程序包: 
  
  
  
    javax.naming: 命名操作；
  
  
  
    javax.naming.directory: 目录操作；
  
  
  
    javax.naming.event: 在命名目录服务器中请求事件通知；
  
  
  
    javax.naming.ldap: 提供LDAP支持；
  
  
  
    javax.naming.spi: 允许动态插入不同实现。
  
  
  
    利用JNDI的命名与服务功能来满足企业级API对命名与服务的访问，诸如EJB、JMS、JDBC 2.0以及IIOP上的RMI通过JNDI来使用CORBA的命名服务。
  
  
     JNDI架构
  
  
    JNDI架构提供了一组标准的独立于命名系统的API，这些API构建在与命名系统有关的驱动之上。这一层有助于将应用与实际数据源分离，因此不管应用访问的是LDAP、RMI、DNS、还是其他的目录服务。换句话说，JNDI独立于目录服务的具体实现，只要有目录的服务提供接口 (或驱动) ，就可以使用目录。
  
  
  
    关于JNDI要注意的重要一点是，它提供了应用编程接口(application programming interface，API)和服务提供者接口(service provider interface，SPI)。这一点的真正含义是，要让应用与命名服务或目录服务交互，必须有这个服务的JNDI服务提供者，这正是JNDI SPI发挥作用的地方。服务提供者基本上是一组类，这些类为各种具体的命名和目录服务实现了JNDI接口—很象JDBC驱动为各种具体的数据库系统实现了JDBC接口一样。作为一个应用开发者，不必操心JNDI SPI。只需要确认要使用的每一个命名或目录服务都有服务提供者。
  
  
     JNDI组件
  
  
    1、Javax.naming: 包含了访问命名服务的类和接口。例如，它定义了Context接口，这是命名服务执行查询的入口。
  
  
  
    2、Javax.naming.directory: 对命名包的扩充，提供了访问目录服务的类和接口。例如，它为属性增加了新的类，提供了表示目录上下文的DirContext接口，定义了检查和更新目录对象的属性的方法。
  
  
  
    3、Javax.naming.event: 提供了对访问命名和目录服务时的时间通知的支持。例如，定义了NamingEvent类，这个类用来表示命名/目录服务产生的事件，定义了侦听NamingEvents的NamingListener接口。
  
  
  
    4、Javax.naming.ldap: 这个包提供了对LDAP 版本3扩充的操作和控制的支持，通用包javax.naming.directory没有包含这些操作和控制。
  
  
  
    5、Javax.naming.spi: 这个包提供了一个方法，通过javax.naming和有关包动态增加对访问命名和目录服务的支持。这个包是为有兴趣创建服务提供者的开发者提供的。
  
  
     JNDI用途
  
  
    命名或目录服务使用户可以集中存储共有信息，这一点在网络应用中是重要的，因为这使得这样的应用更协调、更容易管理。例如，可以将打印机设置存储在目录服务中，以便被与打印机有关的应用使用。
  
  
  
    我们大家每天都不知不觉地使用了命名服务。命名系统中的对象可以是DNS记录中的名称、应用服务器中的EJB组件(Enterprise JavaBeans Component)、LDAP(Lightweight Directory Access Protocol)中的用户Profile。
  
  
  
    目录服务是命名服务的自然扩展。两者之间的关键差别是目录服务中对象可以有属性 (例如，用户有email地址) ，而命名服务中对象没有属性。因此，在目录服务中，你可以根据属性搜索对象。JNDI允许你访问文件系统中的文件，定位远程RMI注册的对象，访问象LDAP这样的目录服务，定位网络上的EJB组件。
  
  
  
    对于象LDAP 客户端、应用launcher、类浏览器、网络管理实用程序，甚至地址薄这样的应用来说，JNDI是一个很好的选择。
  
  
  
    JNDI可访问的现有的目录及服务有: 
  
  
  
    DNS、XNam 、Novell目录服务、LDAP(Lightweight Directory Access Protocol 轻型目录访问协议)、 CORBA对象服务、文件系统、Windows XP/2000/NT/Me/9x的注册表、RMI、DSML v1&v2、NIS
  
  
     JNDI与JDBC
  
  
    JNDI提供了一种统一的方式，可以用在网络上查找和访问服务。通过指定一个资源名称，该名称对应于数据库或命名服务中的一个记录，同时返回数据库连接建立所必须的信息。
  
  
  
    JNDI主要有两部分组成: 应用程序编程接口和服务供应商接口。应用程序编程接口提供了Java应用程序访问各种命名和目录服务的功能，服务供应商接口提供了任意一种服务的供应商使用的功能。
  
  
  
    代码示例: 
  
  
  
    try{
  
  
  
    Context cntxt = new InitialContext();
  
  
  
    DataSource ds = (DataSource) cntxt.lookup("jdbc/dpt");
  
  
  
    }
  
  
  
    catch(NamingException ne){
  
  
  
    ...
  
  
  
    }
  
  
     JNDI与JMS
  
  
    消息通信是软件组件或应用程序用来通信的一种方法。JMS就是一种允许应用程序创建、发送、接收、和读取消息的JAVA技术。
  
  
  
    代码示例: 
  
  
  
    try{
  
  
  
    Properties env = new Properties();
  
  
  
    InitialContext inictxt = new InitialContext(env);
  
  
  
    TopicConnectionFactory connFactory = (TopicConnectionFactory) inictxt.lookup("TTopicConnectionFactory");
  
  
  
    ...
  
  
  
    }
  
  
  
    catch(NamingException ne){
  
  
  
    ...
  
  
  
    }
  
  
  
    访问特定目录: 举个例子，人是个对象，他有好几个属性，诸如这个人的姓名、电话号码、电子邮件地址、邮政编码等属性。通过getAttributes()方法
  
  
  
    Attribute attr =
  
  
  
    directory.getAttributes(personName).get("email");
  
  
  
    String email = (String)attr.get();
  
  
  
    通过使用JNDI让客户使用对象的名称或属性来查找对象: 
  
  
  
    foxes = directory.search("o=Wiz,c=US", "sn=Fox", controls);
  
  
  
    通过使用JNDI来查找诸如打印机、数据库这样的对象，查找打印机的例子: 
  
  
  
    Printer printer = (Printer)namespace.lookup(printerName);
  
  
  
    printer.print(document);
  
  
  
    浏览命名空间: 
  
  
  
    NamingEnumeration list = namespace.list("o=Widget, c=US");
  
  
  
    while (list.hasMore()) {
  
  
  
    NameClassPair entry = (NameClassPair)list.next();
  
  
  
    display(entry.getName(), entry.getClassName());
  
  
  
    }
  
  
     常用的JNDI操作
  
  
    void bind(String sName,Object object);――绑定: 把名称同对象关联的过程
  
  
  
    void rebind(String sName,Object object);――重新绑定: 用来把对象同一个已经存在的名称重新绑定
  
  
  
    void unbind(String sName);――释放: 用来把对象从目录中释放出来
  
  
  
    Object lookup(String sName);――查找: 返回目录中的一个对象
  
  
  
    void rename(String sOldName,String sNewName);――重命名: 用来修改对象名称绑定的名称
  
  
  
    NamingEnumeration listBinding(String sName);――清单: 返回绑定在特定上下文中对象的清单列表
  
  
  
    NamingEnumeration list(String sName);
  
  
  
    代码示例: 重新得到了名称、类名和绑定对象。
  
  
  
    NamingEnumeration namEnumList = ctxt.listBinding("cntxtName");
  
  
  
    ...
  
  
  
    while ( namEnumList.hasMore() ) {
  
  
  
    Binding bnd = (Binding) namEnumList.next();
  
  
  
    String sObjName = bnd.getName();
  
  
  
    String sClassName = bnd.getClassName();
  
  
  
    SomeObject objLocal = (SomeObject) bnd.getObject();
  
  
  
    }
  


## JNDI 是什么
<http://blog.csdn.net/zhaosg198312/article/details/3979435>

JNDI是 Java 命名与目录接口 (Java Naming and Directory Interface) ，在JavaEE规范中是重要的规范之一，不少专家认为，没有透彻理解JNDI的意义和作用，就没有真正掌握JavaEE特别是EJB的知识。
  
那么，JNDI到底起什么作用？

要了解JNDI的作用，我们可以从"如果不用JNDI我们怎样做？用了JNDI后我们又将怎样做？"这个问题来探讨。

没有JNDI的做法: 
  
程序员开发时，知道要开发访问MySQL数据库的应用，于是将一个对 MySQL JDBC 驱动程序类的引用进行了编码，并通过使用适当的 JDBC URL 连接到数据库。
  
就像以下代码这样: 

```java
  
Connection conn=null;
  
try {
  
Class.forName("com.MySQL.jdbc.Driver",true, Thread.currentThread().getContextClassLoader());
  
conn=DriverManager.getConnection("jdbc:MySQL://MyDBServer?user=qingfeng&password=mingyue");
  
/* 使用conn并进行SQL操作 */
  
......
  
conn.close();
  
}
  
catch(Exception e) {
  
e.printStackTrace();
  
}
  
finally {
  
if(conn!=null) {
  
try {
  
conn.close();
  
} catch(SQLException e) {}
  
}
  
}
  
```

这是传统的做法，也是以前非Java程序员 (如Delphi、VB等) 常见的做法。这种做法一般在小规模的开发过程中不会产生问题，只要程序员熟悉Java语言、了解JDBC技术和MySQL，可以很快开发出相应的应用程序。

没有JNDI的做法存在的问题: 
  
1. 数据库服务器名称MyDBServer 、用户名和口令都可能需要改变，由此引发JDBC URL需要修改；
  
2. 数据库可能改用别的产品，如改用DB2或者Oracle，引发JDBC驱动程序包和类名需要修改；
  
3. 随着实际使用终端的增加，原配置的连接池参数可能需要调整；
  
4. ......

解决办法: 
  
程序员应该不需要关心"具体的数据库后台是什么？JDBC驱动程序是什么？JDBC URL格式是什么？访问数据库的用户名和口令是什么？"等等这些问题，程序员编写的程序应该没有对 JDBC 驱动程序的引用，没有服务器名称，没有用户名称或口令 —— 甚至没有数据库池或连接管理。而是把这些问题交给J2EE容器来配置和管理，程序员只需要对这些配置和管理进行引用即可。

由此，就有了JNDI。

用了JNDI之后的做法: 
  
首先，在在JavaEE容器中配置JNDI参数，定义一个数据源，也就是JDBC引用参数，给这个数据源设置一个名称；然后，在程序中，通过数据源名称引用数据源从而访问后台数据库。
  
具体操作如下 (以JBoss为例) : 
  
1. 配置数据源
  
在JBoss的 D:/jboss420GA/docs/examples/jca 文件夹下面，有很多不同数据库引用的数据源定义模板。将其中的 MySQL-ds.xml 文件Copy到你使用的服务器下，如 D:/jboss420GA/server/default/deploy。
  
修改 MySQL-ds.xml 文件的内容，使之能通过JDBC正确访问你的MySQL数据库，如下: 
  
<!--?xml version="1.0" encoding="UTF-8"?-->

```xml

<?xml version="1.0" encoding="UTF-8"?>
  
<datasources>
  
<local-tx-datasource>
      
<jndi-name> MySQLDS</jndi-name>
      
<connection-url> jdbc:MySQL://localhost:3306/lw</connection-url>
      
<driver-class> com.MySQL.jdbc.Driver</driver-class>
      
<user-name> root</user-name>
      
<password> rootpassword</password>
  
<exception-sorter-class-name>org.jboss.resource.adapter.jdbc.vendor.MySQLExceptionSorter</exception-sorter-class-name>
      
<metadata>
         
<type-mapping> MySQL</type-mapping>
      
</metadata>
  
</local-tx-datasource>
  
</datasources>
  
```

这里，定义了一个名为MySQLDS的数据源，其参数包括JDBC的URL，驱动类名，用户名及密码等。

2. 在程序中引用数据源: 

```java
  
Connection conn=null;
  
try {
  
Context ctx=new InitialContext();
  
Object datasourceRef=ctx.lookup("java:MySQLDS"); //引用数据源
  
DataSource ds=(Datasource)datasourceRef;
  
conn=ds.getConnection();
  
/* 使用conn进行数据库SQL操作 */
  
......
  
conn.close();
  
}
  
catch(Exception e) {
  
e.printStackTrace();
  
}
  
finally {
  
if(conn!=null) {
  
try {
  
conn.close();
  
} catch(SQLException e) { }
  
}
  
}
  
```

直接使用JDBC或者通过JNDI引用数据源的编程代码量相差无几，但是现在的程序可以不用关心具体JDBC参数了。
  
在系统部署后，如果数据库的相关参数变更，只需要重新配置 MySQL-ds.xml 修改其中的JDBC参数，只要保证数据源的名称不变，那么程序源代码就无需修改。
  
由此可见，JNDI避免了程序与数据库之间的紧耦合，使应用更加易于配置、易于部署。
  
JNDI的扩展: 
  
JNDI在满足了数据源配置的要求的基础上，还进一步扩充了作用: 所有与系统外部的资源的引用，都可以通过JNDI定义和引用。
  
所以，在J2EE规范中，J2EE 中的资源并不局限于JDBC 数据源。引用的类型有很多，其中包括资源引用(已经讨论过)、环境实体和 EJB 引用。特别是 EJB 引用，它暴露了 JNDI 在 J2EE 中的另外一项关键角色: 查找其他应用程序组件。
  
EJB 的 JNDI 引用非常类似于JDBC 资源的引用。在服务趋于转换的环境中，这是一种很有效的方法。可以对应用程序架构中所得到的所有组件进行这类配置管理，从EJB组件到JMS队列和主题，再到简单配置字符串或其他对象，这可以降低随时间的推移服务变更所产生的维护成本，同时还可以简化部署，减少集成工作。 外部资源"。
  
J2EE 规范要求所有 J2EE 容器都要提供 JNDI 规范的实现。JNDI 在J2EE中的角色就是"交换机" —— J2EE 组件在运行时间接地查找其他组件、资源或服务的通用机制。在多数情况下，提供 NDI供应者的容器可以充当有限的数据存储，这样管理员就可以设置应用程序的执行属性，并让其他应用程序引用这些属性 (Java 管理扩展 (Java Management Extensions，JMX) 也可以用作这个目的) 。JNDI 在 J2EE 应用程序中的主要角色就是提供间接层，这样组件就可以发现所需要的资源，而不用了解这些间接性。
  
在 J2EE 中，JNDI 是把 J2EE 应用程序合在一起的粘合剂，JNDI 提供的间接寻址允许跨企业交付可伸缩的、功能强大且很灵活的应用程序。这是 J2EE 的承诺，而且经过一些计划和预先考虑，这个承诺是完全可以实现的。

