---
title: Spring MVC和Struts2的比较
author: "-"
date: 2012-11-30T03:32:23+00:00
url: /?p=4801
categories:
  - Java
  - Web
tags:$
  - reprint
---
## Spring MVC和Struts2的比较
Web层面的框架学习了三个Struts1和2，SpringMVC，那他们之间肯定存在一个优劣和适用的环境，Struts1和2的异同点我已经做过对比《[Struts1和Struts2][1]》，这篇将对比下Struts2和SpringMVC的异同，下面数据基本来源于网络，本人是搜集整理所得，供大家参考。

一个项目使用什么样的技术，决定的因素很多，我所能想到的有: 对系统的性能、开发的效率、团队学习的成本、业务场景等，下面尽量从这几个方面入手，来分析比较下他们之间存在的优劣。

首先说**性能方面**，通过一些测试人员的测试，对Jsp、Struts1、Struts2、SpringMVC的结论如下表: 


  
    
      名称
    
    
    
      性能排名
    
    
    
      结论
    
  
  
  
    
      Jsp
    
    
    
      1
    
    
    
      越原始效率越高
    
  
  
  
    
      Struts1
    
    
    
      2
    
    
    
      采用单例Action模式，且本身的封装相比struts2简单，性能稳定高效。
    
  
  
  
    
      SpringMVC
    
    
    
      2.5(略逊于struts1)
    
    
    
      springMVC有着不比struts2差的开发效率和解耦度，但性能却是struts2的好几倍。
    
  
  
  
    
      Struts2
    
    
    
      3
    
    
    
      
        
          由于采用值栈、OGNL表达式、拦截器等技术对请求参数的映射和返回结果进行了处理，另外还采用大量的标签库等，这些都增加了处理的时间；
        
        
          struts2性能的瓶颈不在于它的多例Action模式
        
      
    
  


从以上性能角度来看，如果项目中使用框架，SpringMVC是首选；如果想把效能提升到最大，jsp是首选。

然后从**开发效率**来分析: 

开发效率这点，大家做程序员的一般都会深有体会，越是靠后的产品，一般开发效率都会高一些，就像我们计算机语言的发展，从二进制到汇编语言，再到目前主流的java、C#等，都越来越接近人能理解的程度，开发效率越来越高。因此，从这个观点出发，得出的结论是: 

由快到慢: SpringMVCand Strut2 > Struts1 > jsp

框架的出现很大程度就是为了提升开发效率，解决纯手工代码带来的不便，因此Struts1优于jsp毫无疑问；Struts2和SpringMVC出现的较晚，都是吸取了Struts1的经验教训而来。那Struts2和SpringMVC哪个的开发效率要更高一些呢？根据大家在网上的体会所得: 

由高到低: SpringMVC> Struts2 (存疑) 

Springmvc可以认为已经100%零配置，但是Struts2并没有实现这点，SpringMVC高于Struts2具体理由公说公有理婆说婆有理，关于这两者的开发效率由于每个人对两者的熟悉程度不同，因此导致了不同的结果。在我看来，更愿意使用SpringMVC，如果项目中用到了Spring，那就更棒了。

**团队学习成本: **

Jsp当然是入门，如果这个都不懂，谈学习成本也毫无意义，从我个人来看，如果之前接触过Struts1和Spring，学习Struts2和SpringMVC的时间成本差不了多少，但是SpringMVC国内用的并不多，因此，相对来说SpringMVC的学习成本要大一些。

由大到小: SpringMVC> Struts2

大家可根据团队自身目前的情况，自由选择。上面这两个框架，不管学哪个，我认为Struts1都应该接触一下，这样才能更深的理解MVC框架设计的精妙之处。

**业务场景**，只要涉及到业务，就不能确定哪个框架好，哪个不好，因此，业务场景只能根据当前业务，加上对技术的深度理解，找到一款合适的框架为宜。

