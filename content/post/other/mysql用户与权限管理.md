---
title: MySQL用户与权限管理
author: "-"
date: 2011-12-26T04:23:28+00:00
url: /?p=1998
categories:
  - DataBase
tags:
  - MySQL

---
## MySQL用户与权限管理
//创建新用户 user0

```bash
cREATE USER user0 IDENTIFIED BY 'password0';```

\***密码要带引号

授权:

```bash
grant all privileges on database0.* to user0@localhost identified by 'password0';
```

授权之后该用户才能用他自己的用户名密码访问MySQL.

### 从MySQL删除用户账户

要想移除账户，应使用Drop USER语句.

Drop USER _user_ [, _user_] ...

Drop USER语句用于删除一个或多个MySQL账户。要使用Drop USER，您必须拥有MySQL数据库的全局Create USER权限或Delete权限。使用与GRANT或REVOKE相同的格式为每个 账户命名；例如，'jeffrey'@'localhost'。 账户名称的用户和主机部分与用户表记录的User和Host列值相对应。 www.87717.com

使用Drop USER，您可以取消一个账户和其权限，操作如下: 

Drop USER _user_;

该语句可以删除来自所有授权表的帐户权限记录。

drop user [username@'%'][1]

drop user <username@localhost>

改密码:

grant all privileges on DBNAME.* to user0@localhost identified by 'password4';

###'@localhost' 这个一定要有.....

为root加上密码xxx123:

./bin/MySQLadmin -u root password xxx123
  
或写成
  
./bin/MySQLadmin -uroot password xxx123

加下密码之后，在本进行进入MySQL: 
  
./bin/MySQL -uroot -p

更改root的密码由xxx123改为yy1234:
  
./bin/MySQLadmin -uroot -pxxx123 password yy1234

＝＝＝＝＝＝＝grant 权限 on 数据库对象 to 用户＝＝＝＝＝＝＝＝＝＝
  
MySQL 赋予用户权限命令的简单格式可概括为: 
  
grant 权限 on 数据库对象 to 用户
  
grant 权限 on 数据库对象 to 用户 identified by "密码"

＝＝＝＝＝＝＝＝用户及权限管理: 最常用操作实例＝＝＝＝＝＝＝＝
  
(用户名: dba1,密码: dbapasswd,登录IP: 192.168.0.10)

//开放管理MySQL中所有数据库的权限
  
grant all on \*.\* to dba1@'192.168.0.10'identified by "dbapasswd";

//开放管理MySQL中具体数据库 (testdb)的权限
  
grant all privileges on testdb to dba1@'192.168.0.10'identified by "dbapasswd";
  
或
  
grant all on testdb to dba1@'192.168.0.10'identified by "dbapasswd";

//开放管理MySQL中具体数据库的表(testdb.table1)的权限
  
grant all on testdb.teable1 to dba1@'192.168.0.10'identified by "dbapasswd";

//开放管理MySQL中具体数据库的表(testdb.table1)的部分列的权限
  
grant select(id, se, rank) on testdb.table1 to ba1@'192.168.0.10'identified by "dbapasswd";

//开放管理操作指令
  
grant select, insert, update, delete on testdb.* to dba1@'192.168.0.10'identified by "dbapasswd";

//回收权限
  
revoke all on \*.\* from dba1@localhost;

//查看 MySQL 用户权限
  
show grants;
  
show grants for dba1@localhost;

＝＝＝＝＝＝＝＝用户及权限管理: 更多更详细实例＝＝＝＝＝＝＝＝
  
下面用实例来进行说明: 

一、grant普通数据用户 (test1)，查询、插入、更新、删除 数据库(test)中所有表数据的权利。
  
grant select on test.* to test1@'%';
  
grant insert on test.* to test1@'%';
  
grant update on test.* to test1@'%';
  
grant delete on test.* to test1@'%';
  
或者，用一条 MySQL 命令来替代: 
  
grant select, insert, update, delete on test.* to test1@'%';

二、grant数据库开发人员(duser)，创建表、索引、视图、存储过程、函数。。。等权限。

grant创建、修改、删除 MySQL 数据表结构权限。
  
grant create on testdb.* to duser@'192.168.0.%';
  
grant alter on testdb.* to duser@'192.168.0.%';
  
grant drop on testdb.* to duser@'192.168.0.%';

grant 操作 MySQL 外键权限。
  
grant references on testdb.* to developer@'192.168.0.%';

grant 操作 MySQL 临时表权限。
  
grant create temporary tables on testdb.* to developer@'192.168.0.%';

grant 操作 MySQL 索引权限。
  
grant index on testdb.* to developer@'192.168.0.%';

grant 操作 MySQL 视图、查看视图源代码 权限。
  
grant create view on testdb.* to duser@'192.168.0.%';
  
grant show view on testdb.* to duser@'192.168.0.%';

grant 操作 MySQL 存储过程、函数 权限。
  
grant create routine on testdb.* to duser@'192.168.0.%';
  
grant alter routine on testdb.* to duser@'192.168.0.%';
  
grant execute on testdb.* to duser@'192.168.0.%';

三、grant 普通DBA管理某个MySQL数据库(test)的权限。
  
grant all privileges on test to dba@'localhost'
  
其中，关键字 "privileges" 可以省略。

四、grant 高级 DBA 管理 MySQL 中所有数据库的权限。
  
grant all on \*.\* to dba@'localhost'

五、MySQL grant 权限，分别可以作用在多个层次上。

1. grant 作用在整个 MySQL 服务器上: 
  
grant select on \*.\* to dba@localhost; - dba 可以查询 MySQL 中所有数据库中的表。
  
grant all on \*.\* to dba@localhost; - dba 可以管理 MySQL 中的所有数据库

2. grant 作用在单个数据库上: 
  
grant select on testdb.* to dba@localhost; - dba 可以查询 testdb 中的表。

3. grant 作用在单个数据表上: 
  
grant select, insert, update, delete on testdb.orders to dba@localhost;

4. grant 作用在表中的列上: 
  
grant select(id, se, rank) on testdb.apache_log to dba@localhost;

5. grant 作用在存储过程、函数上: 
  
grant execute on procedure testdb.pr_add to 'dba'@'localhost'
  
grant execute on function testdb.fn_add to 'dba'@'localhost'

六、查看 MySQL 用户权限
  
查看当前用户 (自己) 权限: 
  
show grants;
  
查看其他 MySQL 用户权限: 
  
show grants for dba@localhost;

七、撤销已经赋予给 MySQL 用户权限的权限。
  
revoke 跟 grant 的语法差不多，只需要把关键字 "to" 换成 "from" 即可: 
  
grant all on \*.\* to dba@localhost;
  
revoke all on \*.\* from dba@localhost;

八、MySQL grant、revoke 用户权限注意事项
  
1. grant, revoke 用户权限后，该用户只有重新连接 MySQL 数据库，权限才能生效。
  
2. 如果想让授权的用户，也可以将这些权限 grant 给其他用户，需要选项 "grant option"
  
grant select on testdb.* to dba@localhost with grant option;
  
这个特性一般用不到。实际中，数据库权限最好由 DBA 来统一管理。

### 
 

 [1]: mailto:username@ %