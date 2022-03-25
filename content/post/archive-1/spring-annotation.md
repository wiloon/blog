---
title: spring annotation
author: "-"
date: 2014-04-30T01:55:01+00:00
url: spring
categories:
  - Spring

tags:
  - reprint
---
## spring annotation
@Component；@Controller；@Service；@Repository 

### @Component
在annotaion配置注解中用 @Component 来表示一个通用注释用于说明一个类是一个spring容器管理的类。即就是该类已经纳入到spring的管理中了。而@Controller, @Service, @Repository是 @Component 的细化，这三个注解比 @Component 带有更多的语义，它们分别对应了控制层、服务层、持久层的类。 
### @Service
@Service 用于标注业务层组件,对象名默认是类名 (头字母小写), 如果想自定义，可以@Service("foo")这样来指定，这种bean默认是单例的，如果想改变，可以使用@Service("foo") @Scope("prototype")来改变。

@Controller用于标注控制层组件 (如struts中的action) 

@Repository用于标注数据访问组件，即DAO组件

@Component 泛指组件，当组件不好归类的时候，我们可以使用这个注解进行标注。

@Autowired Spring自己定义的注解,

JSR-250规范定义的注解

@Resource @Resource的作用相当于@Autowired，只不过@Autowired按byType自动注入，而@Resource默认按 byName自动注入

### @Value
将外部的值动态注入到Bean中

    @Value("normal")
    private String normal; // 注入普通字符串

    @Value("#{systemProperties['os.name']}")
    private String systemPropertiesName; // 注入操作系统属性

    @Value("#{ T(java.lang.Math).random() * 100.0 }")
    private double randomNumber; //注入表达式结果

    @Value("#{beanInject.another}")
    private String fromAnotherBean; // 注入其他Bean属性: 注入beanInject对象的属性another，类具体定义见下面

    @Value("classpath:com/hry/spring/configinject/config.txt")
    private Resource resourceFile; // 注入文件资源

    @Value("http://www.baidu.com")
    private Resource testUrl; // 注入URL资源

### @PostConstruct
注解在方法上，表示此方法是在Spring实例化该Bean之后马上执行此方法，之后才会去实例化其他Bean，并且一个Bean中@PostConstruct注解的方法可以有多个。

### @Resource
@Resource默认按照ByName自动注入，由J2EE提供，需要导入包javax.annotation.Resource。@Resource有两个重要的属性: name和type，而Spring将@Resource注解的name属性解析为bean的名字，而type属性则解析为bean的类型。所以，如果使用name属性，则使用byName的自动注入策略，而使用type属性时则使用byType自动注入策略。如果既不制定name也不制定type属性，这时将通过反射机制使用byName自动注入策略。


http://www.chinasb.org/archives/2011/06/2443.shtml

http://www.cnblogs.com/chenzhao/archive/2012/02/25/2367978.html