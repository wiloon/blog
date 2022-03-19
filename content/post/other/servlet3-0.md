---
title: servlet3.0
author: "-"
date: 2012-06-10T08:44:52+00:00
url: /?p=3491
categories:
  - Java
  - Web
tags:
  - Servlet

---
## servlet3.0
http://www.ibm.com/developerworks/cn/java/j-lo-servlet30/

Servlet 3.0 作为 Java EE 6 规范体系中一员，随着 Java EE 6 规范一起发布。该版本在前一版本 (Servlet 2.5) 的基础上提供了若干新特性用于简化 Web 应用的开发和部署。其中有几项特性的引入让开发者感到非常兴奋，同时也获得了 Java 社区的一片赞誉之声: 


  
    异步处理支持: 有了该特性，Servlet 线程不再需要一直阻塞，直到业务处理完毕才能再输出响应，最后才结束该 Servlet 线程。在接收到请求之后，Servlet 线程可以将耗时的操作委派给另一个线程来完成，自己在不生成响应的情况下返回至容器。针对业务处理较耗时的情况，这将大大减少服务器资源的占用，并且提高并发处理速度。
  
  
    新增的注解支持: 该版本新增了若干注解，用于简化 Servlet、过滤器 (Filter) 和监听器 (Listener) 的声明，这使得 web.xml 部署描述文件从该版本开始不再是必选的了。
  
  
    可插性支持: 熟悉 Struts2 的开发者一定会对其通过插件的方式与包括 Spring 在内的各种常用框架的整合特性记忆犹新。将相应的插件封装成 JAR 包并放在类路径下，Struts2 运行时便能自动加载这些插件。现在 Servlet 3.0 提供了类似的特性，开发者可以通过插件的方式很方便的扩充已有 Web 应用的功能，而不需要修改原有的应用。
  


## 新增的注解支持 {#major3}

Servlet 3.0 的部署描述文件 web.xml 的顶层标签 <web-app> 有一个 metadata-complete 属性，该属性指定当前的部署描述文件是否是完全的。如果设置为 true，则容器在部署时将只依赖部署描述文件，忽略所有的注解 (同时也会跳过 web-fragment.xml 的扫描，亦即禁用可插性支持，具体请看后文关于 可插性支持的讲解) ；如果不配置该属性，或者将其设置为 false，则表示启用注解支持 (和可插性支持) 。

### @WebServlet {#minor3.1}

@WebServlet 用于将一个类声明为 Servlet，该注解将会在部署时被容器处理，容器将根据具体的属性配置将相应的类部署为 Servlet。该注解具有下表给出的一些常用属性 (以下所有属性均为可选属性，但是 vlaue 或者 urlPatterns 通常是必需的，且二者不能共存，如果同时指定，通常是忽略 value 的取值) : 

##### 表 1. @WebServlet 主要属性列表 {#N1008E}


  
    <th>
      属性名
    </th>
    
    <th>
      类型
    </th>
    
    <th>
      描述
    </th>
  
  
  
    
      name
    
    
    
      String
    
    
    
      指定 Servlet 的 name 属性，等价于 <servlet-name>。如果没有显式指定，则该 Servlet 的取值即为类的全限定名。
    
  
  
  
    
      value
    
    
    
      String[]
    
    
    
      该属性等价于 urlPatterns 属性。两个属性不能同时使用。
    
  
  
  
    
      urlPatterns
    
    
    
      String[]
    
    
    
      指定一组 Servlet 的 URL 匹配模式。等价于 <url-pattern> 标签。
    
  
  
  
    
      loadOnStartup
    
    
    
      int
    
    
    
      指定 Servlet 的加载顺序，等价于 <load-on-startup> 标签。http://blog.csdn.net/enjoyo/article/details/1761033
    
  
  
  
    
      initParams
    
    
    
      WebInitParam[]
    
    
    
      指定一组 Servlet 初始化参数，等价于 <init-param> 标签。http://www.wiloon.com/?p=6138
    
  
  
  
    
      asyncSupported
    
    
    
      boolean
    
    
    
      声明 Servlet 是否支持异步操作模式，等价于  标签。
    
  
  
  
    
      description
    
    
    
      String
    
    
    
      该 Servlet 的描述信息，等价于 <description> 标签。
    
  
  
  
    
      displayName
    
    
    
      String
    
    
    
      该 Servlet 的显示名，通常配合工具使用，等价于 <display-name> 标签。
    
  


下面是一个简单的示例: 

