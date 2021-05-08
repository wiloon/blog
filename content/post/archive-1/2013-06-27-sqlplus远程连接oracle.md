---
title: sqlplus远程连接oracle
author: w1100n
type: post
date: 2013-06-27T02:39:43+00:00
url: /?p=5560
categories:
  - DataBase

---
sqlplus system/manager@192.168.208.120:1521/orcl

sqlplus sys/PASSWORD@ip:port/orcl as sysdba

tnsnames.ora示例如下: 
  
ORCL =
  
(DESCRIPTION =
  
(ADDRESS = (PROTOCOL = TCP)(HOST = 192.168.208.120)(PORT = 1521))
  
(CONNECT_DATA =
  
(SERVER = DEDICATED)
  
(SERVICE_NAME = orcl)
  
)
  
)

以上文件中，ORCL是个连接标示符，可以自己修改，HOST是远程Oracle服务器的地址，PORT是Oracle的服务端口，没有修改过的话，默认是1521。Service_name是远程实例名称。

使用sql-plus连接
  
命令行下执行sqlplus /nolog
  
进入sqlplus提示符，输入
  
connect / @<连接标识符>
  
或者
  
sqlplus system/manager@192.168.208.120:1521/orcl
  
没有意外的话连接成功。
  
如果上述方法试验没有成功，用下面的方式最直接了
  
Sqlplus system/manager@'(description=(address_list=(address=(proto=tcp)(host=192.168.208.120)(port=1521)))(connect_data=(service_name=orcl)))'
  
以上使用sqlplus的方法被转载n次。