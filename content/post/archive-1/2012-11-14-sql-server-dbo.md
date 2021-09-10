---
title: sql server dbo
author: "-"
type: post
date: 2012-11-14T08:19:43+00:00
url: /?p=4677
categories:
  - DataBase
tags:
  - SQLServer

---
<pre id="best-answer-content" data-accusearea="aContent">DBO是每个数据库的默认用户，具有所有者权限，即DbOwner

通过用DBO作为所有者来定义对象，能够使数据库中的任何用户引用而不必提供所有者名称。
比如: 你以User1登录进去并建表Table，而未指定DBO，
当用户User2登进去想访问Table时就得知道这个Table是你User1建立的，要写上User1.Table，如果他不知道是你建的，则访问会有问题。
如果你建表时把所有者指给了Dbo，则别的用户进来时写上Dbo.Table就行了，不必知道User1。
不光表是如此，视图等等数据库对象建立时也要如此才算是好。

建表、存储过程、视图等数据库对象时，其对应的所有者是创建它的用户。则除了该用户其他登录用户要引用这些东西时，都要加上前缀，很是麻烦。而且，程序因此易出错，你查来查去问题确出在这，浪费你时间。