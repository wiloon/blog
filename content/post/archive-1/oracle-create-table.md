---
title: oracle create table
author: "-"
date: 2014-03-04T07:38:13+00:00
url: /?p=6328
categories:
  - Uncategorized

---
## oracle create table
http://zhoujian0610.blog.163.com/blog/static/56567658201052815913549/

创建表(Create table)语法详解
  
1. ORACLE常用的字段类型
  
ORACLE常用的字段类型有
  
VARCHAR2 (size) 可变长度的字符串, 必须规定长度
  
CHAR(size) 固定长度的字符串, 不规定长度默认值为１
  
NUMBER(p,s) 数字型p是位数总长度, s是小数的长度, 可存负数
  
最长38位. 不够位时会四舍五入.
  
DATE 日期和时间类型
  
LOB 超长字符, 最大可达4G
  
CLOB 超长文本字符串
  
BLOB 超长二进制字符串
  
BFILE 超长二进制字符串, 保存在数据库外的文件里是只读的.

数字字段类型位数及其四舍五入的结果
  
原始数值1234567.89
  
数字字段类型位数 存储的值
  
Number 1234567.89
  
Number(8) 12345678
  
Number(6) 错
  
Number(9,1) 1234567.9
  
Number(9,3) 错
  
Number(7,2) 错
  
Number(5,-2) 1234600
  
Number(5,-4) 1230000
  
Number(*,1) 1234567.9

2. 创建表时给字段加默认值 和约束条件
  
创建表时可以给字段加上默认值
  
例如 : 日期字段 DEFAULT SYSDATE
  
这样每次插入和修改时, 不用程序操作这个字段都能得到动作的时间

创建表时可以给字段加上约束条件
  
例如: 非空 NOT NULL
  
不允许重复 UNIQUE
  
关键字 PRIMARY KEY
  
按条件检查 CHECK (条件)
  
外键 REFERENCES 表名(字段名)

3. 创建表的例子
  
CREATE TABLE DEPT(
  
EPTNO NUMBER(2) CONSTRAINT PK_DEPT PRIMARY KEY,
  
DNAME VARCHAR2(14),
  
LOC VARCHAR2(13)) ;

CREATE TABLE region(
  
ID number(2) NOT NULL PRIMARY KEY,
  
postcode number(6) default '0' NOT NULL,
  
areaname varchar2(30) default ' ' NOT NULL);

4. 创建表时的命名规则和注意事项
  
1)表名和字段名的命名规则: 必须以字母开头,可以含符号A-Z,a-z,0-9,_,$,#
  
2)大小写不区分
  
3)不用SQL里的保留字, 一定要用时可用双引号把字符串括起来．
  
4)用和实体或属性相关的英文符号长度有一定的限制

注意事项:
  
1)建表时可以用中文的字段名, 但最好还是用英文的字段名
  
2)创建表时要把较小的不为空的字段放在前面, 可能为空的字段放在后面
  
3)建表时如果有唯一关键字或者唯一的约束条件,建表时自动建了索引
  
4)一个表的最多字段个数也是有限制的,254个.

5. 约束名的命名规则和语法
  
约束名的命名规则约束名如果在建表的时候没有指明,系统命名规则是SYS_Cn(n是数字)
  
约束名字符串的命名规则同于表和字段名的命名规则

6. 使用约束时的注意事项
  
约束里不能用系统函数,如SYSDATE和别的表的字段比较
  
可以用本表内字段的比较

想在事务处理后, 做约束的
  
检查
  
SQL> alter session set constraints deferred.


7. 由实体关系图到创建表的例子 s_dept
  
前提条件:已有region表且含唯一关键字的字段id
  
SQL> CREATE TABLE s_dept
  
(id NUMBER(7)
  
CONSTRAINT s_dept_id_pk PRIMARY KEY,
  
name VARCHAR2(25)
  
CONSTRAINT s_dept_name_nn NOT NULL,
  
region_id NUMBER(7)
  
CONSTRAINT s_dept_region_id_fk REFERENCES region (id),
  
CONSTRAINT s_dept_name_region_id_uk UNIQUE(name, region_id));

8. 较复杂的创建表例子
  
SQL> CREATE TABLE s_emp
  
(id NUMBER(7)
  
CONSTRAINT s_emp_id_pk PRIMARY KEY,
  
last_name VARCHAR2(25)
  
CONSTRAINT s_emp_last_name_nn NOT NULL,
  
first_name VARCHAR2(25),
  
userid VARCHAR2(8)
  
CONSTRAINT s_emp_userid_nn NOT NULL
  
CONSTRAINT s_emp_userid_uk UNIQUE,
  
start_date DATE DEFAULT SYSDATE,
  
comments VARCHAR2(25),
  
manager_id NUMBER(7),
  
title VARCHAR2(25),
  
dept_id NUMBER(7)
  
CONSTRAINT s_emp_dept_id_fk REFERENCES s_dept(id),
  
salary NUMBER(11,2),
  
commission_pct NUMBER(4,2)
  
CONSTRAINT s_emp_commission_pct_ck CHECK
  
(commission_pct IN(10,12.5,15,17.5,20)));

8. 通过子查询建表
  
通过子查询建表的例子
  
SQL>CREATE TABLE emp_41 AS SELECT id, last_name, userid, start_date
  
FROM s_emp WHERE dept_id = 41;

SQL> CREATE TABLE A as select * from B where 1=2;
  
只要表的结构.

10. 用子查询建表的注意事项
  
1)可以关连多个表及用集合函数生成新表,注意选择出来的字段必须有合法的字段名称,且不能重复。
  
2)用子查询方式建立的表,只有非空NOT NULL的约束条件能继承过来, 其它的约束条件和默认值都没有继承过来.
  
3)根据需要,可以用alter table add constraint ……再建立其它的约束条件,如primary key等.

11. Foreign Key的可选参数ON DELETE CASCADE
  
在创建Foreign Key时可以加可选参数:
  
ON DELETE CASCADE它的含义是如果删除外键主表里的内容,子表里相关的内容将一起被删除.
  
如果没有ON DELETE CASCADE参数,子表里有内容,父表里的主关键字记录不能被删除掉.

12. 如果数据库表里有不满足的记录存在,建立约束条件将不会成功.

13. 给表创建和删除同义词的例子
  
SQL> CREATE SYNONYM d_sum
  
2 FOR dept_sum_vu;

SQL> CREATE PUBLIC SYNONYM s_dept
  
2 FOR alice.s_dept;

SQL> DROP SYNONYM s_dept;