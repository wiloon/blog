---
title: MySQL basic
author: "-"
date: 2011-04-15T14:42:09+00:00
url: mysql
categories:
  - db
tags:
  - mysql
---
## MySQL basic

## install

```bash
# client
sudo pacman -S mariadb-clients
# server + client
sudo pacman -S mariadb

```

### 查看表结构

```sql
desc table_name;
```

### mysqldump

```bash
mysqldump -h 192.168.50.100 -uroot -p --databases rssx --tables user --where=user_id='0'
```

## mysql GUI client for Linux

```bash
    IDEA
```

### jdbc url

```r
    jdbc:MySQL://localhost:3306/tmp
    # driver
    com.MySQL.jdbc.Driver
```

### MySQL heidisql 变量

```bash
    SET @total_count := 10;
    select @total_count;
```

### 配置文件位置

```r
    /etc/my.cnf
```

### 查端口

```r
    show variables like 'port';
```

### 字段默认值

```sql
    alter tabe tbl_ecp modify load_count default 0;
```

MySQL管理员用户名: root
  
密码安装MySQL时指定.
  
登录MySQL:
    MySQL -u root -p

### 查看有哪些数据库
  
show databases;

### 创建新用户 wiloon

```sql
CREATE USER wiloon IDENTIFIED BY '123456';
-- 密码要带引号
```

### 创建数据库, 数据库名 mydb

```sql
create database mydb;
```

创建数据库指定数据库的字符集

```sql
create database mydb character set utf8;
```

### 授权用户wiloon 拥有数据库 enx 的所有权限

```sql
    grant all privileges on enlab.* to wiloon@'%' identified by 'password';
```

退出后用wiloon登录, 然后show databases; 应该可以看到enlab了.

### 查看建表语句

```sql
    show create table table0;
    SHOW CREATE TABLE table0 \G;
```

### 查看版本

```sql
select version();
-- 查看sql_model参数命令: 

SELECT @@GLOBAL.sql_mode;
SELECT @@SESSION.sql_mode;
```

### podmn

```bash
# mysql
podman run -d \
--name mysql \
-p 3306:3306 \
-v /etc/localtime:/etc/localtime:ro \
-v mysql-config:/etc/mysql/conf.d \
-v mysql-data:/var/lib/mysql \
-e MYSQL_ROOT_PASSWORD=rootroot \
mysql:5.7.37-debian \
--character-set-server=utf8mb4 \
--collation-server=utf8mb4_unicode_ci

#marial db
podman run -d \
--name mariadb \
-p 3306:3306 \
-v /etc/localtime:/etc/localtime:ro \
-v MySQL-config:/etc/MySQL/conf.d \
-v MySQL-data:/var/lib/MySQL \
-e MySQL_ROOT_PASSWORD=password0 \
mariadb:latest \
--character-set-server=utf8mb4 \
--collation-server=utf8mb4_unicode_ci

    # docker client
    podman run -it \
    --rm mariadb MySQL -h 127.0.0.1 -u root -p password0
```

### MySQL client, conn

```bash
sudo pacman -S mariadb-clients
MySQL -u user0 -ppassword0 -h 127.0.0.1 -P 3306 -D mydb
mariadb -u user0 -h 127.0.0.1 -P 3306 -D database0 -ppassword0
# add yum repo https://dev.MySQL.com/doc/MySQL-repo-excerpt/5.6/en/linux-installation-yum-repo.html
yum install MySQL-community-client
```

```bash
sudo pacman -S mariadb
sudo MySQL_install_db --user=MySQL --basedir=/usr --datadir=/var/lib/MySQL
sudo systemctl start mariadb.service
MySQL -u root -p
```

### 查表字段名

```sql
select COLUMN_NAME from information_schema.COLUMNS where table_name = 'your_table_name';
select COLUMN_NAME from information_schema.COLUMNS where table_name = 'your_table_name' AND COLUMN_NAME='column_name_0'
select COLUMN_NAME from information_schema.COLUMNS where table_name = 'your_table_name' and table_schema = 'your_db_name';
```

