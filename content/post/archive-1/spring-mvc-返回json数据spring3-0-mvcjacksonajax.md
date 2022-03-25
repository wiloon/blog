---
title: spring MVC 返回JSON数据(Spring3.0 MVC+Jackson+AJAX)
author: "-"
date: 2014-02-21T08:28:19+00:00
url: /?p=6274
categories:
  - Uncategorized
tags:
  - JavaScript
  - Json
  - Spring

---
## spring MVC 返回JSON数据(Spring3.0 MVC+Jackson+AJAX)
本文本的框架为:SpringMVC 3.2.3 \ jackson 1.9.2

传统的返回JSON格式的AJAX,用的方法一般是: 在后台先把数据(Object)封装成JSON数据,再用HttpServletResponse返回。

本示例中,SpringMVC可直接支持JSON格式数据的返回。具体如下。

**1、JAR包: SPRINGMVC包需的包,另外还需JACKSON的两个包。**
  
jackson-core-asl-1.9.2.jar
  
jackson-mapper-asl-1.9.2.jar

**2、spring-servlet.xml中加入: **


  
    
      Java代码  <img alt="收藏代码" src="http://angelbill3.iteye.com/images/icon_star.png" />
  
  
  
    
      <!- 返回JSON模版 ->
    
    
      <bean class="org.springframework.web.servlet.mvc.annotation.AnnotationMethodHandlerAdapter" >
    
    
          <property name="messageConverters">
    
    
          
    
    
               <bean class="org.springframework.http.converter.json.MappingJacksonHttpMessageConverter" />
    
    
          </list>
    
    
          </property>
    
    
      </bean>
    
  

我们在SPRING的配置中加入了一个新的适配器: AnnotationMethodHandlerAdapter,通过这个适配器,我们配置了一个属性,messageConverters,其中mappingJacksonHttpMessageConverter这个Bean,它就是用来处理json数据转换的。
  
注: 我的项目中没有乱码现象,这样配即可,若有乱码现象,可以在MappingJacksonHttpMessageConverter的BEAN中配置supportedMediaTypes属性,是用于解决返回的乱码问题。

**3、Controller中的使用**


  
    
      Java代码  <img alt="收藏代码" src="http://angelbill3.iteye.com/images/icon_star.png" />
  
  
  
    
      @Controller
    
    
      public class SelectController {
    
    
          @Resource
    
    
          private TypeService typeService;
    
    
    
    
          @RequestMapping("/type")
    
    
          @ResponseBody
    
    
          public Object type(){
    
    
              List<Type> typelist = this.typeService.getTypeByParentid(Const.TYPE_DAILY);
    
    
              return typelist;
    
    
          }
    
    
      }
    
  

在SpringMVC中可以在Controller的某个方法上加**@ResponseBody**注解,表示该方法的返回结果直接写入HTTP response body中。

--------------
  
**遇到的问题: **

用上面的controller,访问: http://localhost:8080/demo/type.htm,报406错如下: 
  
**Failed to load resource: the server responded with a status of 406 (Not Acceptable) :  The resource identified by this request is only capable of generating responses with characteristics not acceptable according to the request "accept" headers () **

查资料表明,不是JAR的版本问题,网友解答描述: 

1. spring 3.2时requestedMediaTypes却为[text language="/html"][/text]的情况报406错误,还有一个原因可能是由于采用的后缀有关,如果使用\*.htm,\*.html等,默认就会采用[text language="/html"][/text]编码,若改成\*.json,\*.shtml等就OK

2. 3.2.4 也遇到这个问题。修改ajax 请求的后缀为json 或者其他就可以了。他还是会优先根据url请求的后缀决定请求类型。所以你看到的一直是[text language="/html"][/text]

**所以,将访问路径从http://localhost:8080/demo/type.htm改为http://localhost:8080/demo/type.json即可。
  
 (如果你只拦截htm开头的链接,可以在web.xml里新增一个url-pattern为*.json的servlet即可。) **

--------------
  
参考: http://digdata.me/archives/96/

http://angelbill3.iteye.com/blog/1985075