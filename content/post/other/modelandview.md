---
title: ModelAndView
author: "-"
date: 2014-01-09T03:01:03+00:00
url: /?p=6181
categories:
  - Inbox
tags:
  - Java
  - Spring
  - SpringMVC

---
## ModelAndView
http://itroop.iteye.com/blog/263845

的构造方法有7个。但是它们都是相通的。这里使用无参构造函数来举例说明如何构造ModelAndView

实例。
  
ModelAndView类别就如其名称所示,是代表了MVC Web程序中Model与View的对象,不过它只是方便您一次返回这两个对象的holder,Model与View两者仍是分离的概念。
  
最简单的ModelAndView是持有View的名称返回,之后View名称被view resolver,也就是实作org.springframework.web.servlet.View接口的实例解析,例如 InternalResourceView或JstlView等等: 

ModelAndView(String viewName)
  
如果您要返回Model对象,则可以使用Map来收集这些Model对象,然后设定给ModelAndView,使用下面这个版本的ModelAndView: 

ModelAndView(String viewName, Map model)
  
Map对象中设定好key与value值,之后可以在视图中取出,如果您只是要返回一个Model对象,则可以使用下面这个ModelAndView版本: 

ModelAndView(String viewName, String modelName, Object modelObject)
  
藉由modelName,您可以在视图中取出Model并显示。
  
ModelAndView类别提供实作View接口的对象来作View的参数: 

ModelAndView(View view)

ModelAndView(View view, Map model)

ModelAndView(View view, String modelName, Object modelObject)
  
一个例子是org.springframework.web.servlet.view.RedirectView,ModelAndView预设是使 用forward来转发请求结果至视图,使用RedirectView的话,则会使用redirect将请求重导至视图,例如: 

…

public ModelAndView handleRequest(....) … {

....

return new ModelAndView(new RedirectView(this.getViewPage()));

}

....
  
在这边,viewPage的地址是从服务器网页根目录开始指定,而不是Web应用程序的根目录,所以您的getViewPage()传回的地址必须像是 /springapp/pages/index.htm这样的地址,其中springapp是您的Web应用程序目录。
  
使用forward的话,网址列上并不会出现被转发的目标地址,而且forward是在Web应用程序之内进行,可以访问Web应用程序的隐藏目录,像是WEB-INF,然而forward只能在Web应用程序中进行,不能指定至其它的Web应用程序地址。
  
使用redirect的话,是要求客户端浏览器重新发出一个指定的请求地址,因此网址列上会出现被重导的目录地址,重导的请求是由浏览器发出,所以不能 访问Web应用程序中的隐藏目录,像是WEB-INF,然而重导是重新要求一个网页,所以可以指定至其它的Web应用程序地址。
  
DispatcherServlet会根据传回的ModelAndView来解析View名称,并处理给予的Model。View名称的解析是委托给实 作org.springframework.web.servlet.ViewResolver接口的实例,ViewResolver接口定义如下: 

public interface ViewResolver {

public view resolveViewName(String, Locale locale) throws ServletException;

}
  
ViewResolver的一个实例是InternalResourceViewResolver,名称解析完之后,实际的View绘制与Model转 换处理是交给实作org.springframework.web.servlet.View的实例,View接口如下: 

public interface View {

public void render(Map model, HttpServletResquest resquest, HttpServletResponse response) throws ServletException, IOException;

}
  
View的实作之前用过org.springframework.web.servlet.view.InternalResourceView,另外也还有JstlView、TilesView、VelocityView等等的实作,分别进行不同的表现展处理 。

ModelAndView()

这个构造方法构造出来的ModelAndView

不能直接使用,应为它没有指定view,也没有绑定对应的model对象。当然,model对象不是必须的,但是view确实必须的。

用这个构造方法构造的实例主要用来在以后往其中加view设置和model对象。

给ModelAndView

实例设置view的方法有两

个: setViewName(String viewName) 和 setView(View view)。前者是使用view

name,后者是使用预先构造好的View对象。其中前者比较常用。事实上View是一个接口,而不是一个可以构造的具体类,我们只能通过其他途径来获取

View的实例。对于view

name,它既可以是jsp的名字,也可以是tiles定义的名字,取决于使用的ViewNameResolver如何理解这个view name。

如何获取View的实例以后再研究。

而对应如何给ModelAndView

实例设置model则比较复杂。有三个方法可以使用: 

addObject(Object modelObject)

addObject(String modelName, Object modelObject)

addAllObjects(Map modelMap)

ModelAndView

可以接收Object类型的对象,ModelAndView

将它视为其众多model中的一个。当使用Object类型的对象的时候,必须指定一个名字。ModelAndView

也可以接收没有明显名字的对象,原因在于ModelAndView

将调用spring自己定义的Conventions 类的.getVariableName()方法来为这个model生成一个名字。显然,对model而言,名字是必须的。

Conventions.getVariableName()生成名字的规则是使用对象的类名的小写模式来作model名字。当这个model是集合或数组的时候,使用集合的第一个元素的类名加s来作model的名字。

ModelAndView

也可以接收Map类型的对象,ModelAndView

将这个Map中的元素视为model,而不是把这个Map本身视为model。但是其他的集合类可以用本身作为model对象。

实际上,ModelAndView

对model的支持来自于类ModelMap,这个类继承自HashMap。

完整的例子
  
    
      Java代码
  
  
  
    
      public ModelAndView handleRequestInternal(
    
    
              HttpServletRequest request,
    
    
              HttpServletResponse response) throws Exception {
    
    
    
    
    
    
      ModelAndView mav = new ModelAndView("hello");//实例化一个VIew的ModelAndView实例
    
    
    
    
      mav.addObject("message", "Hello World!");//添加一个带名的model对象
    
    
    
    
    
    
              return mav;
    
    
    
    
    
    
      }
    
    
      
    
  
