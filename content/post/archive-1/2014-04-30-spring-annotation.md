---
title: spring annotation
author: w1100n
type: post
date: 2014-04-30T01:55:01+00:00
url: /?p=6569
categories:
  - Uncategorized

---
<span style="color: #393939;">@Component；@Controller；@Service；@Repository 

<span style="color: #393939;"> 在annotaion配置注解中用@Component来表示一个通用注释用于说明一个类是一个spring容器管理的类。即就是该类已经拉入到spring的管理中了。而@Controller, @Service, @Repository是@Component的细化，这三个注解比@Component带有更多的语义，它们分别对应了控制层、服务层、持久层的类。 

@Service用于标注业务层组件,对象名默认是类名（头字母小写），如果想自定义，可以@Service("foo")这样来指定，这种bean默认是单例的，如果想改变，可以使用@Service("foo") @Scope("prototype")来改变。

@Controller用于标注控制层组件（如struts中的action）

@Repository用于标注数据访问组件，即DAO组件

@Component泛指组件，当组件不好归类的时候，我们可以使用这个注解进行标注。

@Autowired Spring自己定义的注解,

JSR-250规范定义的注解

@Resource @Resource的作用相当于@Autowired，只不过@Autowired按byType自动注入，而@Resource默认按 byName自动注入


http://www.chinasb.org/archives/2011/06/2443.shtml

http://www.cnblogs.com/chenzhao/archive/2012/02/25/2367978.html