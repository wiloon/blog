---
title: maven plugins, pluginManagement
author: "-"
date: 2018-03-06T06:40:17+00:00
url: /?p=11959
categories:
  - Inbox
tags:
  - reprint
---
## maven plugins, pluginManagement
https://www.jianshu.com/p/49acf1246eff

1.plugins和pluginManagement的区别概述
  
plugins 和 pluginManagement 的区别,和我们前面研究过的 dependencies 和 dependencyManagement 的区别是非常类似的。plugins 下的 plugin 是真实使用的,而 pluginManagement 下的 plugins 下的 plugin 则仅仅是一种声明,子项目中可以对 pluginManagement 下的 plugin 进行信息的选择、继承、覆盖等。

2.pluginManagement使用实战
  
假如存在两个项目,项目A为项目B的父项目,其关系通过pom文件的关系确定。项目A的父pom文件片段如下: <pluginManagement> <plugins> <plugin> <groupId>org.apache.maven.plugins</groupId>

              
maven-source-plugin</artifactId>
              
<version>2.1</version>
              
<configuration>
                  
true</attach>
              
</configuration>
              
<executions>
                  
<execution> <phase>compile</phase> <goals>
                          
<goal>jar</goal>
                      
</goals>
                  
</execution>
              
</executions> </plugin> </plugins> </pluginManagement> 如果项目B也想使用该plugin配置,则在项目B的子pom文件中只需要如下配置:  <plugins> <plugin> <groupId>org.apache.maven.plugins</groupId>
          
maven-source-plugin</artifactId> </plugin> </plugins> 我们可以看到,子pom文件中,省去了版本、配置细节等信息,只需要指定groupId和artifactId,其他信息均从父pom文件继承。当然,如果子pom文件想定制自己的特定内容,可以另行设置,并会覆盖从父pom文件继承到的内容。 

需要注意的是,dependencies 和 dependencyManagement 均是 project 下的直接子元素,但是 plugins 和 pluginManagement 却是 project 下 build 的直接子元素。

作者: 秋梦尘
  
链接: https://www.jianshu.com/p/49acf1246eff
  
來源: 简书
  
著作权归作者所有。商业转载请联系作者获得授权,非商业转载请注明出处。