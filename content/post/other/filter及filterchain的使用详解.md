---
title: Filter FilterChain
author: "-"
date: 2012-11-18T05:17:32+00:00
url: /?p=4712
categories:
  - Java
  - Web
tags:$
  - reprint
---
## Filter FilterChain
**<http://blog.csdn.net/zhaozheng7758/article/details/6105749>**

**一、****Filter****的介绍及使用******

什么是过滤器？

与Servlet相似，过滤器是一些web应用程序组件，可以绑定到一个web应用程序中。但是与其他web应用程序组件不同的是，过滤器是"链"在容器的处理过程中的。这就意味着它们会在servlet处理器之前访问一个进入的请求，并且在外发响应信息返回到客户前访问这些响应信息。这种访问使得过滤器可以检查并修改请求和响应的内容。

过滤器适用于那些地方？

l  为一个web应用程序的新功能建立模型(可被添加到web应用程序中或者从web应用程序中删除而不需要重写基层应用程序代码)；

l  向过去的代码添加新功能。

过滤器放在容器结构的什么位置？

过滤器放在web资源之前，可以在请求抵达它所应用的web资源(可以是一个Servlet、一个Jsp页面，甚至是一个HTML页面)之前截获进入的请求，并且在它返回到客户之前截获输出请求。Filter: 用来拦截请求，处于客户端与被请求资源之间，目的是重用代码。Filter链，在web.xml中哪个先配置，哪个就先调用。在filter中也可以配置一些初始化参数。

Java中的Filter 并不是一个标准的Servlet ，它不能处理用户请求，也不能对客户端生成响应。 主要用于对HttpServletRequest 进行预处理，也可以对HttpServletResponse 进行后处理，是个典型的处理链。

Filter 有如下几个用处: 

l  在HttpServletRequest 到达Servlet 之前，拦截客户的HttpServletRequest 。

l  根据需要检查HttpServletRequest ，也可以修改HttpServletRequest 头和数据。

l  在HttpServletResponse 到达客户端之前，拦截HttpServletResponse 。

l  根据需要检查HttpServletResponse ，可以修改HttpServletResponse 头和数据。

Filter 有如下几个种类: 

l  用户授权的Filter: Filter 负责检查用户请求，根据请求过滤用户非法请求。

l  日志Filter: 详细记录某些特殊的用户请求。

l  负责解码的Filter: 包括对非标准编码的请求解码。

l  能改变XML 内容的XSLTFilter 等。

一个Filter 可负责拦截多个请求或响应:一个请求或响应也可被多个请求拦截。

创建一个Filter 只需两个步骤:
  
(1)创建Filter 处理类:

(2)在web.xml 文件中配置Filter 。
  
创建Filter 必须实现javax.servlet.Filter 接口，在该接口中定义了三个方法。
  
• void init(FilterConfig config): 用于完成Filter 的初始化。
  
• void destroy(): 用于Filter 销毁前，完成某些资源的回收。
  
• void doFilter(ServletRequest request, ServletResponse response,FilterChain chain): 实现过滤功能，该方法就是对每个请求及响应增加的额外处理。

过滤器Filter也具有生命周期: init()->doFilter()->destroy()，由部署文件中的filter元素驱动。在servlet2.4中，过滤器同样可以用于请求分派器，但须在web.xml中声明，<dispatcher>INCLUDE或FORWARD或REQUEST或ERROR</dispatcher>该元素位于filter-mapping中。

Filter常用的场景: 

例一、  日志的记录，当有请求到达时，在该过滤器中进行日志的记录。处理完成后，进入后续的Filter或者处理。

步骤1: 编写Filter类

**package** test.filter;

**import** javax.servlet.Filter;

**import** javax.servlet.FilterChain;

**import** javax.servlet.FilterConfig;

**import** javax.servlet.ServletContext;

**import** javax.servlet.ServletRequest;

**import** javax.servlet.ServletResponse;

**import** javax.servlet.http.HttpServletRequest;

