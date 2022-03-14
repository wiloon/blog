---
title: Android之ContentProvider
author: "-"
date: 2014-07-31T02:09:44+00:00
url: /?p=6859
categories:
  - Uncategorized

tags:
  - reprint
---
## Android之ContentProvider
http://www.cnblogs.com/devinzhang/archive/2012/01/20/2327863.html

Android之ContentProvider

1.适用场景

1) ContentProvider为存储和读取数据提供了统一的接口

2) 使用ContentProvider,应用程序可以实现数据共享

3) android内置的许多数据都是使用ContentProvider形式,供开发者调用的(如视频,音频,图片,通讯录等)

2.相关概念介绍

1) ContentProvider简介
  
当应用继承ContentProvider类,并重写该类用于提供数据和存储数据的方法,就可以向其他应用共享其数据。虽然使用其他方法也可以对外共享数据,但数据访问方式会因数据存储的方式而不同,如: 采用文件方式对外共享数据,需要进行文件操作读写数据；采用sharedpreferences共享数据,需要使用sharedpreferences API读写数据。而使用ContentProvider共享数据的好处是统一了数据访问方式。

2) Uri类简介

Uri uri = Uri.parse("content://com.changcheng.provider.contactprovider/contact")

在Content Provider中使用的查询字符串有别于标准的SQL查询。很多诸如select, add, delete, modify等操作我们都使用一种特殊的URI来进行,这种URI由3个部分组成, "content://", 代表数据的路径,和一个可选的标识数据的ID。以下是一些示例URI:

content://media/internal/images 这个URI将返回设备上存储的所有图片
  
content://contacts/people/ 这个URI将返回设备上的所有联系人信息
  
content://contacts/people/45 这个URI返回单个结果 (联系人信息中ID为45的联系人记录) 

尽管这种查询字符串格式很常见,但是它看起来还是有点令人迷惑。为此,Android提供一系列的帮助类 (在android.provider包下) ,里面包含了很多以类变量形式给出的查询字符串,这种方式更容易让我们理解一点,因此,如上面content://contacts/people/45这个URI就可以写成如下形式: 

Uri person = ContentUris.withAppendedId(People.CONTENT_URI, 45);

然后执行数据查询:

Cursor cur = managedQuery(person, null, null, null);

这个查询返回一个包含所有数据字段的游标,我们可以通过迭代这个游标来获取所有的数据: 