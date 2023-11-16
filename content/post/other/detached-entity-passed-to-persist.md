---
title: detached entity passed to persist
author: "-"
date: 2014-05-30T01:08:45+00:00
url: /?p=6697
categories:
  - Inbox
tags:
  - JPA

---
## detached entity passed to persist

病理特征: Caused by: org.hibernate.PersistentObjectException: detached entity passed to persist: com.xxx.Xxx

简单地说，发生此异常即是一个游离的对象要被持久化(save)时，其ID既要ORM框架为它生成ID值，而此实体的ID却已然有值。对于新手容易出现此异常，但一些有经验的程序员有时也会碰到此问题，笔者就有一次，故与网友们"分享这次遭遇"。

让ORM为即将要持久的实体生成ID值(ORM的主键策略)，是典型的做法，例如有自增长(即便是DBMS来做)、UUID，Hibernate框架则更多。因此，不能手工为此实体赋上ID值。笔者设计主要实体时，通常用UUID作主键，很显然它是字符型的。但是，有时会发现form表单为其赋一个长度为0的字符串，看html代码:

```xml
<input name="id" type="text" id="id" value=""/>
```

注意 value=""

如果是增加，则不需要在form表单中安置这么个控件，笔者通常将增加和修改实体在一个form表单中完成，笔者很喜欢用Spring MVC。这时id字段被Spring MVC包装到实体中就有值了(其值是长度为0的空字符串)。ORM保存时上面的异常就来了。解决的办法很多，笔者是为其实体做一个属性编辑器，在编辑器判断ID是否为空且长度是否为0，若是，则置入一个null。在保存前检查一下ID也是一种解决办法。

有时在一对一、一对多保存时，关联方也会存在这种情况，所以关键检查ID字段就可以了

[http://howsun.blog.sohu.com/129035715.html](http://howsun.blog.sohu.com/129035715.html)