**public** **class** LogFilter **implements** Filter {

**private** FilterConfig config;

// 实现初始化方法

**public** **void** init(FilterConfig config) {

**this**.config = config;

}

// 实现销毁方法

**public** **void** destroy() {

**this**.config = **null**;

}

**public** **void** doFilter(ServletRequest request, ServletResponse response,

FilterChain chain) {

// 获取ServletContext 对象，用于记录日志

ServletContext context = **this**.config.getServletContext();

**long** before = System._currentTimeMillis_();

System._out_.println("开始过滤... ");

// 将请求转换成HttpServletRequest 请求

HttpServletRequest hrequest = (HttpServletRequest) request;

// 记录日志

context.log("Filter已经截获到用户的请求的地址: " + hrequest.getServletPath());

**try** {

// Filter 只是链式处理，请求依然转发到目的地址。

chain.doFilter(request, response);

} **catch** (Exception e) {

e.printStackTrace();

}

**long** after = System._currentTimeMillis_();

// 记录日志

context.log("过滤结束");

// 再次记录日志

context.log(" 请求被定位到" + ((HttpServletRequest) request).getRequestURI()

+ "所花的时间为: " + (after - before));

}

}

在上面的请求Filter中，仅在日志中记录请求的URL，对所有的请求都执行chain.doFilter(request，reponse)方法，当Filter 对请求过滤后，依然将请求发送到目的地址。

步骤2: 在web.xml中配置Filter

<!- 定义Filter ->

<filter>

<!- Filter 的名字 ->

<filter-name>log</filter-name>

<!- Filter 的实现类 ->

<filter-class> test.filter.LogFilter</filter-class>

</filter>

<!- 定义Filter 拦截地址 ->

<filter-mapping>

<!- Filter 的名字 ->

<filter-name>log</filter-name>

<!- Filter 负责拦截的URL ->

