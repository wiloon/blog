---
title: pacakge-info.java
author: "-"
date: 2012-08-15T05:33:17+00:00
url: /?p=3901
categories:
  - Development
  - Java

tags:
  - reprint
---
## pacakge-info.java
http://strong-life-126-com.iteye.com/blog/806246
  
翻看以前的笔记，看到一个特殊的java文件: pacakge-info.java，虽然有记录，但是不全，就尝试着追踪一下该问题， 分享一下流水账式的结果。
  
首先，它不能随便被创建。在Eclipse中， package-info文件不能随便被创建，会报"Type name is notvalid"错误，类名无效，Java变量定义规范是: 字母、数字、下划线，还有那个不怎么常用的$符号 (顺带说下，Java是支持中文名称的变量，习惯挑战的同学可以尝试下，分享一下这方面的经验) ，这个中划线可不再之列，那怎么创建这个文件呢？
  
很简单，用记事本创建一个，然后拷贝进去再改一下就成了，更直接的办法就是从别的项目中拷贝过来一个，这更方便。
      
其次，服务的对象很特殊。一个类是一类或一组事物的描述，比如Dog这个类，就是描述旺财的，那package-info这个类是描述啥的呢？它总要有一个被描述或被陈述的对象，它是描述和记录本包信息。
      
最后，类不能带有public、private访问权限。package-info.java再怎么特殊，也是一个类文件，也会被编译成package-info.class，但是在package-info.java中只能声明默认访问权限的类，也就是友好类。
  
其实还有几个特殊的地方，比如不可以继承，没有接口，没有类间关系 (关联、组合、聚合等等) 等。
  
这个文件的特殊性说完了，那再说说它有什么作用，它有三个作用: 
  
1. 为标注在包上Annotation提供便利；
  
2. 声明友好类和包常量；
  
3. 提供包的整体注释说明。
      
我们来建立一个项目演示这三个作用，建立一个package-info的Java Project，在com.company包三个类:package-info.java 是我们重点关注的，PkgAnnotation.java是一个标注在包上的注解定义，Client.java模拟业务操作类。其结构如下图: 

为标注在包上Annotation提供便利
       
首先定义一个包类型的注解，它只能放置的一个包上: 

Java代码
  
/**
   
* 定义只能标注在package上的注解
  
*/
  
@Target(ElementType.PACKAGE)
  
@Retention(RetentionPolicy.RUNTIME)
  
public @interface PkgAnnotation {
  
}

再定义一个package-info类，这个是一个特殊的类，先看代码: 

Java代码
  
@PkgAnnotation
  
package com.company;
        
很简单，就这么个文件，里面啥都没有，就这两句话，没有class类，没有常变量声明。接着写一个模拟交易类，代码如下: 

Java代码
  
public class Client {
      
public static void main(String[] args) {
          
//可以通过I/O操作或配置项获得包名
          
String pkgName = "com.company";
          
Package pkg = Package.getPackage(pkgName);
          
//获得包上的注解
          
Annotation[] annotations = pkg.getAnnotations();
          
//遍历注解数组
          
for(Annotation an:annotations){
              
if(an instanceof PkgAnnotation){
                  
System.out.println("Hi,I'm the PkgAnnotation ,which is be placed on package!");
                  
/*
                   
* 注解操作
                   
* MyAnnotation myAnn = (PkgAnnotation)an;
                   
* 还可以操作该注解包下的所有类，比如初始化，检查等等
                   
* 类似Struts的@Namespace，可以放到包名上，标明一个包的namespace路径
                   
*/
              
}
          
}
      
}
  
}
        
运行结果如下所示: 

Hi,I'm the PkgAnnotation ,which is be placed on package!

声明友好类和包常量
       
这个比较简单，而且很实用，比如一个包中有很多的内部访问的类或常量，就可以统一的放到package-info类中，这样就方便，而且集中管理，减少friendly类到处游走的情况，看例子: 

Java代码
  
@PkgAnnotation
  
package com.company;
   
//这里是包类，声明一个包使用的公共类，强调的是包访问权限
  
class PkgClass{
      
public void test(){
      
}
  
}
  
//包常量，只运行包内访问，适用于分"包"开发
  
class PkgConst{
      
static final String PACAKGE_CONST="ABC";
  
}

提供包的整体注释说明
       
如果是分"包"开发，也就是说一个包实现一个业务逻辑或功能点、或模块、或组件，则需要对一个包有很好的说明，说明这个包是干啥的，有啥作用，版本变迁，特别说明等等，如下: 

Java代码
  
/**
   
* **package-info不是平常类，其作用有三个:**
   
* 1、为标注在包上Annotation提供便利；
   
* 2、声明包的私有类和常量；
   
* 3、提供包的整体注释说明。
  
*/
  
package com.company;

通过javadoc生成的API文档如下: 

这与包下放置package.htm没啥区别，只是package-info可以更好的在代码中维护文档的完整性，并且可以实现代码与文档同步更新，package.htm也可以做到，不争论，建议是Java 1.5以上版本都使用package-info.java来注释。

与package-info相关的问题
       
在项目开发中，可以放置在包上的常用注解有: Struts的@namespace、Hibernate的@FilterDef和@TypeDef等等。在包下，随便一个类中的包名前加这些注解，Eclipse会提示"Package annotations must be in file package-info.java",在该包下建立package-info.java文件，把注解移到这里即可。
      
使用Checkstyle插件做代码检查时，会报一个警告"Missing package-info.java file."也是这个package-info文件惹的祸，在各个包下创建一个即可。