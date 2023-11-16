---
title: Fluent Interface, fluent manner, fluent风格, 流式接口, 流式风格
author: "-"
date: 2015-12-23T04:52:56+00:00
url: /?p=8596
categories:
  - Inbox
tags:
  - reprint
---
## Fluent Interface, fluent manner, fluent风格, 流式接口, 流式风格

这个故事是从下面这样一个对外暴露接口的调用开始的。

```java
queryUserEvent event = new QueryUserEvent();
event.setName(name);
event.setAge(18);
event.setType(QueryUserEvent.TYPE_NORMAL);
event.setSex(QueryUserEvent.SEX_MALE);
//...
List<User> userList = userService.query(event);
```

我想做的事情其实很简单,我想查询一个用户列表,可是接口参数的拼装让我感到头疼,这样的代码太过啰嗦,我希望有可读性更好的解决办法。

P兄台说,如果我直接传入一个user对象,是不是可以避开了这个未必带来多少好处的event？

User user = new User();
  
user.setName(name);
  
user.setAge(18);
  
user.setSex(QueryUserEvent.SEX_MALE);
  
……
  
List<User> userList = userService.query(user, UserService.QUERY_TYPE_NORMAL);
  
我有时候会考虑你说的办法的,可是,你没有解决实际的问题,我现在的最大问题在于,这一堆的setXXX方法,它破坏了我构造这个查询条件对象的流畅性。

他紧接着说,那要不然,我们把setXXX方法的劳动省下来,让构造器来替我们完成这个任务吧:

User user = new User(name, 18, QueryUserEvent.SEX_MALE, ……);
  
List<User> userList = userService.query(user, UserService.QUERY_TYPE_NORMAL);
  
我说,你的办法看起来不错,不过有时候按你的办法做,我的构造方法会变得臃肿无比,比如出现十多个参数；

另外还有一个问题,假如说,我的查询条件是简单的 (我只需要根据年龄查询) ,那么其它的参数都要写成null,类似这样子:

User user = new User(null, 18, null, null, null, null, ……);
  
List<User> userList = userService.query(user, UserService.QUERY_TYPE_NORMAL);
  
天,让谁去阅读这样的代码,他都不会喜欢的。

而且,有时候情形变得复杂,比如,我不是要查询18岁的所有user,而是要查询大于18岁的所有user,你的办法似乎行不通了呢……

你真是一个麻烦的人,他说,这样吧,我定义一个Condition,他给查询条件带来了灵活的组装方式:

UserQueryCondition condition = new UserQueryCondition();
  
condition.setAge(Condition.GREATER_THAN, 18);
  
List<User> userList = userService.query(condition, UserService.QUERY_TYPE_NORMAL);
  
不过,他补充道,如果在JavaScript中,我可以采取的办法要好得多。如果要查询18岁的和符合其他条件的用户,可以这样写:

userService.query({
  
name : name,
  
age : 18,
  
sex : User.SEX_MALE
  
}, UserService.QUERY_TYPE_NORMAL);
  
如果要大于18岁呢,可以这样写:

userService.query({
  
name : name,
  
greaterThan : {
  
age : 18
  
},
  
sex : User.SEX_MALE
  
}, UserService.QUERY_TYPE_NORMAL);
  
不过,他接着说,在Java里面好像还没有类似简洁的表示方法……

万幸的是,有一种接口连续调用的风格,叫做"Fluent Interface",可以让这个问题写成这样一种有趣的实现:

List<User> userList = new UserService().setName(name).setAge(18).setSex(User.SEX_MALE).query(UserService.QUERY_TYPE_NORMAL);
  
大于18岁的话,这样写:

List<User> userList = new UserService().setName(name).greaterThan(new User().setAge(18)).setSex(User.SEX_MALE).query(UserService.QUERY_TYPE_NORMAL);
  
我想,这样的设计如果在数学计算的时候,会显得有用得多,看这样一个算式:

ln(sin((x+y)的平方))
  
如果用传统的方式来实现的话,应该类似这样子:

Math.log(Math.sin(Math.sqrt(x + y)))
  
显然,它的可读性不如Fluent Interface来得好:

new MyNumber(x+y).sqrt().sin().log()
  
这样的例子还有很多,比如在JQuery中的使用,在EasyMock中的使用等等。看下面的例子,这样构建一个DOM树,是不是比单纯的字符串拼接,要好理解一些呢？

$("#div1")
  
.div({id:"subDIV"})
  
.h1("A Title")
  
.a({href:"xxx"})
  
.a()
  
.h1()
  
.div();
  
《CommandQuerySeperation》这篇文章把一个对象的方法大致分成下面两种:

Queries: Return a result and do not change the observable state of the system (are free of side effects).

Commands: Change the state of a system but do not return a value.

对于Fluent Interface而言,它的接口调用既改变了对象的状态,又返回了对象 (this或其他) ,并不属于上面的两种类型。

文章未经特殊标明皆为本人原创,未经许可不得用于任何商业用途,转载请保持完整性并注明来源链接《四火的唠叨》

    关于接口设计,还有 Fluent Interface,这种有趣的接口设计风格
  
[https://www.raychase.net/263/embed#?secret=yAm220vjxR](https://www.raychase.net/263/embed#?secret=yAm220vjxR)