```java
  
@WebServlet(urlPatterns = {"/simple"},
  
asyncSupported = true,
  
loadOnStartup = -1,
  
name = "SimpleServlet",
  
displayName = "ss",
  
initParams = {@WebInitParam(name = "username", value = "tom")}
  
public class SimpleServlet extends HttpServlet{ … }
  
)
  
```
  
  
  
    @WebInitParam
  
  
    该注解通常不单独使用，而是配合 @WebServlet 或者 @WebFilter 使用。它的作用是为 Servlet 或者过滤器指定初始化参数，这等价于 web.xml 中 <servlet> 和 <filter> 的 <init-param> 子标签。@WebInitParam 具有下表给出的一些常用属性: 
  
  
    表 2. @WebInitParam 的常用属性
  
  
  
    
      <th>
        属性名
      </th>
      
      <th>
        类型
      </th>
      
      <th>
        是否可选
      </th>
      
      <th>
        描述
      </th>
    
    
    
      
        name
      
      
      
        String
      
      
      
        否
      
      
      
        指定参数的名字，等价于 <param-name>。
      
    
    
    
      
        value
      
      
      
        String
      
      
      
        否
      
      
      
        指定参数的值，等价于 <param-value>。
      
    
    
    
      
        description
      
      
      
        String
      
      
      
        是
      
      
      
        关于参数的描述，等价于 <description>。
      
    
  
  
  
  
  
    @WebFilter
  
  
    @WebFilter 用于将一个类声明为过滤器，该注解将会在部署时被容器处理，容器将根据具体的属性配置将相应的类部署为过滤器。该注解具有下表给出的一些常用属性 ( 以下所有属性均为可选属性，但是 value、urlPatterns、servletNames 三者必需至少包含一个，且 value 和 urlPatterns 不能共存，如果同时指定，通常忽略 value 的取值 ): 
  
  
    表 3. @WebFilter 的常用属性
  
  
  
    
      <th>
        属性名
      </th>
      
      <th>
        类型
      </th>
      
      <th>
        描述
      </th>
    
    
    
      
        filterName
      
      
      
        String
      
      
      
        指定过滤器的 name 属性，等价于 <filter-name>
      
    
    
    
      
        value
      
      
      
        String[]
      
      
      
        该属性等价于 urlPatterns 属性。但是两者不应该同时使用。
      
    
    
    
      
        urlPatterns
      
      
      
        String[]
      
      
      
        指定一组过滤器的 URL 匹配模式。等价于 <url-pattern> 标签。
      
    
    
    
      
        servletNames
      
      
      
        String[]
      
      
      
        指定过滤器将应用于哪些 Servlet。取值是 @WebServlet 中的 name 属性的取值，或者是 web.xml 中 <servlet-name> 的取值。
      
    
    
    
      
        dispatcherTypes
      
      
      
        DispatcherType
      
      
      
        指定过滤器的转发模式。具体取值包括: 
 ASYNC、ERROR、FORWARD、INCLUDE、REQUEST。
      
    
    
    
      
        initParams
      
      
      
        WebInitParam[]
      
      
      
        指定一组过滤器初始化参数，等价于 <init-param> 标签。
      
    
    
    
      
        asyncSupported
      
      
      
        boolean
      
      
      
        声明过滤器是否支持异步操作模式，等价于  标签。
      
    
    
    
      
        description
      
      
      
        String
      
      
      
        该过滤器的描述信息，等价于 <description> 标签。
      
    
    
    
      
        displayName
      
      
      
        String
      
      
      
        该过滤器的显示名，通常配合工具使用，等价于 <display-name> 标签。
      
    
  
  
    下面是一个简单的示例: 
  
  
    @WebFilter(servletNames = {"SimpleServlet"},filterName="SimpleFilter") 
public class LessThanSixFilter implements Filter{...}
  
  
    如此配置之后，就可以不必在 web.xml 中配置相应的 <filter> 和 <filter-mapping> 元素了，容器会在部署时根据指定的属性将该类发布为过滤器。它等价的 web.xml 中的配置形式为: 
  
  
    <filter> 
    <filter-name>SimpleFilter</filter-name> 
    <filter-class>xxx</filter-class> 
</filter> 
<filter-mapping> 
    <filter-name>SimpleFilter</filter-name> 
    <servlet-name>SimpleServlet</servlet-name> 
</filter-mapping>


    
    
      @WebListener
    
    
    
      该注解用于将类声明为监听器，被 @WebListener 标注的类必须实现以下至少一个接口: 
    
    
    
      
        ServletContextListener
      
      
        ServletContextAttributeListener
      
      
        ServletRequestListener
      
      
        ServletRequestAttributeListener
      
      
        HttpSessionListener
      
      
        HttpSessionAttributeListener
      
    
    
    
      该注解使用非常简单，其属性如下: 
    
    
    
      表 4. @WebListener 的常用属性
    
    
    
      
        <th>
          属性名
        </th>
        
        <th>
          类型
        </th>
        
        <th>
          是否可选
        </th>
        
        <th>
          描述
        </th>
      
      
      
        
          value
        
        
        
          String
        
        
        
          是
        
        
        
          该监听器的描述信息。
        
      
    
    
    
      一个简单示例如下: 
    
    
    
      @WebListener("This is only a demo listener") 
public class SimpleListener implements ServletContextListener{...}
    
    
    
      如此，则不需要在 web.xml 中配置  标签了。它等价的 web.xml 中的配置形式如下: 
    
    
    
       
    footmark.servlet.SimpleListener</listener-class> 
</listener>
  
