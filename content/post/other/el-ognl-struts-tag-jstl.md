---
title: EL, Ognl, Struts Tag, JSTL
author: "-"
date: 2013-04-04T11:06:30+00:00
url: /?p=5377
categories:
  - Java
tags:$
  - reprint
---
## EL, Ognl, Struts Tag, JSTL
<http://www.cnblogs.com/LeneJay/archive/2011/11/14/2248218.html>

JavaWeb 默认的语法，除HTML 外，共有: 

1. <% 可以使用Java语言 %>

2. <%!  可以使用Java 语言定义变量或函数，是public 类型的 %>

3. <%= 变量 %> 可以取值

4. <%@  指令元素  %>

5. <jsp:include、forward  …… ></jsp:include、forward> 默认标签语言


以上五种是Javaweb 默认语法，除第五种是标签语言外，其余上四种都是JavaWeb 默认的语法格式。


此后，JSP2.0之后，引入了 EL 表达语言和 扩展了 标签语言 称为:JSTL 。


EL 表达式语言，其实可以说是一套独立的编程语言，有自己的语法格式，算式运算符，关系运算符，逻辑运算符，条件运算符等等完整的体系，加上还有一些内置的对象，虽然这些内置的对象都需要Java 支持，但也不失为一套完善的编程语言了。


EL 主要编写在 后缀为.jsp 的页面中，虽然它有自己的语法格式，但其实它的本质是Java类，它会通过Web容器转为特定的Java代码，而后运行在Java虚拟机中，只是为了规范 和方便，所以SUN公司推出了它，但发展到现在，它已经称为JavaWeb不可分割的一部分 (虽然JSP页面如今少写业务逻辑) 


JSTL 是 JSP2.0 后引入的默认标签库，记得默认语法中，第五条就是 <jsp:xxx /> ，而JSTL可以说是那个的升级版，增加了很多可以直接在 jsp 页面中使用，而格式跟普通HTML类似的标签。


接下来，谈谈，Struts2.x 中的OGNL  表达式 和 标签 Struts Tag 。


Struts2.x 中的 OGNL 可以说是取代了 默认的EL表达式，它自身本就是 EL 表达式，它与默认的EL表达式语言，区别共有多少，我没有仔细去了解，只能说说大致了解的。

1.   取值范围: 

a)         默认的EL表达式的格式 ${ }，它能单独使用，默认取值范围在 : page (PageContext)

b)        OGNL 表达式常用的格式为 # ，还有 $ % 等，默认的取值范围是: valueStack 值栈。

2.    使用范围

a)         默认的EL表达式能单独使用。

b)        OGNL 需要和 标签 Struts Tag 联合使用

3.   优势

a)         EL 表达式 在于有完整的体系，功能完善，

b)        OGNL 没有那些运算，关系，条件，逻辑等等运算符，但它在于能单独访问对象 (类) ，包括静态类，静态方法等

4.   搭档

a)         EL + JSTL 。默认的EL虽然能完成大部分功能，但天生缺少的一些，比如遍历等，就需要配合JSTL使用，功能更为完善。

b)        OGNL + Struts Tag 。OGNL 负责取值，Struts Tag 负责控制流程。分工明确！


Struts 2.x 的 Struts Tag ，是Struts 默认的标签库，和OGNL 一起使用功能更强大。一般来说，OGNL 取值，而Struts Tag 控制流程和显示。

它取代了 默认的JSTL标签库。

--------------------------

不管是标签，还是表达式语言，都是为了规范在JSP页面的语法，尽量遵循HTML标签式语言，令一些非专业程序员也能使用这些语法开发JSP页面，和保持JSP页面的简洁。

--------------------------