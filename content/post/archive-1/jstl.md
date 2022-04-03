---
title: jstl
author: "-"
date: 2013-01-20T13:54:30+00:00
url: /?p=5055
categories:
  - Uncategorized
tags:
  - JSP

---
## jstl
JSP 标准标记库 (JSP Standard Tag Library，JSTL) 是一个实现 Web 应用程序中常见的通用功能的定制标记库集，这些功能包括迭代和条件判断、数据管理格式化、XML 操作以及数据库访问。

JavaServer Pages (JSP) 是用于 J2EE 平台的标准表示层技术。JSP 技术提供了用于执行计算 (这些计算用来动态地生成页面内容) 的脚本编制元素和操作。脚本编制元素允许在 JSP 页面中包括程序源代码，在为响应用户请求而呈现页面时可以执行这些源代码。操作将计算操作封装到很象 HTML 或 XML 标记的标记中，JSP 页面的模板文本通常包含这些标记。JSP 规范只将几种操作定义成了标准，但从 JSP 1.1 开始，开发人员已经能够以定制标记库的方式创建其自己的操作了。

JSP 标准标记库 (JSTL) 是 JSP 1.2 定制标记库集，这些标记库实现大量服务器端 Java 应用程序常用的基本功能。通过为典型表示层任务 (如数据格式化和迭代或条件内容) 提供标准实现，JSTL 使 JSP 作者可以专注于特定于应用程序的开发需求，而不是为这些通用操作"另起炉灶"。

当然，您可以使用 JSP 脚本编制元素 (scriptlet、表达式和声明) 来实现此类任务。例如，可以使用三个 scriptlet 实现条件内容，清单 1 中着重显示了这三个 scriptlet。但是，因为脚本编制元素依赖于在页面中嵌入程序源代码 (通常是 Java 代码) ，所以对于使用这些脚本编制元素的 JSP 页面，其软件维护任务的复杂度大大增加了。例如，清单 1 中的 scriptlet 示例严格地依赖于花括号的正确匹配。如果不经意间引入了一个语法错误，则条件内容中的嵌套其它 scriptlet 可能会造成严重破坏，并且在 JSP 容器编译该页面时，要使所产生的错误信息有意义可能会很困难。

JSTL 1.0 which is designed for JSP 1.2 has the class `ELException` included in JSTL JAR file. JSTL 1.1 which is designed for JSP 2.0 doesn't have it included anymore since that's together with several EL specific classes moved to JSP 2.0 API (which is provided by the servletcontainer itself).

When you run JSTL 1.1 on a JSP 1.2 container, it'll complain that `ELException` is missing because it's not available by JSP 1.2.

jstl 1.2: <%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>


    <%@ taglib uri="http://java.sun.com/jstl/core" prefix="c" %>

This URI is from the old and EOL'ed JSTL 1.0 library. Since JSTL 1.1, you need an extra `/jsp` in the path because the taglib's internal workings were changed because the EL part was moved from JSTL to JSP:

    <%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>

Further, the JAR files which you attempted to drop in `/WEB-INF/lib` are wrong. The `javax.servlet.jsp.jstl-api-1.2.1-javadoc.jar` is contains only the JSTL javadocs and the `javaee.jar` contains the entire Java EE API which may be desastreus because Tomcat ships with parts of it already (JSP/Servlet) which may [conflict][1].


http://stackoverflow.com/questions/4199596/java-lang-noclassdeffounderror-javax-servlet-jsp-el-elexception

http://blog.csdn.net/for_china2012/article/details/9307471


http://stackoverflow.com/questions/9976281/the-absolute-uri-http-java-sun-com-jstl-core-cannot-be-resolved-in-either-web

 [1]: http://stackoverflow.com/questions/4076601/how-do-i-import-the-javax-servlet-api-in-my-eclipse-project/4076706#4076706