<url-pattern>/filter/*</url-pattern>

</filter-mapping>

通过上述步骤的操作，此时就可以通过URI进行访问。具体访问后会在log文件中的localhost文件中产生具体的访问日志。如下所示: 

2010-12-28 21:12:50 org.apache.catalina.core.ApplicationContext log

信息:  请求被定位到/examples/jsp/jsp2/el/basic-arithmetic.jsp所花的时间为: 0

2010-12-28 21:14:55 org.apache.catalina.core.ApplicationContext log

信息: Filter已经截获到用户的请求的地址: /jsp/jsp2/el/basic-comparisons.jsp

2010-12-28 21:14:56 org.apache.catalina.core.ApplicationContext log

信息: 过滤结束

例二、      进行编码的修正，当有新的请求时，需要将用户传送过来的字符进行重新编码，以使其可以满足服务器的编码格式。

1.    编写EncodingFilter类


  package test.filter;


  import java.io.IOException;


  import javax.servlet.Filter;


  import javax.servlet.FilterChain;


  import javax.servlet.FilterConfig;


  import javax.servlet.ServletContext;


  import javax.servlet.ServletException;


  import javax.servlet.ServletRequest;


  import javax.servlet.ServletResponse;


  public class EncodingFilter implements Filter {


      private FilterConfig filterConfig = null;


      private String encoding = null;


      //实现销毁方法


      public void destroy() {


           encoding = null;


       }


      //进行具体的过滤


      public void doFilter(ServletRequest request, ServletResponse response,


               FilterChain chain) throws IOException, ServletException {


          // 获取ServletContext 对象，用于记录日志


           ServletContext context =this.filterConfig.getServletContext();


           context.log("开始设置编码格式");


           String encoding = getEncoding();


           if (encoding == null){


               encoding = "gb2312";


           }


           // 在请求里设置上指定的编码


           request.setCharacterEncoding(encoding);


           chain.doFilter(request, response);


           context.log("成功设置了编码格式");


       }


      //初始化配置


      public void init(FilterConfig filterConfig) throwsServletException {


          this.filterConfig = filterConfig;


          this.encoding = filterConfig.getInitParameter("encoding");


       }


      private String getEncoding() {


          return this.encoding;


       }

}

步骤2: 在web.xml中配置Filter

<!- 定义Filter ->

<filter>

<!- Filter 的名字 ->

<filter-name>encoding</filter-name>

<!- Filter 的实现类 ->

<filter-class> test.filter.EncodingFilter</filter-class>

<init-param>

<param-name>encoding</param-name>

<param-value>gb2312</param-value>

</init-param>

</filter>

<!- 定义Filter 拦截地址 ->

<filter-mapping>

<!- Filter 的名字 ->

<filter-name> encoding </filter-name>

<!- Filter 负责拦截的URL ->

<url-pattern>/encode/*</url-pattern>

</filter-mapping>

通过上述步骤的操作，此时就可以通过URI进行访问。

例三、用户权限的认证，当用户发送请求时，可以对用户的身份信息进行验证，如果能够通过验证则接下来再进行其它操作，否则直接不进入下一步的处理。

1.    编写身份认证SecurityFilter类


  package test.filter;


  import java.io.IOException;


  import javax.servlet.Filter;


  import javax.servlet.FilterChain;


  import javax.servlet.FilterConfig;


  import javax.servlet.ServletContext;


  import javax.servlet.ServletException;


  import javax.servlet.ServletRequest;


  import javax.servlet.ServletResponse;


  import javax.servlet.http.HttpServletRequest;


  import javax.servlet.http.HttpServletResponse;


  import javax.servlet.http.HttpSession;


  public class SecurityFilter implements Filter {


      private FilterConfig filterConfig;


      //初始化方法实现


      @Override


      public void init(FilterConfig filterConfig) throwsServletException {


          this.filterConfig = filterConfig;


      }


      //身份认证的过滤


      @Override


      public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)


              throws IOException, ServletException {


          ServletContext context =this.filterConfig.getServletContext();


          HttpServletRequest req = (HttpServletRequest) request;


          HttpServletResponse res = (HttpServletResponse) response;


          HttpSession session = req.getSession();


          //登录后才能进入下一步处理，否则直接进入错误提示页面


          if (session.getAttribute("username") != null) {


              context.log("身份认证通过，进入下一步处理 ");


              chain.doFilter(request, response);


          } else {


              context.log("身份认证失败，直接返回");


              res.sendRedirect("../failure.jsp");


          }


      }


      //实现销毁方法


      @Override


      public void destroy() {


          this.filterConfig = null;


      }

}

步骤2: 在web.xml中配置Filter

<!- 定义Filter ->

<filter>

<!- Filter 的名字 ->

<filter-name>security</filter-name>

<!- Filter 的实现类 ->

<filter-class> test.filter.SecurityFilter</filter-class>

</filter>

<!- 定义Filter 拦截地址 ->

<filter-mapping>

<!- Filter 的名字 ->

<filter-name> security </filter-name>

<!- Filter 负责拦截的URL ->

<url-pattern>/security/*</url-pattern>

</filter-mapping>

通过上述步骤的操作，此时就可以通过URI进行访问。此时如果能够取得Session中的username值时，会直接进入下一步处理，否则直接进入错误页面。


  二、过滤链FilterChain


  两个过滤器，EncodingFilter负责设置编码，SecurityFilter负责控制权限，服务器会按照web.xml中过滤器定义的先后循序组装成一条链，然后一次执行其中的doFilter()方法。执行的顺序就如下图所示，执行第一个过滤器的chain.doFilter()之前的代码，第二个过滤器的chain.doFilter()之前的代码，请求的资源，第二个过滤器的chain.doFilter()之后的代码，第一个过滤器的chain.doFilter()之后的代码，最后返回响应。


  执行的代码顺序是: 


  l  执行EncodingFilter.doFilter()中chain.doFilter()之前的部分；request.setCharacterEncoding(encoding);


  l  执行SecurityFilter.doFilter()中chain.doFilter()之前的部分: 判断用户是否已登录。


  l  如果用户已登录，则访问请求的资源。


  l  如果用户未登录，则页面重定向到: /failure.jsp。


  l  执行SecurityFilter.doFilter()中chain.doFilter()之后的部分: 这里没有代码。


  l  执行EncodingFilter.doFilter()中chain.doFilter()之后的部分: 写入已经完成的日志。


  过滤链的好处是，执行过程中任何时候都可以打断，只要不执行chain.doFilter()就不会再执行后面的过滤器和请求的内容。而在实际使用时，就要特别注意过滤链的执行顺序问题，像EncodingFilter就一定要放在所有Filter之前，这样才能确保在使用请求中的数据前设置正确的编码。