下面再贴一些Struts2和SpringMVC技术点的异同，其实，这些技术上的不同也正好反映在上面说到的几点中。


  
    
      Struts2
    
    
    
      Spring MVC
    
  
  
  
    
      类级别的拦截，一个类对应一个request上下文，很难实现restful url，而struts2的架构实现起来要费劲，因为action的一个方法可以对应一个url，而其类属性却被所有方法共享，这也就无法用注解或其他方式标识其所属方法了
    
    
    
      方法级别的拦截，一个方法对应一个request上下文，而方法同时又跟一个url对应，所以说从架构本身上spring3 mvc就容易实现restful url
    
  
  
  
    
      比较乱，虽然方法之间也是独立的，但其所有Action变量是共享的，这不会影响程序运行，却给我们编码读程序时带来麻烦；Struts2在接受参数的时候，可以用属性来接受参数，这就说明参数是让多个方法共享的
    
    
    
      方法之间基本上独立的，独享request response数据，请求数据通过参数获取，处理结果通过ModelMap交回给框架，方法之间不共享变量
    
  
  
  
    
      支持手动验证凭借validate方法和XWork验证框架
    
    
    
      验证也是一个亮点，支持JSR303 
      
      
        处理ajax的请求更是方便只需一个注解@ResponseBody，然后直接返回响应文本即可  
        
        
          
            入口是filter
          
          
          
            入口是servlet
          
          
        
        
          目前所能整理出来的异同点只有这些，具体的感受需要大家自行尝试，下附的连接是一篇讨论Springmvc和Struts2的帖子，供大家参考。
        
        
        
          地址: http://www.iteye.com/topic/646240
        
        
        
          
        
        
        
          
        
        
        
          http://my.oschina.net/leepi/blog/170803
        
        
        
          
        
        
        
          虽然说没有系统的学习过Spring MVC框架, 但是工作这么长时间, 基本上在WEB层使用的都是Spring MVC, 自己觉得Struts2也是一个不错的WEB层框架, 这两种框架至今自己还未有比较, 今天闲着没事干, 从网上找了一些资料, 再加上平时使用Spring MVC的感触来总结一下。
        
        
        
          Spring MVC PK Struts2
        
        
        
          我们用struts2时采用的传统的配置文件的方式，并没有使用传说中的0配置。spring3 mvc可以认为已经100%零配置了 (除了配置spring mvc-servlet.xml外) 。
        
        
        
          Spring MVC和Struts2的区别: 
        
        
        
          1. 机制: spring mvc的入口是servlet，而struts2是filter (这里要指出，filter和servlet是不同的。以前认为filter是servlet的一种特殊) ，这样就导致了二者的机制不同，这里就牵涉到servlet和filter的区别了。
        
        
        
          2. 性能: spring会稍微比struts快。spring mvc是基于方法的设计，而sturts是基于类，每次发一次请求都会实例一个action，每个action都会被注入属性，而spring基于方法，粒度更细，但要小心把握像在servlet控制数据一样。spring3 mvc是方法级别的拦截，拦截到方法后根据参数上的注解，把request数据注入进去，在spring3 mvc中，一个方法对应一个request上下文。而struts2框架是类级别的拦截，每次来了请求就创建一个Action，然后调用setter getter方法把request中的数据注入；struts2实际上是通过setter getter方法与request打交道的；struts2中，一个Action对象对应一个request上下文。
        
        
        
          3. 参数传递: struts是在接受参数的时候，可以用属性来接受参数，这就说明参数是让多个方法共享的。
        
        
        
          4. 设计思想上: struts更加符合oop的编程思想， spring就比较谨慎，在servlet上扩展。
        
        
        
          5. intercepter的实现机制: struts有以自己的interceptor机制，spring mvc用的是独立的AOP方式。这样导致struts的配置文件量还是比spring mvc大，虽然struts的配置能继承，所以我觉得论使用上来讲，spring mvc使用更加简洁，开发效率Spring MVC确实比struts2高。spring mvc是方法级别的拦截，一个方法对应一个request上下文，而方法同时又跟一个url对应，所以说从架构本身上spring3 mvc就容易实现restful url。struts2是类级别的拦截，一个类对应一个request上下文；实现restful url要费劲，因为struts2 action的一个方法可以对应一个url；而其类属性却被所有方法共享，这也就无法用注解或其他方式标识其所属方法了。spring3 mvc的方法之间基本上独立的，独享request response数据，请求数据通过参数获取，处理结果通过ModelMap交回给框架方法之间不共享变量，而struts2搞的就比较乱，虽然方法之间也是独立的，但其所有Action变量是共享的，这不会影响程序运行，却给我们编码，读程序时带来麻烦。
        
        
        
          6. 另外，spring3 mvc的验证也是一个亮点，支持JSR303，处理ajax的请求更是方便，只需一个注解@ResponseBody ，然后直接返回响应文本即可。送上一段代码: 
        
        
        
          @RequestMapping(value="/whitelists")
 public String index(ModelMap map) {
 Account account = accountManager.getByDigitId(SecurityContextHolder.get().getDigitId());
 List<Group> groupList = groupManager.findAllGroup(account.getId());
 map.put("account", account);
 map.put("groupList", groupList);
 return "/group/group-index";
 }
        
        
        
          // @ResponseBody ajax响应，处理Ajax请求也很方便
 @RequestMapping(value="/whitelist/{whiteListId}/del")
 @ResponseBody
 public String delete(@PathVariable Integer whiteListId) {
 whiteListManager.deleteWhiteList(whiteListId);
 return "success";
 }
        

 [1]: http://blog.csdn.net/stubbornpotatoes/article/details/8679523