```sql
-- 查看索引
show index from tablename;

show keys from table

show warnings;
-- create user, ***密码要带引号
CREATE USER user0 IDENTIFIED BY 'password0';

-- create database
CREATE DATABASE db0 DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

-- 授权:
grant all privileges on db0 .* to user0@'%' identified by 'password0';
grant all privileges on db0 .* to user0@localhost identified by 'password0';
-- delete database
drop database db0 ;

EXPLAIN SELECT * FROM t0 where id=1 \G
explain partitions select * from t4 where id=1 \G

-- create table, http://www.wiloon.com/?p=1811
CREATE TABLE t1(id int not null,name char(20),c0 int);

-- primary key
alter table t1 drop primary key;
alter table t1 add primary key (id);

-- date format
select date_format(create_time,'%Y-%c-%d'),count(*) from t_market_data group by date_format(create_time,'%Y%c%d');
show variables like 'max_connections';
show global status like 'Max_used_connections';
show status like 'Threads%';

-- length
select length(xxx) from txxx;
```

### insert

```sql
    INSERT INTO items (name,city,price,number,picture) VALUES ('耐克运动鞋','广州',500,1000,'003.jpg');

    INSERT INTO 
    items(name,city,price,number,picture) 
    VALUES
    ('耐克运动鞋','广州',500,1000,'003.jpg'),
    ('耐克运动鞋2','广州2',500,1000,'002.jpg');
```

+——————-+——-+
| Variable_name | Value |
+——————-+——-+

| Threads_cached | 58 |
  
| Threads_connected | 57 | ###这个数值指的是打开的连接数
  
| Threads_created | 3676 |
  
| Threads_running | 4 | ###这个数值指的是激活的连接数，这个数值一般远低于connected数值
  
+——————-+——-+
  
Threads_connected 跟show processlist结果相同，表示当前连接数。准确的来说，Threads_running是代表当前并发数
  
这是是查询数据库当前设置的最大连接数
  
MySQL> show variables like '%max_connections%';
  
+—————–+——-+
  
| Variable_name | Value |
  
+—————–+——-+
  
| max_connections | 1000 |
  
+—————–+——-+
  
可以在/etc/my.cnf里面设置数据库的最大连接数
  
[MySQLd]
  
max_connections = 1000
  
archlinux start MySQL service

select @@tx_isolation;
  
show full processlist;

systemctl start MySQLd.service

查看所有用户

use MySQL;
  
select * from user;
  
当前日期

select now() from dual;

set password

SET PASSWORD FOR user0@localhost= PASSWORD("password");
  
# 注意后面这句话 "COLLATE utf8_general_ci",大致意思是在排序时根据utf8变码格式来排序

授权之后该用户才能用他自己的用户名密码访问MySQL.

MySQL-限制返回记录数limit
  
SELECT * FROM table  LIMIT [offset,] rows | rows OFFSET offset
  
SELECT  * FROM  table  order by time desc LIMIT  n;
  
## auto_increment

alter table tb_name modify id int auto_increment primary key;

## export one table

MySQLdump -uroot -p DBName TableName> foo.sql

创建表:

create table tbl_ecp (
  
id int primary key not null,
  
english varchar(256) not null,
  
chinese varchar(512),
  
pronunciation varchar(256),
  
create_datetime datetime
  
);

drop table dbname table_name ;
  
drop table table_name ;
  
表, 增加字段

ALTER TABLE table_name ADD field_name field_type;
  
alter table tbl_user add email varchar(2255);
  
把字段 id 设成自增: auto_increment.

自增字段必须设成主键.

alter table tbl_log modify column id integer not null auto_increment, add primary key (id);

systemdate(), now()
  
sysdate是去读取系统的时间戳，now是读取数据库的时间戳

MySQL添加字段的方法并不复杂，下面将为您详细介绍MySQL添加字段和修改字段等操作的实现方法，希望对您学习MySQL添加字段方面会有所帮助。

1.登录数据库

MySQL -u root -p 数据库名称

2.查询所有数据表

show tables;

3.查询表的字段信息

desc 表名称;

4.1添加表字段

alter table table1 add transactor varchar(10) not Null;

alter table table1 add id int unsigned not Null auto_increment primary key

4.2.修改某个表的字段类型及指定为空或非空

-alter table 表名称 change 字段名称 字段名称 字段类型 [是否允许非空];

alter table tbl_user change password password varchar(256)

-alter table 表名称 modify 字段名称 字段类型 [是否允许非空];
  
alter table tbl_user modify deleted char(1) not null;

> alter table 表名称 modify 字段名称 字段类型 [是否允许非空];

> 4.3.修改某个表的字段名称及指定为空或非空

