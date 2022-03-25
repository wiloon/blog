---
title: spring restful, spring boot, maven,gradle
author: "-"
date: 2017-02-22T08:51:55+00:00
url: spring/boot
categories:
  - Spring

tags:
  - reprint
---
## spring restful, spring boot, maven,gradle
### spring-boot-starter-parent
```xml
  <parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>2.6.2</version>
  </parent>

```

表示当前pom文件从spring-boot-starter-parent继承下来，在spring-boot-starter-parent中提供了很多默认的配置，这些配置可以大大简化我们的开发。

Parent Poms Features
通过继承spring-boot-starter-parent，默认具备了如下功能：

Java版本 (Java8）
源码的文件编码方式 (UTF-8）
依赖管理
打包支持
动态识别资源
识别插件配置
识别不同的配置，如：application-dev.properties 和 application-dev.yml
以上继承来的特性有的并非直接继承自spring-boot-starter-parent，而是继承自spring-boot-starter-parent的父级spring-boot-dependencies

需要特别说明的是，application-dev.properties 和 application-dev.yml支持spring风格的占位符(${…​})，但是Maven项目把对占位符的支持改为(@..@)，可以通过设置Maven属性resource.delimiter来重置回去。

继承spring-boot-starter-parent后，大大简化了我们的配置，它提供了丰富的常用的默认的依赖的版本定义，我们就不需要再次指定版本号：

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
</dependencies>
```
假设我们需要定制自己的版本号，可以通过下面的方式重写：

### spring-boot-starter-web
<properties>
    <spring-data-releasetrain.version>Fowler-SR2</spring-data-releasetrain.version>
</properties>


### 
```xml
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
```
Spring Web Starter使用Spring MVC，REST和Tomcat作为默认的嵌入式服务器

Spring Boot还支持另外两个嵌入式服务器：

Jetty Server
Undertow Server

```bash
gradle bootRun
```

### run with env

    java -jar xxx.jar --spring.profiles.active=prod

>https://tengj.github.io/2017/02/26/springboot1/
http://git.oschina.net/wiloon/java8x/tree/master/java-web-x?dir=1&filepath=java-web-x&oid=f781e8d83fbb0bf06b36e766fbe0bbaeb8f51756&sha=121ba0714d171c1fe53e246cf86a43fb145589b4

https://spring.io/guides/gs/rest-service/

https://github.com/mariuszs/spring-boot-web-jsp-example

作者：Johnny_
链接：https://www.jianshu.com/p/628acadbe3d8
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

>https://www.yiibai.com/spring-boot/spring-boot-starter-web.html


### Spring Boot 启动时，让方法自动执行的 4 种方法！
1. 实现ServletContextAware接口并重写其setServletContext方法

```java
@Component
public class TestStarted implements ServletContextAware {
    /**
     * 在填充普通bean属性之后但在初始化之前调用
     * 类似于initializingbean的afterpropertiesset或自定义init方法的回调
     *
     */
    @Override
    public void setServletContext(ServletContext servletContext) {
        System.out.println("setServletContext方法");
    }
}
```
注意：该方法会在填充完普通Bean的属性，但是还没有进行Bean的初始化之前执行

2、实现ServletContextListener接口

/**
 * 在初始化Web应用程序中的任何过滤器或servlet之前，将通知所有servletContextListener上下文初始化。
 */
@Override
public void contextInitialized(ServletContextEvent sce) {
    //ServletContext servletContext = sce.getServletContext();
    System.out.println("执行contextInitialized方法");
}
3、将要执行的方法所在的类交个spring容器扫描(@Component),并且在要执行的方法上添加@PostConstruct注解或者静态代码块执行

@Component
public class Test2 {
    //静态代码块会在依赖注入后自动执行,并优先执行
    static{
        System.out.println("---static--");
    }
    /**
     *  @Postcontruct’在依赖注入完成后自动调用
     */
    @PostConstruct
    public static void haha(){
        System.out.println("@Postcontruct’在依赖注入完成后自动调用");
    }
}
4、实现ApplicationRunner接口

/**
 * 用于指示bean包含在SpringApplication中时应运行的接口。可以定义多个applicationrunner bean
 * 在同一应用程序上下文中，可以使用有序接口或@order注释对其进行排序。
 */
@Override
public void run(ApplicationArguments args) throws Exception {
    System.out.println("ApplicationRunner的run方法");
}
5、实现CommandLineRunner接口

/**
 * 用于指示bean包含在SpringApplication中时应运行的接口。可以在同一应用程序上下文中定义多个commandlinerunner bean，并且可以使用有序接口或@order注释对其进行排序。
 * 如果需要访问applicationArguments而不是原始字符串数组，请考虑使用applicationrunner。
 * 
 */
@Override
public void run(String... ) throws Exception {
    System.out.println("CommandLineRunner的run方法");
}

>https://segmentfault.com/a/1190000039363178

### 参数检验
@NotEmpty用在集合类上面 @NotBlank 用在String上面 @NotNull 用在基本类型上