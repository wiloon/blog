---
title: Spring中bean的作用域
author: "-"
date: 2012-09-16T03:38:52+00:00
url: /?p=4043
categories:
  - Development
  - Java
tags:$
  - reprint
---
## Spring中bean的作用域
[http://blog.csdn.net/ProvidenceZY/article/details/1878582 ][1]


  
    如何使用spring的作用域: 
  
  
    <bean id="role" class="spring.chapter2.maryGame.Role" scope="singleton"/>
  
  
    这里的scope就是用来配置spring bean的作用域，它标识bean的作用域。
  
  
    在spring2.0之前bean只有2种作用域即: singleton(单例)、non-singleton (也称prototype) , Spring2.0以后，增加了session、request、global session三种专用于Web应用程序上下文的Bean。因此，默认情况下Spring2.0现在有五种类型的Bean。当然，Spring2.0对Bean的类型的设计进行了重构，并设计出灵活的Bean类型支持，理论上可以有无数多种类型的Bean，用户可以根据自己的需要，增加新的Bean类型，满足实际应用需求。
  
  
    1、singleton作用域
  
  
    当一个bean的作用域设置为singleton, 那么Spring IOC容器中只会存在一个共享的bean实例，并且所有对bean的请求，只要id与该bean定义相匹配，则只会返回bean的同一实例。换言之，当把一个bean定义设置为singleton作用域时，Spring IOC容器只会创建该bean定义的唯一实例。这个单一实例会被存储到单例缓存 (singleton cache) 中，并且所有针对该bean的后续请求和引用都将返回被缓存的对象实例，这里要注意的是singleton作用域和GOF设计模式中的单例是完全不同的，单例设计模式表示一个ClassLoader中只有一个class存在，而这里的singleton则表示一个容器对应一个bean，也就是说当一个bean被标识为singleton时候，spring的IOC容器中只会存在一个该bean。
  
  
    配置实例: 
  
  
    <bean id="role" class="spring.chapter2.maryGame.Role" scope="singleton"/>
  
  
    或者
  
  
    <bean id="role" class="spring.chapter2.maryGame.Role" singleton="true"/>
  
  
    2、prototype
  
  
     prototype作用域部署的bean，每一次请求 (将其注入到另一个bean中，或者以程序的方式调用容器的getBean()方法) 都会产生一个新的bean实例，相当与一个new的操作，对于prototype作用域的bean，有一点非常重要，那就是Spring不能对一个prototype bean的整个生命周期负责，容器在初始化、配置、装饰或者是装配完一个prototype实例后，将它交给客户端，随后就对该prototype实例不闻不问了。不管何种作用域，容器都会调用所有对象的初始化生命周期回调方法，而对prototype而言，任何配置好的析构生命周期回调方法都将不会被调用。清除prototype作用域的对象并释放任何prototype bean所持有的昂贵资源，都是客户端代码的职责。 (让Spring容器释放被singleton作用域bean占用资源的一种可行方式是，通过使用bean的后置处理器，该处理器持有要被清除的bean的引用。) 
  
  
    配置实例: 
  
  
    <bean id="role" class="spring.chapter2.maryGame.Role" scope="prototype"/>
  
  
    或者
  
  
    <beanid="role" class="spring.chapter2.maryGame.Role" singleton="false"/>
  
  
  
  
    3、request
  
  
    request表示该针对每一次HTTP请求都会产生一个新的bean，同时该bean仅在当前HTTP request内有效，配置实例: 
  
  
    request、session、global session使用的时候首先要在初始化web的web.xml中做如下配置: 
  
  
    如果你使用的是Servlet 2.4及以上的web容器，那么你仅需要在web应用的XML声明文件web.xml中增加下述ContextListener即可:  
    
    
      <web-app>
  ...
  
 <img src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/None.gif" alt="" align="top" />org.springframework.web.context.request.RequestContextListener</listener-class>
  </listener>
  ...
 <img src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/None.gif" alt="" align="top" /></web-app>
 <img src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/None.gif" alt="" align="top" />
    
    
    
      ，如果是Servlet2.4以前的web容器,那么你要使用一个javax.servlet.Filter的实现: 
  
  
    
      <img src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/None.gif" alt="" align="top" /><web-app>
 ..
 <filter>
    <filter-name>requestContextFilter</filter-name>
    <filter-class>org.springframework.web.filter.RequestContextFilter</filter-class>
 </filter>
 <filter-mapping>
    <filter-name>requestContextFilter</filter-name>
    <url-pattern>/*</url-pattern>
 </filter-mapping>
  ...
 <img src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/None.gif" alt="" align="top" /></web-app>
 <img src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/None.gif" alt="" align="top" />
    
    
    
      接着既可以配置bean的作用域了: 
  
  
  
    <bean id="role" class="spring.chapter2.maryGame.Role" scope="request"/>
  
  
    4、session
  
  
    session作用域表示该针对每一次HTTP请求都会产生一个新的bean，同时该bean仅在当前HTTP session内有效，配置实例: 
  
  
    配置实例: 
  
  
    和request配置实例的前提一样，配置好web启动文件就可以如下配置: 
  
  
    <bean id="role" class="spring.chapter2.maryGame.Role" scope="session"/>
  
  
    5、global session
  
  
    global session作用域类似于标准的HTTP Session作用域，不过它仅仅在基于portlet的web应用中才有意义。Portlet规范定义了全局Session的概念，它被所有构成某个portlet web应用的各种不同的portlet所共享。在global session作用域中定义的bean被限定于全局portlet Session的生命周期范围内。如果你在web中使用global session作用域来标识bean，那么web会自动当成session类型来使用。
  
  
    配置实例: 
  
  
    和request配置实例的前提一样，配置好web启动文件就可以如下配置: 
  
  
    <bean id="role" class="spring.chapter2.maryGame.Role" scope="global session"/>
  
  
    6、自定义bean装配作用域
  
  
    在spring2.0中作用域是可以任意扩展的，你可以自定义作用域，甚至你也可以重新定义已有的作用域 (但是你不能覆盖singleton和prototype) ，spring的作用域由接口org.springframework.beans.factory.config.Scope来定义，自定义自己的作用域只要实现该接口即可，下面给个实例: 
  
  
    我们建立一个线程的scope，该scope在表示一个线程中有效，代码如下:  
    
    
      <img id="_37_848_Open_Image" src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/ExpandedBlockStart.gif" alt="" align="top" />publicclass MyScope implements Scope {
 <img id="_102_199_Open_Image" src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/ExpandedSubBlockStart.gif" alt="" align="top" />     privatefinal ThreadLocal threadScope = new ThreadLocal() {
 <img id="_146_192_Open_Image" src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/ExpandedSubBlockStart.gif" alt="" align="top" />          protected Object initialValue() {
 <img src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/InBlock.gif" alt="" align="top" />            returnnew HashMap();
 <img src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/ExpandedSubBlockEnd.gif" alt="" align="top" />          }
 <img src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/ExpandedSubBlockEnd.gif" alt="" align="top" />    };
 <img id="_268_510_Open_Image" src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/ExpandedSubBlockStart.gif" alt="" align="top" />     public Object get(String name, ObjectFactory objectFactory) {
 <img src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/InBlock.gif" alt="" align="top" />        Map scope = (Map) threadScope.get();
 <img src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/InBlock.gif" alt="" align="top" />        Object object = scope.get(name);
 <img id="_384_478_Open_Image" src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/ExpandedSubBlockStart.gif" alt="" align="top" />        if(object==null) {
 <img src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/InBlock.gif" alt="" align="top" />          object = objectFactory.getObject();
 <img src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/InBlock.gif" alt="" align="top" />          scope.put(name, object);
 <img src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/ExpandedSubBlockEnd.gif" alt="" align="top" />        }
 <img src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/InBlock.gif" alt="" align="top" />        return object;
 <img src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/ExpandedSubBlockEnd.gif" alt="" align="top" />     }
 <img id="_552_642_Open_Image" src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/ExpandedSubBlockStart.gif" alt="" align="top" />     public Object remove(String name) {
 <img src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/InBlock.gif" alt="" align="top" />        Map scope = (Map) threadScope.get();
 <img src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/InBlock.gif" alt="" align="top" />        return scope.remove(name);
 <img src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/ExpandedSubBlockEnd.gif" alt="" align="top" />     }
 <img id="_720_728_Open_Image" src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/ExpandedSubBlockStart.gif" alt="" align="top" />     publicvoid registerDestructionCallback(String name, Runnable callback) {
 <img src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/ExpandedSubBlockEnd.gif" alt="" align="top" />     }
 <img id="_768_835_Open_Image" src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/ExpandedSubBlockStart.gif" alt="" align="top" />    public String getConversationId() {
 <img src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/InBlock.gif" alt="" align="top" />       // TODO Auto-generated method stub
 <img src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/InBlock.gif" alt="" align="top" />       returnnull;
 <img src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/ExpandedSubBlockEnd.gif" alt="" align="top" />    }
 <img src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/ExpandedBlockEnd.gif" alt="" align="top" />          }
 <img src="http://images.csdn.net/syntaxhighlighting/OutliningIndicators/None.gif" alt="" align="top" />
  

 [1]: http://blog.csdn.net/ProvidenceZY/article/details/1878582