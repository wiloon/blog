---
title: spring 事务 
author: "-"
date: 2012-02-02T05:10:12+00:00
url: /?p=2227
categories:
  - Inbox
tags:
  - reprint
---
## spring 事务

## @Transactional

==========================
使用 @Transactional 注解
==========================

使用 @Transactional 的要点有:

1. 在DAO 层使用 JdbcTemplate 实现DB操作, 在 Service 的实现类上加上 @Transactional 注解, 不推荐在 Service 接口上加 @Transactional 注解.
2. 需要进行事务控制的方法, 必须是 public 方法, 同时要打上 @Transactional 注解.
3. 也可以在Class上加上 @Transactional 注解, 这样相当于给每个 public 函数加上了 @Transactional 注解, 当然我们还可以在其中的函数上加该注解, 这时候将以函数上的设置为准.

@Transactional 使用陷阱:

1. 只有 public 方法打上 @Transactional 注解, 事务控制才能生效.
2. 注意自调用问题, @Transactional 注解仅在外部类的调用才生效, 原因是使用 Spring AOP 机制造成的. 所以: 主调函数如果是本Service类, 应该也要打上 @Transactional, 否则事务控制被忽略.
3. 缺省的情况下, 只有 RuntimeException 类异常才会触发回滚. 如果在事务中抛出其他异常,并期望回滚事务, 必须设定 rollbackFor 参数.
     例子: @Transactional(propagation=Propagation.REQUIRED,rollbackFor= MyException.class)
4. 如果主调函数和多个被调函数都加了 @Transactional 注解, 则整个主调函数将是一个统一的事务控制范围, 甚至它们分属多个Service也能被统一事务控制着
5. 通常我们应该使用 Propagation.REQUIRED, 但需要说明的是, 如果一个非事务方法顺序调用了"两个不同service bean"的事务函数, 它们并不在同一个事务上下文中, 而是分属于不同的事务上下文.

><https://www.cnblogs.com/harrychinese/p/SpringBoot_jdbc_transaction.html>
