---
title: Thymeleaf
author: wiloon
type: post
date: 2017-02-23T02:03:53+00:00
url: /?p=9869
categories:
  - Uncategorized

---
https://www.tianmaying.com/tutorial/using-thymeleaf


Thymeleaf是一款用于渲染XML/XHTML/HTML5内容的模板引擎。类似JSP，Velocity，FreeMaker等，它也可以轻易的与Spring MVC等Web框架进行集成作为Web应用的模板引擎。与其它模板引擎相比，Thymeleaf最大的特点是能够直接在浏览器中打开并正确显示模板页面，而不需要启动整个Web应用。

Thymeleaf初探
  
相比于其他的模板引擎，Thymeleaf最大的特点是通过HTML的标签属性渲染标签内容，以下是一个Thymeleaf模板例子：

<!DOCTYPE html SYSTEM "http://www.thymeleaf.org/dtd/xhtml1-strict-thymeleaf-4.dtd">

<html xmlns="http://www.w3.org/1999/xhtml"
  
xmlns:th="http://www.thymeleaf.org">

<head>
  
<title>Good Thymes Virtual Grocery</title>
  
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  
<link rel="stylesheet" type="text/css" media="all"
  
href="../../css/gtvg.css" th:href="@{/css/gtvg.css}" />
  
</head>

<body>

<p th:text="#{home.welcome}">Welcome to our grocery store!

</body>

</html>

这是一段标准的HTML代码，这也就意味着通过浏览器直接打开它是可以正确解析它的结构并看到页面的样子。相比去其他的模板引擎在指定的位置通过${}等表达式进行渲染，Thymeleaf则是一种针对HTML/XML定制的模板语言（当然它可以被扩展），它通过标签中的th:text属性来填充该标签的一段内容。上例中，<p th:text="#{home.welcome}">Welcome to our grocery store!意味着标签中的内容会被表达式#{home.welcome}的值所替代，无论模板中它的内容是什么，之所以在模板中"多此一举"地填充它的内容，完全是为了它能够作为原型在浏览器中直接显示出来。

标准表达式语法
  
变量
  
Thymeleaf模板引擎在进行模板渲染时，还会附带一个Context存放进行模板渲染的变量，在模板中定义的表达式本质上就是从Context中获取对应的变量的值：

Today is: <span th:text="${today}">13 february 2011.

假设today的值为2015年8月14日，那么渲染结果为：Today is: 2015年8月14日.。可见Thymeleaf的基本变量和JSP一样，都使用${.}表示获取变量的值。

URL
  
URL在Web应用模板中占据着十分重要的地位，需要特别注意的是Thymeleaf对于URL的处理是通过语法@{...}来处理的。Thymeleaf支持绝对路径URL：

<a th:href="@{http://www.thymeleaf.org}">Thymeleaf</a>

同时也能够支持相对路径URL：

当前页面相对路径URL——user/login.html，通常不推荐这样写。
  
Context相关URL——/static/css/style.css
  
另外，如果需要Thymeleaf对URL进行渲染，那么务必使用th:href，th:src等属性，下面是一个例子

<!- Will produce 'http://localhost:8080/gtvg/order/details?orderId=3' (plus rewriting) ->
  
<a href="details.html"
  
th:href="@{http://localhost:8080/gtvg/order/details(orderId=${o.id})}">view</a>

<!- Will produce '/gtvg/order/details?orderId=3' (plus rewriting) ->
  
<a href="details.html" th:href="@{/order/details(orderId=${o.id})}">view</a>

<!- Will produce '/gtvg/order/3/details' (plus rewriting) ->
  
<a href="details.html" th:href="@{/order/{orderId}/details(orderId=${o.id})}">view</a>

几点说明：

上例中URL最后的(orderId=${o.id})表示将括号内的内容作为URL参数处理，该语法避免使用字符串拼接，大大提高了可读性
  
@{...}表达式中可以通过{orderId}访问Context中的orderId变量
  
@{/order}是Context相关的相对路径，在渲染时会自动添加上当前Web应用的Context名字，假设context名字为app，那么结果应该是/app/order
  
字符串替换
  
很多时候可能我们只需要对一大段文字中的某一处地方进行替换，可以通过字符串拼接操作完成：

<span th:text="'Welcome to our application, ' + ${user.name} + '!'">

一种更简洁的方式是：

<span th:text="|Welcome to our application, ${user.name}!|">

当然这种形式限制比较多，|...|中只能包含变量表达式${...}，不能包含其他常量、条件表达式等。

运算符
  
在表达式中可以使用各类算术运算符，例如+, -, *, /, %

th:with="isEven=(${prodStat.count} % 2 == 0)"

逻辑运算符>, <, <=,>=，==,!=都可以使用，唯一需要注意的是使用<,>时需要用它的HTML转义符：

th:if="${prodStat.count} > 1"
  
