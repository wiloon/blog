---
title: Maven中的DependencyManagement和Dependencies
author: "-"
date: 2014-04-28T05:52:59+00:00
url: /?p=6564
categories:
  - Inbox
tags:
  - Maven

---
## Maven中的DependencyManagement和Dependencies
这里介绍一个在父项目中的根结点中声明dependencyManagement和dependencies的区别

dependencyManagement

Maven 使用dependencyManagement 元素来提供了一种管理依赖版本号的方式。通常会在一个组织或者项目的最顶层的父POM 中看到dependencyManagement 元素。使用pom.xml 中的dependencyManagement 元素能让

所有在子项目中引用一个依赖而不用显式的列出版本号。Maven 会沿着父子层次向上走，直到找到一个拥有dependencyManagement 元素的项目，然后它就会使用在这个dependencyManagement 元素中指定的版本号。


例如在父项目里: 

Xml代码 收藏代码

<dependencyManagement>

<dependencies>

<dependency>

<groupId>MySQL</groupId>

MySQL-connector-java</artifactId>

<version>5.1.2</version>

</dependency>

...

<dependencies>

</dependencyManagement>

然后在子项目里就可以添加MySQL-connector时可以不指定版本号，例如: 


Xml代码 收藏代码

<dependencies>

<dependency>

<groupId>MySQL</groupId>

MySQL-connector-java</artifactId>

</dependency>

</dependencies>

这样做的好处就是: 如果有多个子项目都引用同一样依赖，则可以避免在每个使用的子项目里都声明一个版本号，这样当想升级或切换到另一个版本时，只需要在顶层父容器里更新，而不需要一个一个子项目的修改 ；另外如果某个子项目需要另外的一个版本，只需要声明version就可。


dependencyManagement里只是声明依赖，并不实现引入，因此子项目需要显式的声明需要用的依赖。

dependencies

相对于dependencyManagement，所有声明在dependencies里的依赖都会自动引入，并默认被所有的子项目继承。


classifier

如果你要发布同样的代码，但是由于技术原因需要生成两个单独的构件，你就要使用一个分类器 (classifier) 。例如，如果你想要构建两个单独的构件成JAR，一个使用Java 1.4 编译器，另一个使用Java 6 编译器，你就可以使用分类器

来生成两个单独的JAR构件，它们有同样的groupId:artifactId:version组合。如果你的项目使用本地扩展类库，你可以使用分类器为每一个目标平台生成一个构件。分类器常用于打包构件的源码，JavaDoc 或者二进制集合。