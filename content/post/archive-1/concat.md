---
title: concat
author: "-"
date: 2013-07-11T06:42:51+00:00
url: /?p=5642
categories:
  - DataBase

tags:
  - reprint
---
## concat
和其他数据库系统类似，[Oracle][1]字符串连接使用"||"进行字符串拼接，其使用方式和MSSQLServer中的加号"+"一样。

比如执行下面的SQL语句: 
  
SELECT '工号为'||FNumber||'的员工姓名为'||FName FROM T_Employee
  
WHERE FName IS NOT NULL

除了"||"，Oracle还支持使用CONCAT()函数进行字符串拼接，比如执行下面的SQL语句: 
  
SELECT CONCAT('工号:',FNumber) FROM T_Employee

如果CONCAT中连接的值不是字符串，Oracle会尝试将其转换为字符串，比如执行下面的SQL语句: 
  
SELECT CONCAT('年龄:',FAge) FROM T_Employee

与MySQL的CONCAT()函数不同，Oracle的CONCAT()函数只支持两个参数，不支持两个以上字符串的拼接，比如下面的SQL语句在Oracle中是错误的: 
  
SELECT CONCAT('工号为',FNumber,'的员工姓名为',FName) FROM T_Employee
  
WHERE FName IS NOT NULL
  
运行以后Oracle会报出下面的错误信息: 
  
参数个数无效

如果要进行多个字符串的拼接的话，可以使用多个CONCAT()函数嵌套使用，上面的SQL可以如下改写: 
  
SELECT CONCAT(CONCAT(CONCAT('工号为',FNumber),'的员工姓名为'),FName) FROM
  
T_Employee
  
WHERE FName IS NOT NULL

 [1]: http://database.51cto.com/art/201010/231973.htm