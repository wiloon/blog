---
title: JDBC URL
author: "-"
date: 2014-03-05T05:25:38+00:00
url: /?p=6343
categories:
  - Inbox
tags:
  - Database

---
## JDBC URL

### disable tls

JDK8版本过高引起MySQL连接失败：javax.net.ssl.SSLHandshakeException: No appropriate protocol
><https://juejin.cn/post/6969142310718144520>

    jdbc:mysql://127.0.0.1/database0?useunicode=true&characterencoding=utf8&tinyInt1isBit=false&useSSL=false

MySQL

MySQL Connector/J Driver

驱动程序包: <http://mvnrepository.com/artifact/MySQL/MySQL-connector-java>

驱动程序类名: com.MySQL.jdbc.Driver

### JDBC URL Format

The general format for a JDBC URL for connecting to a MySQL server is as follows, with items in square brackets ([ ]) being optional:

jdbc:MySQL://[host1][:port1][,[host2][:port2]]...[/[database]]
[?propertyName1=propertyValue1[&propertyName2=propertyValue2]...]

Here is a simple example for a connection URL:

jdbc:MySQL://localhost:3306/sakila?profileSQL=true

JDBC URL: jdbc:MySQL://<host>:<port>/<database_name>

默认端口3306，如果服务器使用默认端口则port可以省略

MySQL Connector/J Driver 允许在URL中添加额外的连接属性jdbc:MySQL://<host>:<port>/<database_name>?property1=value1&property2=value2

常用的有两个，一个是gjt (Giant Java Tree) 组织提供的MySQL驱动，其JDBC Driver名称 (JAVA类名) 为: org.gjt.mm.MySQL.Driver

详情请参见网站: <http://www.gjt.org/>

或在本网站下载MySQL JDBC Driver(mm.jar)

另一个是MySQL官方提供的JDBC Driver，其JAVA类名为: com.MySQL.jdbc.Driver

驱动下载网址: <http://dev.MySQL.com/downloads/，进入其中的MySQL> Connector/J区域下载。

MySQL JDBC URL格式如下:

jdbc:MySQL://[host:port],[host:port].../[database][?参数名1][=参数值1][&参数名2][=参数值2]...

现只列举几个重要的参数，如下表所示:

参数名称 参数说明 缺省值 最低版本要求

user 数据库用户名 (用于连接数据库)  所有版本

password 用户密码 (用于连接数据库)  所有版本

useUnicode 是否使用Unicode字符集，如果参数characterEncoding设置为gb2312或gbk，本参数值必须设置为true false 1.1g

characterEncoding 当useUnicode设置为true时，指定字符编码。比如可设置为gb2312或gbk false 1.1g

autoReconnect 当数据库连接异常中断时，是否自动重新连接？ false 1.1

autoReconnectForPools 是否使用针对数据库连接池的重连策略 false 3.1.3

failOverReadOnly 自动重连成功后，连接是否设置为只读？ true 3.0.12

maxReconnects autoReconnect设置为true时，重试连接的次数 3 1.1

initialTimeout autoReconnect设置为true时，两次重连之间的时间间隔，单位: 秒 2 1.1

connectTimeout 和数据库服务器建立socket连接时的超时，单位: 毫秒。 0表示永不超时，适用于JDK 1.4及更高版本 0 3.0.1

socketTimeout socket操作 (读写) 超时，单位: 毫秒。 0表示永不超时 0 3.0.1

对应中文环境，通常MySQL连接URL可以设置为:

jdbc:MySQL://localhost:3306/test?user=root&password=&useUnicode=true&characterEncoding=gbk&autoReconnect=true&failOverReadOnly=false

在使用数据库连接池的情况下，最好设置如下两个参数:

autoReconnect=true&failOverReadOnly=false

需要注意的是，在xml配置文件中，url中的&符号需要转义成&。比如在tomcat的server.xml中配置数据库连接池时，MySQL jdbc url样例如下:

