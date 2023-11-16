---
title: Spring Annotation @Resource
author: "-"
date: 2013-01-16T04:37:18+00:00
url: /?p=5031
categories:
  - Java
  - Web
tags:
  - Spring

---
## Spring Annotation @Resource

Spring 不但支持自己定义的 `@Autowired` 的注释，还支持几个由 JSR-250 规范定义的注释，它们分别是`@Resource`、`@PostConstruct` 以及 `@PreDestroy`。

**@Resource**

`@Resource` 的作用相当于 `@Autowired`，只不过 `@Autowired` 按 byType 自动注入，面 `@Resource` 默认按 byName 自动注入罢了。`@Resource` 有两个属性是比较重要的，分别是 name 和 type，Spring 将 `@Resource` 注释的 name 属性解析为 Bean 的名字，而 type 属性则解析为 Bean 的类型。所以如果使用 name 属性，则使用 byName 的自动注入策略，而使用 type 属性时则使用 byType 自动注入策略。如果既不指定 name 也不指定 type 属性，这时将通过反射机制使用 byName 自动注入策略。

 @Resource装配顺序

  1. 如果同时指定了name和type，则从Spring上下文中找到唯一匹配的bean进行装配，找不到则抛出异常
  2. 如果指定了name，则从上下文中查找名称 (id) 匹配的bean进行装配，找不到则抛出异常
  3. 如果指定了type，则从上下文中找到类型匹配的唯一bean进行装配，找不到或者找到多个，都会抛出异常
  4. 如果既没有指定name，又没有指定type，则自动按照byName方式进行装配 (见2) ；如果没有匹配，则回退为一个原始类型 (UserDao) 进行匹配，如果匹配则自动装配；

Spring不但支持自己定义的@Autowired注解，还支持几个由JSR-250规范定义的注解，它们分别是@Resource、@PostConstruct以及@PreDestroy。
  
@Resource的作用相当于@Autowired，只不过@Autowired按byType自动注入，而@Resource默认按 byName自动注入罢了。@Resource有两个属性是比较重要的，分是name和type，Spring将@Resource注解的name属性解析为bean的名字，而type属性则解析为bean的类型。所以如果使用name属性，则使用byName的自动注入策略，而使用type属性时则使用byType自动注入策略。如果既不指定name也不指定type属性，这时将通过反射机制使用byName自动注入策略。
  
@Resource装配顺序
  
1. 如果同时指定了name和type，则从Spring上下文中找到唯一匹配的bean进行装配，找不到则抛出异常
  
2. 如果指定了name，则从上下文中查找名称 (id) 匹配的bean进行装配，找不到则抛出异常
  
3. 如果指定了type，则从上下文中找到类型匹配的唯一bean进行装配，找不到或者找到多个，都会抛出异常
  
4. 如果既没有指定name，又没有指定type，则自动按照byName方式进行装配；如果没有匹配，则回退为一个原始类型进行匹配，如果匹配则自动装配；

@Autowired 与@Resource的区别:

1. @Autowired与@Resource都可以用来装配bean. 都可以写在字段上,或写在setter方法上。

2. @Autowired默认按类型装配 (这个注解是属业spring的) ，默认情况下必须要求依赖对象必须存在，如果要允许null值，可以设置它的required属性为false，如: @Autowired(required=false) ，如果我们想使用名称装配可以结合@Qualifier注解进行使用，如下:

            1
          
          
          
            2
          
        
        
        
          
            
              @Autowired() @Qualifier("baseDao")
            
            
            
              private BaseDao baseDao;

3. @Resource (这个注解属于J2EE的) ，默认安装名称进行装配，名称可以通过name属性进行指定，如果没有指定name属性，当注解写在字段上时，默认取字段名进行安装名称查找，如果注解写在setter方法上默认取属性名进行装配。当找不到与名称匹配的bean时才按照类型进行装配。但是需要注意的是，如果name属性一旦指定，就只会按照名称进行装配。

            1
          
          
          
            2
          
        
        
        
          
            
              @Resource(name="baseDao")
            
            
            
              private BaseDao baseDao;

推荐使用: @Resource注解在字段上，这样就不用写setter方法了，并且这个注解是属于J2EE的，减少了与spring的耦合。这样代码看起就比较优雅。