th:text="'Execution mode is ' + ( (${execMode} == 'dev')? 'Development' : 'Production')"

循环
  
渲染列表数据是一种非常常见的场景，例如现在有n条记录需要渲染成一个表格<table>，该数据集合必须是可以遍历的，使用th:each标签：

<body>
  
<h1>Product list</h1>

<table>
  
<tr>
  
<th>NAME</th>
  
<th>PRICE</th>
  
<th>IN STOCK</th>
  
</tr>
  
<tr th:each="prod : ${prods}">
  
<td th:text="${prod.name}">Onions</td>
  
<td th:text="${prod.price}">2.41</td>
  
<td th:text="${prod.inStock}? #{true} : #{false}">yes</td>
  
</tr>
  
</table>
  
<a href="../home.html" th:href="@{/}">Return to home</a>
  
  
</body>

可以看到，需要在被循环渲染的元素（这里是<tr>）中加入th:each标签，其中th:each="prod : ${prods}"意味着对集合变量prods进行遍历，循环变量是prod在循环体中可以通过表达式访问。

条件求值
  
If/Unless
  
Thymeleaf中使用th:if和th:unless属性进行条件判断，下面的例子中，<a>标签只有在th:if中条件成立时才显示：

<a th:href="@{/login}" th:unless=${session.user != null}>Login</a>

th:unless于th:if恰好相反，只有表达式中的条件不成立，才会显示其内容。

Switch
  
Thymeleaf同样支持多路选择Switch结构：

<div th:switch="${user.role}">
  
<p th:case="'admin'">User is an administrator
  
<p th:case="#{roles.manager}">User is a manager
  

默认属性default可以用*表示：

<div th:switch="${user.role}">
  
<p th:case="'admin'">User is an administrator
  
<p th:case="#{roles.manager}">User is a manager
  
<p th:case="*">User is some other thing
  

Utilities
  
为了模板更加易用，Thymeleaf还提供了一系列Utility对象（内置于Context中），可以通过#直接访问：

#dates
  
#calendars
  
#numbers
  
#strings
  
arrays
  
lists
  
sets
  
maps
  
...
  
下面用一段代码来举例一些常用的方法：

#dates
  
/*
  
* Format date with the specified pattern
  
* Also works with arrays, lists or sets
  
*/
  
${#dates.format(date, 'dd/MMM/yyyy HH:mm')}
  
${#dates.arrayFormat(datesArray, 'dd/MMM/yyyy HH:mm')}
  
${#dates.listFormat(datesList, 'dd/MMM/yyyy HH:mm')}
  
${#dates.setFormat(datesSet, 'dd/MMM/yyyy HH:mm')}

/*
  
* Create a date (java.util.Date) object for the current date and time
  
*/
  
${#dates.createNow()}

/*
  
* Create a date (java.util.Date) object for the current date (time set to 00:00)
  
*/
  
${#dates.createToday()}

#strings
  
/*
  
* Check whether a String is empty (or null). Performs a trim() operation before check
  
* Also works with arrays, lists or sets
  
*/
  
${#strings.isEmpty(name)}
  
${#strings.arrayIsEmpty(nameArr)}
  
${#strings.listIsEmpty(nameList)}
  
${#strings.setIsEmpty(nameSet)}

/*
  
* Check whether a String starts or ends with a fragment
  
* Also works with arrays, lists or sets
  
*/
  
${#strings.startsWith(name,'Don')} // also array\*, list\* and set*
  
${#strings.endsWith(name,endingFragment)} // also array\*, list\* and set*

/*
  
* Compute length
  
* Also works with arrays, lists or sets
  
*/
  
${#strings.length(str)}

/*
  
* Null-safe comparison and concatenation
  
*/
  
${#strings.equals(str)}
  
${#strings.equalsIgnoreCase(str)}
  
${#strings.concat(str)}
  
${#strings.concatReplaceNulls(str)}

/*
  
* Random
  
*/
  
${#strings.randomAlphanumeric(count)}

页面即原型
  
在Web开发过程中一个绕不开的话题就是前端工程师与后端工程师的写作，在传统Java Web开发过程中，前端工程师和后端工程师一样，也需要安装一套完整的开发环境，然后各类Java IDE中修改模板、静态资源文件，启动/重启/重新加载应用服务器，刷新页面查看最终效果。

但实际上前端工程师的职责更多应该关注于页面本身而非后端，使用JSP，Velocity等传统的Java模板引擎很难做到这一点，因为它们必须在应用服务器中渲染完成后才能在浏览器中看到结果，而Thymeleaf从根本上颠覆了这一过程，通过属性进行模板渲染不会引入任何新的浏览器不能识别的标签，例如JSP中的<form:input>，不会在Tag内部写表达式。整个页面直接作为HTML文件用浏览器打开，几乎就可以看到最终的效果，这大大解放了前端工程师的生产力，它们的最终交付物就是纯的HTML/CSS/JavaScript文件。