jdbc:MySQL://localhost:3306/test?user=root&password=&useUnicode=true&characterEncoding=gbk

&autoReconnect=true&failOverReadOnly=false

<http://blog.csdn.net/ring0hx/article/details/6152528>

Microsoft SQL Server

Microsoft SQL Server JDBC Driver  (一般用来连接 SQLServer 2000)

驱动程序包名: msbase.jar mssqlserver.jar msutil.jar

驱动程序类名: com.microsoft.jdbc.sqlserver.SQLServerDriver

JDBC URL: jdbc:microsoft:sqlserver://<server_name>:<port>

默认端口1433，如果服务器使用默认端口则port可以省略

Microsoft SQL Server 2005 JDBC Driver

驱动程序包名: sqljdbc.jar

驱动程序类名: com.microsoft.sqlserver.jdbc.SQLServerDriver

JDBC URL: jdbc:sqlserver://<server_name>:<port>

默认端口1433，如果服务器使用默认端口则port可以省略

Oracle

Oracle Thin JDBC Driver

驱动程序包名: ojdbc14.jar

驱动程序类名: oracle.jdbc.driver.OracleDriver

JDBC URL:

jdbc:oracle:thin:@//<host>:<port>/ServiceName

或

jdbc:oracle:thin:@<host>:<port>:<SID>

IBM DB2

IBM DB2 Universal Driver Type 4

驱动程序包名: db2jcc.jar db2jcc_license_cu.jar

驱动程序类名: com.ibm.db2.jcc.DB2Driver

JDBC URL: jdbc:db2://<host>[:<port>]/<database_name>

IBM DB2 Universal Driver Type 2

驱动程序包名: db2jcc.jar db2jcc_license_cu.jar

驱动程序类名: com.ibm.db2.jcc.DB2Driver

JDBC URL: jdbc:db2:<database_name>

Informix

Informix JDBC Driver

驱动程序包名: ifxjdbc.jar

驱动程序类名: com.informix.jdbc.IfxDriver

JDBC URL: jdbc:informix-sqli://{<ip-address>|<host-name>}:<port-number>[/<dbname>]: INFORMIXSERVER=<server-name>

Sybase

Sybase Adaptive Server Enterprise JDBC Driver

驱动程序包名: jconn2.jar 或jconn3.jar

驱动程序类名: com.sybase.jdbc2.jdbc.SybDriver (com.sybase.jdbc3.jdbc.SybDriver)

JDBC URL: jdbc:sybase:Tds:<host>:<port>默认端口5000

Sybase Adaptive Server Anywhere or Sybase IQ JDBC Driver

驱动程序包名: jconn2.jar 或jconn3.jar

驱动程序类名: com.sybase.jdbc2.jdbc.SybDriver (com.sybase.jdbc3.jdbc.SybDriver)

JDBC URL: jdbc:sybase:Tds:<host>:<port>?ServiceName=<database_name>

默认端口2638

PostgreSQL

PostgreSQL Native JDBC Driver

驱动程序包名: 驱动程序类名: org.postgresql.Driver

JDBC URL: jdbc:postgresql://<host>:<port>/<database_name>

默认端口5432

Teradata

Teradata Driver for the JDBC Interface

驱动程序包名: terajdbc4.jar tdgssjava.jar gui.jar

驱动程序类名: com.ncr.teradata.TeraDriver

JDBC URL:

Type 4: jdbc:teradata://DatabaseServerName/Param1,Param2,...

Type 3: jdbc:teradata://GatewayServerName:PortNumber

/DatabaseServerName/Param1,Param2,...

Netezza

Netezza JDBC Driver

驱动程序包名: terajdbc4.jar tdgssjava.jar gui.jar

驱动程序类名: org.netezza.Driver

JDBC URL: jdbc:netezza://<host>:<port>/<database_name>

<http://www.2cto.com/database/201203/125168.html>

<https://dev.MySQL.com/doc/connector-j/5.1/en/connector-j-reference-configuration-properties.html>
