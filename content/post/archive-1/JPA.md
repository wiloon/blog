---
title: JPA的merge和persist ！
author: "-"
date: -001-11-30T00:00:00+00:00
draft: true
url: /?p=6812
categories:
  - Uncategorized
tags:
  - JPA

---
## JPA的merge和persist ！
原创作品，允许转载，转载时请务必以超链接形式标明文章 原始出处 、作者信息和本声明。否则将追究法律责任。http://pz0513.blog.51cto.com/443986/113098
  
原来merge()也有persist()的作用！
  
persist会把传进去的实体放到持久化上下文中，此时如果持久化上下文中有了这个实体，就会抛出javax.persistence.EntityExistsException，没有的话事务提交的时候把那个对象加进数据库中，如果数据库中已经存在了那个对象 (那一行) ，就会抛出com.MySQL.jdbc.exceptions.jdbc4.MySQLIntegrityConstraintViolationException；

而merge会在持久化上下文中生成传进去的实体的受管版本，如果已经有了受管版本，那也不会抛出异常，然后把那个受管的实体返回出来，事务提交的时候如果数据库中不存在那个对象 (那一行) ，就把把那个受管的加进去，存在的话就替换掉原来的数据。merge是如果持久化上下文中有了受管版本，那就更新，没有就复制一份，返回受管的。

再次总结persist (①，②-③，④-⑤) : 
  
 (这里说的抛出的异常都是指对象 (或者数据库中的行) 重复的异常) 
  
① 如果persist的是一个受管实体 (即已经在上下文中) ，就不会抛出异常。
  
②如果persist的是一个游离实体 (即上下文中没有它) ，而上下文中又没有它的受管版本，数据库中也没有，也不会抛出异常，而会把这个实体写进数据库中。
  
③如果persist的是一个游离实体 (即上下文中没有) ，而上下文中又没有它的受管版本，数据库却有这个实体，那么EntityManager在persist它的时候不会抛出异常，但是事务提交的时候就会抛出异常: 
  
Caused by: com.MySQL.jdbc.exceptions.jdbc4.MySQLIntegrityConstraintViolationException: Duplicate entry '7' for key 1；
  
④如果persist的是一个游离实体 (即上下文中没有) ，而上下文中却有它的受管版本，数据库中又没有这个实体，那么还是不会抛出异常，而是把它的受管版本加进去 (不是那个游离的，是那个受管的！)  (即，这种情况persist和没persist是一样的！) 。
  
⑤如果persist的是一个游离实体 (即上下文中没有) ，而上下文中却有它的受管版本，数据库中也有了这个实体，那么EntityManager在persist它的时候就会抛出异常: javax.persistence.EntityExistsException
  
而merge就不会抛出什么对象重复的异常的了。。
  
本文出自 "辽源大火的奋斗历程" 博客，请务必保留此出处http://pz0513.blog.51cto.com/443986/113098