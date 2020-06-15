---
title: '绝对路径${pageContext.request.contextPath}'
author: wiloon
type: post
date: 2012-10-31T07:21:27+00:00
url: /?p=4591
categories:
  - Java
  - Web

---
<div id="header">



  
    <div id="cnblogs_post_body">
      
        登录后第一次点击正确,鼠标放在链接上，出现正确url&#8212;&#8212;&#8212;&#8212;&#8211;http://localhost:8080/ibatisORM/listuser/2
      
      
      
        但点击之后，链接会变成http://localhost:8080/ibatisORM/listuser/listuser/2
      
      
      
        加上绝对路径${pageContext.request.contextPath}
      
      
      
        &#8212;-<a href="${pageContext.request.contextPath}/listuser/1" style="font-size:13px;">首页</a>
      
      
      
        为了解决不同部署方式的差别，在所有非struts标签的路径前加${pageContext.request.contextPath}，如原路径为：
 "/images/title.gif"，改为
      
      
      
        "${pageContext.request.contextPath}/images/title.gif"
 代码” ${pageContext.request.contextPath}”的作用是取出部署的应用程序名，这样不管如何部署，所用路径都是正确的。
 缺点：
 操作不便，其他工具无法正确解释${pageContext.request.contextPath}
      
      
      
        在使用的时候可以使用${pageContext.request.contextPath}，也同时可以使用<%=request.getContextPath()%>达到同样的效果，同时，也可以将${pageContext.request.contextPath}，放入一个JSP文件中，将用C：set放入一个变量中，然后在用的时候用EL表达式取出来。
      
    
  