Resource 注释类位于 Spring 发布包的 lib/j2ee/common-annotations.jar 类包中，因此在使用之前必须将其加入到项目的类库中。来看一个使用 `@Resource` 的例子:
  
**清单 16. 使用 @Resource 注释的 Boss.java**

package com.baobaotao;

import javax.annotation.Resource;

public class Boss {
    // 自动注入类型为 Car 的 Bean
    @Resource
    private Car car;

    // 自动注入 bean 名称为 office 的 Bean
    @Resource(name = "office")
    private Office office;
}

一般情况下，我们无需使用类似于 `@Resource(type=Car.class)` 的注释方式，因为 Bean 的类型信息可以通过 Java 反射从代码中获取。

要让 JSR-250 的注释生效，除了在 Bean 类中标注这些注释外，还需要在 Spring 容器中注册一个负责处理这些注释的 `BeanPostProcessor`:

      <bean
 />

`CommonAnnotationBeanPostProcessor` 实现了 `BeanPostProcessor` 接口，它负责扫描使用了 JSR-250 注释的 Bean，并对它们进行相应的操作。

**@PostConstruct 和 @PreDestroy**

Spring 容器中的 Bean 是有生命周期的，Spring 允许在 Bean 在初始化完成后以及 Bean 销毁前执行特定的操作，您既可以通过实现 InitializingBean/DisposableBean 接口来定制初始化之后 / 销毁之前的操作方法，也可以通过 <bean> 元素的 init-method/destroy-method 属性指定初始化之后 / 销毁之前调用的操作方法。关于 Spring 的生命周期，笔者在《精通 Spring 2.x—企业应用开发精解》第 3 章进行了详细的描述，有兴趣的读者可以查阅。

JSR-250 为初始化之后/销毁之前方法的指定定义了两个注释类，分别是 @PostConstruct 和 @PreDestroy，这两个注释只能应用于方法上。标注了 @PostConstruct 注释的方法将在类实例化后调用，而标注了 @PreDestroy 的方法将在类销毁之前调用。
  
**清单 17. 使用 @PostConstruct 和 @PreDestroy 注释的 Boss.java**

package com.baobaotao;

import javax.annotation.Resource;
import javax.annotation.PostConstruct;
import javax.annotation.PreDestroy;

public class Boss {
    @Resource
    private Car car;

    @Resource(name = "office")
    private Office office;

    @PostConstruct
    public void postConstruct1(){
        System.out.println("postConstruct1");
    }

    @PreDestroy
    public void preDestroy1(){
        System.out.println("preDestroy1");
    }
    …
}

您只需要在方法前标注 `@PostConstruct` 或 `@PreDestroy`，这些方法就会在 Bean 初始化后或销毁之前被 Spring 容器执行了。

我们知道，不管是通过实现 `InitializingBean`/`DisposableBean` 接口，还是通过 <bean> 元素的`init-method/destroy-method` 属性进行配置，都只能为 Bean 指定一个初始化 / 销毁的方法。但是使用`@PostConstruct` 和 `@PreDestroy` 注释却可以指定多个初始化 / 销毁方法，那些被标注 `@PostConstruct` 或`@PreDestroy` 注释的方法都会在初始化 / 销毁时被执行。

通过以下的测试代码，您将可以看到 Bean 的初始化 / 销毁方法是如何被执行的:
  
**清单 18. 测试类代码**

package com.baobaotao;

import org.springframework.context.support.ClassPathXmlApplicationContext;

public class AnnoIoCTest {

    public static void main(String[] args) {
        String[] locations = {"beans.xml"};
        ClassPathXmlApplicationContext ctx =
            new ClassPathXmlApplicationContext(locations);
        Boss boss = (Boss) ctx.getBean("boss");
        System.out.println(boss);
        ctx.destroy();// 关闭 Spring 容器，以触发 Bean 销毁方法的执行
    }
}

这时，您将看到标注了 `@PostConstruct` 的 `postConstruct1()` 方法将在 Spring 容器启动时，创建 `Boss` Bean 的时候被触发执行，而标注了 `@PreDestroy` 注释的 `preDestroy1()` 方法将在 Spring 容器关闭前销毁 `Boss`Bean 的时候被触发执行。

[http://blog.sina.com.cn/s/blog_4bc179a80100w7ap.html](http://blog.sina.com.cn/s/blog_4bc179a80100w7ap.html)
