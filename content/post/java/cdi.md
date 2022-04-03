---
title: CDI
author: "-"
date: 2012-03-26T06:59:50+00:00
url: /?p=2633
categories:
  - Development
tags:
  - Java

---
<http://www.infoq.com/cn/articles/cf-javaone-2011-cdi-google-dart>

## CDI

对于依赖注入的概念，相信很多开发人员都不陌生。一个组件在运行过程中会依赖其他组件提供的功能。传统的做法是由组件本身负责查找所需的依赖对象。这种方式会造成组件之间的紧耦合，不利于组件的维护和更新。依赖注入的做法则是由组件以声明式的方式表明其依赖关系，由框架在运行时把所需的组件的Java对象注入到当前组件中。相对于Java SE来说，依赖注入的概念对于Java EE更加适用。Java EE中的很多资源和服务都是由容器来负责管理的。对于单个应用来说，查找由容器负责管理的组件并不是一件容易的事情。更好的做法是由应用来声明所需的资源和服务，由容器负责注入到应用中。通过这种方式，容器也可以更好的对资源和服务进行管理。以数据库连接为例，传统的做法需要由应用本身加载相关驱动并创建数据库连接，以及在适当的时候进行释放。而使用容器管理并注入依赖的做法，则减轻了应用开发人员的工作量。

Java EE 5中添加了对依赖注入的有限支持。通过注解可以往容器管理的对象中注入资源的对应对象。Java EE 6中把依赖注入的概念更进一步，即引入了JSR 299 (Contexts and Dependency Injection for the Java EE platform)规范，简称CDI。CDI规范吸收了来自Spring IoC容器、JBoss Seam和Google Guice的最佳实践，并与Java EE开发的实际需要相结合。正如CDI的字面含义一样，CDI中的两个核心功能是上下文信息 (context) 和依赖注入。这两个功能的结合点是Java中基本的组件模型bean。在CDI中，bean 定义了应用的状态和逻辑，并由容器来进行管理。每个被管理的bean都有定义好的绑定到特定上下文的作用域和生命周期。当需要注入或访问bean时，容器会从作用域对应的上下文中获取。当作用域失效时，对应上下文中所有的对象都会被删除。CDI中的每个bean都可以作为依赖注入时的目标。

CDI中预定义了一些常用的作用域。默认的作用域是Dependent，表示只对被注入的对象生效。作用域ApplicationScoped表示应用的全局作用域，用来创建全局唯一的对象。RequestScoped和SessionScoped则与HTTP相关，分别表示HTTP请求和HTTP会话。ConversationScoped是由应用自定义生命周期长短的作用域，可以用来实现跨多页面的工作流。如下面代码中的OrderProcessor类只存活在HTTP请求中，并且依赖OrderDao接口的实现。容器会在运行时查找到OrderDao接口的实现对象，并注入到OrderProcessor类的对象中。

@Named
@RequestScoped
public class OrderProcessor {
    @Inject
    private OrderDao orderDao;
}

通常的依赖注入方式是在代码中只依赖接口，由容器在运行时选择合适的实现类的对象来进行注入。如果接口只有一个实现类，则不需要额外的声明。如果接口有不同的实现，则需要使用限定符 (qualifier) 来声明具体使用的实现，否则容器无法做出正确的选择。CDI的一个特点是限定符不是普通的字符串，而是类型安全的注解。

通过Qualifier元注解可以创建新的限定符注解。如下面的代码创建了一个新的限定符注解InMemory。

@Qualifier
@Retention(RUNTIME)
@Target({TYPE})
public @interface InMemory {}

该注解可以添加在OrderDao接口的实现上。

@InMemory
    public class InMemoryOrderDao implements OrderDao {
}

如果在测试时，希望使用简单的基于内存的存储实现，可以使用InMemory注解来声明。这样容器在注入时会使用InMemoryOrderDao类的对象。

@Named
@RequestScoped
public class OrderProcessor {
    @Inject @InMemory
    private OrderDao orderDao;
}

使用类型安全的注解类型可以避免使用字符串时会出现的问题。在使用字符串来区分时，可能由于字符串内容的细微错误而造成难以发现的问题。


Introduction to Contexts and Dependency Injection for the Java EE Platform
  
Contexts and Dependency Injection (CDI) for the Java EE platform is one of several Java EE 6 features that help to knit together the web tier and the transactional tier of the Java EE platform. CDI is a set of services that, used together, make it easy for developers to use enterprise beans along with JavaServer Faces technology in web applications. Designed for use with stateful objects, CDI also has many broader uses, allowing developers a great deal of flexibility to integrate various kinds of components in a loosely coupled but typesafe way.

CDI is specified by JSR 299, formerly known as Web Beans. Related specifications that CDI uses include the following:

JSR 330, Dependency Injection for Java

The Managed Beans specification, which is an offshoot of the Java EE 6 platform specification (JSR 316)

The following topics are addressed here:

Overview of CDI

About Beans

About CDI Managed Beans

Beans as Injectable Objects

Using Qualifiers

Injecting Beans

Using Scopes

Giving Beans EL Names

Adding Setter and Getter Methods

Using a Managed Bean in a Facelets Page

Injecting Objects by Using Producer Methods

Configuring a CDI Application

Further Information about CDI