alter table 表名称 change 字段原名称 字段新名称 字段类型 [是否允许非空

4.4如果要删除某一字段，可用命令: ALTER TABLE mytable DROP 字段 名;

导出

MySQLdump -uwiloon -pPASSWORD -default-character-set=utf8 enlab >enlab.sql
  
导入

MySQL -uusername -ppassword db_name < db_name.sql
  
### 日期格式化函数date_format()

```sql
    -- %Y: 年 %c: 月 %d: 日 %H: 小时 %i: 分钟 %s: 秒
    select date_format(now(),'%Y');
```

还可以用一个USE db_name语句启动文本文件。在这种情况下，不需要在命令行中指定数据库名:

shell> MySQL < text_file

如果正运行MySQL，可以使用source或.命令执行SQL脚本文件:

MySQL> source filename

查看MySQL版本

在MySQL中: MySQL> status;

eg:
  
[root@linuxtest test]# MySQL -u root -p
  
Enter password:
  
Welcome to the MySQL monitor. Commands end with ; or \g.
  
Your MySQL connection id is 5
  
Server version: 5.1.30-community MySQL Community Server (GPL)

Type 'help;' or '\h' for help. Type '\c' to clear the buffer.

MySQL> CREATE DATABASE test DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
  
Query OK, 1 row affected (0.06 sec)

MySQL> show databases;
  
+——————–+
  
| Database |
  
+——————–+
  
| information_schema |
  
| cacti |
  
| MySQL |
  
| test | |
  
+——————–+
  
5 rows in set (

索引相关常用命令:
  
1) 创建主键

CREATE TABLE `pk_tab2` (

`id` int(11) NOT NULL AUTO_INCREMENT,

`a1` varchar(45) DEFAULT NULL,

PRIMARY KEY (`id`)
  
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

2) 创建唯一索引
  
create unique index indexname on tablename(columnname);
  
alter table tablename add unique index indexname(columnname);

3) 创建单列一般索引
  
create index indexname on tablename(columnname);
  
alter table tablename add index indexname(columnname);

4) 创建单列前缀索引
  
create index indexname on tablename(columnname(10)); //单列的前10个字符创建前缀索引
  
alter table tablename add index indexname(columnname(10)); //单列的前10个字符创建前缀索引

5) 创建复合索引
  
create index indexname on tablename(columnname1，columnname2); //多列的复合索引
  
create index indexname on tablename(columnname1，columnname2(10)); //多列的包含前缀的复合索引
  
alter table tablename add index indexname(columnname1，columnname2); //多列的复合索引
  
alter table tablename add index indexname(columnname1，columnname(10)); //多列的包含前缀的复合索引

6) 删除索引
  
drop index indexname on tablename;;
  
alter table tablename drop index indexname;

7) 查看索引
  
show index from tablename;
  
show create table pk_tab2;

### ClassNotFoundException: com.MySQL.jdbc.Driver

download and install connector/J , the JDBC driver for MySQL.  
MySQL-connector-java-5.1.15-bin.jar

<http://blog.sina.com.cn/s/blog_5dc960cd0100ea2h.html>

<http://database.51cto.com/art/201011/234549.htm>

<http://blog.csdn.net/myxx520/article/details/5130249>

<http://yh1022.iteye.com/blog/288693>

<http://blog.sina.com.cn/s/blog_5dc960cd0100ea2h.html>

<http://blog.csdn.net/flying_hawk/article/details/3498476>

<http://blog.sina.com.cn/s/blog_4d73c2c20100h8gp.html>

<http://bbs.csdn.net/topics/350006598>

<http://blog.chinaunix.net/uid-20382003-id-3022768.html>
><https://blog.csdn.net/weixin_40482816/article/details/87074689>

## MySQL 查看版本,version

MySQL -V
  
MySQL Ver 14.14 Distrib 5.5.32, for debian-linux-gnu (x86_64) using readline 6.2

# MySQL函数

select version();

### 在MySQL中: MySQL> status

MySQL> status;

    MySQL Ver 14.7 Distrib 4.1.10a, for redhat-linux-gnu (i686)Connection id: 416
      
    SSL: Not in use
      
    Current pager: stdout
      
    Using outfile: "
      
    Using delimiter: ;
      
    Server version: 3.23.56-log
      
    Protocol version: 10
      
    Connection: Localhost via UNIX socket
      
    Client characterset: latin1
      
    Server characterset: latin1
      
    UNIX socket: /tmp/MySQL_3311.sock
      
    Uptime: 62 days 21 hours 21 min 57 secThreads: 1 Questions: 584402560 Slow queries: 424 Opens: 59664208 Flush tables: 1 Open tables: 64 Queries per second avg: 107.551

### MySQL -help

MySQL –help | grep Distrib
  
MySQL Ver 14.7 Distrib 4.1.10a, for redhat-linux-gnu (i686)
