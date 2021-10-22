---
title: JSP 动态INCLUDE 静态INCLUDE
author: "-"
type: post
date: 2012-09-21T08:03:28+00:00
url: /?p=4157
categories:
  - Java

---
## JSP 动态INCLUDE 静态INCLUDE
动态INCLUDE
  
用jsp:include动作实现 <jsp:include page="included.jsp" flush="true" />它总是会检查所含文件中的变化，适合用于包含动态页面，并且可以带参数。
  
静态INCLUDE
  
用include伪码实现,定不会检查所含文件的变化，适用于包含静态页面<%@ include file="included.htm" %>

===================================================================

1. 静态include的结果是把其他jsp引入当前jsp,两者合为一体
  
动态include的结构是两者独立,直到输出时才合并( 看看jsp生成的java文件就可以知道了)

2.正是因为这样,动态include的jsp文件独立性很强,是一个单独的jsp文件,需要使用的对象,页面设置,都必须有自己创建,当然,还好它和include它的页面的request范围是一致的.

而静态include纯粹是把代码写在外面的一种共享方法,所有的变量都是可以和include它的主文件共享,两者高度紧密结合,不能有变量同名的冲突.而页面设置也可以借用主文件的.