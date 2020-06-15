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
</div>

<div>
  <div>
    <div id="cnblogs_post_body">
      <p>
        登录后第一次点击正确,鼠标放在链接上，出现正确url&#8212;&#8212;&#8212;&#8212;&#8211;http://localhost:8080/ibatisORM/listuser/2
      </p>
      
      <p>
        但点击之后，链接会变成http://localhost:8080/ibatisORM/listuser/listuser/2
      </p>
      
      <p>
        加上绝对路径${pageContext.request.contextPath}
      </p>
      
      <p>
        &#8212;-<a href=&#8221;${pageContext.request.contextPath}/listuser/1" style=&#8221;font-size:13px;&#8221;>首页</a>
      </p>
      
      <p>
        为了解决不同部署方式的差别，在所有非struts标签的路径前加${pageContext.request.contextPath}，如原路径为：
 "/images/title.gif&#8221;，改为
      </p>
      
      <p>
        "${pageContext.request.contextPath}/images/title.gif&#8221;
 代码” ${pageContext.request.contextPath}”的作用是取出部署的应用程序名，这样不管如何部署，所用路径都是正确的。
 缺点：
 操作不便，其他工具无法正确解释${pageContext.request.contextPath}
      </p>
      
      <div>
        在使用的时候可以使用${pageContext.request.contextPath}，也同时可以使用<%=request.getContextPath()%>达到同样的效果，同时，也可以将${pageContext.request.contextPath}，放入一个JSP文件中，将用C：set放入一个变量中，然后在用的时候用EL表达式取出来。
      </div>
    </div>
  </div>
</div>