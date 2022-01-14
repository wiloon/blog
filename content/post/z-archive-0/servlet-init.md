---
title: servlet init()
author: "-"
date: 2011-10-30T08:47:06+00:00
url: /?p=1401
categories:
  - Java
tags:
  - Servlet

---
## servlet init()
init方法是在Servlet实例化之后执行的，并且只执行一次。
  
一.先说init(ServletConfig)中参数ServletConfig，代表的是配置信息。即在web.xml中配置的信息，比如: 
  
```xml
  
<servlet>
    
<servlet-name>myfirstservlet</servlet-name>
    
<servlet-class>as</servlet-class>
    
<init-param>
      
<param-name>name</param-name>
      
<param-value>小明</param-value>
    
</init-param>
    
<init-param>
      
<param-name>age</param-name>
      
<param-value>25</param-value>
    
</init-param>
  
</servlet>
  
```
     
在程序中可以用this.getServletConfig()方法得到ServletConfig的实例，然后用ServletConfig的相应方法 可以得到ServletConfig的名字(getServletName)和配置参数的名字(getInitParameter("name"))或者 名字枚举(getInitParameterNames())，并且通过参数名字得到相应的参数值。具体方法参见API。

二.再说说init方法，从源码中我们不难发现: Servlet接口里面只有init(ServletConfig)，这是供tomcat调用的。GenericServlet类里面有成员变量ServletConfig，init(ServletConfig)方法和init()方法: 
  
```java
  
private transient ServletConfig config;
  
public void init(ServletConfig config) throws ServletException{
   
this.config=config;
   
this.init();
   
}

public void init() throws ServletException{
  
}
  
```
  
现在一切都很明了了，当容器(tomcat)帮忙调用init(ServletConfig config)并且给传过来一个参数config，这个方法把参数对象的引用指向类的成员变量this.config，并且调用类的 this.init()方法。有人问了，我们在写Servlet类时只要重写init(ServletConfig config)就可以了，init()不就成了多余的了吗？实际上init()方法是为了防止程序员在写Servlet类重写 init(ServletConfig config)时忘记写super.init(ServletConfig config),这样就容易造成出现空指针异常。而这就要求我们最好不要重写init(ServletConfig config)，而要重写init()方法，就可以不写super。Servlet，你真是绕死人不偿命！