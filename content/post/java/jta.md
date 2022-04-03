---
title: JTA
author: "-"
date: 2011-12-25T03:52:55+00:00
url: /?p=1962
categories:
  - Java

tags:
  - reprint
---
## JTA
JTA，即Java Transaction API，译为Java事务API。


  JTA允许应用程序执行分布式事务处理——在两个或多个网络计算机资源上访问并且更新数据。JDBC驱动程序的JTA支持极大地增强了数据访问能力。 
  
  
  
    JTA和JTS
  
  
    Java事务API (JTA: Java Transaction API) 和它的同胞Java事务服务 (JTS: Java Transaction Service) ，为J2EE平台提供了分布式事务服务 (distributed transaction) 。
  
  
  
    一个分布式事务 (distributed transaction) 包括一个事务管理器 (transaction manager) 和一个或多个资源管理器(resource manager)。
  
  
  
    一个资源管理器 (resource manager) 是任意类型的持久化数据存储。
  
  
  
    事务管理器 (transaction manager) 承担着所有事务参与单元者的相互通讯的责任。
  
  
  
    JTA与JDBC
  
  
    JTA事务比JDBC事务更强大。一个JTA事务可以有多个参与者，而一个JDBC事务则被限定在一个单一的数据库连接。下列任一个Java平台的组件都可以参与到一个JTA事务中: JDBC连接、JDO PersistenceManager 对象、JMS 队列、JMS 主题、企业JavaBeans (EJB) 、一个用J2EE Connector Architecture 规范编译的资源分配器。
  
