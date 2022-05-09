---
title: gradle/maven/eclipse工程相互转化
author: "-"
date: 2014-12-30T02:57:04+00:00
url: /?p=7147
categories:
  - Inbox
tags:
  - Gradle

---
## gradle/maven/eclipse工程相互转化

gradle/maven/eclipse工程相互转化: 
  
前提安装好相应的工具和插件。
  
1. Maven->eclipse

mvn eclipse:eclipse

2. eclipse->maven

安装好maven插件后,项目右键->Configure->Convert to Maven Project

3. gradle->eclipse
  
编辑build.gradle文件,在文件最前面增加一行: 
  
apply plugin: 'eclipse'

gradle eclipse

4. eclipse->gradle
  
使用eclipse的gradle插件转换,我没有测试

5. maven->gradle
  
gradle集成了一个很方便的插件: Build Init Plugin,使用这个插件可以很方便地创建一个新的gradle项目,或者将其它类型的项目转换为gradle项目。
  
gradle init -type pom

6. gradle->maven

gradle->eclipse->maven 暂时没有找到直接转换的方法,不过可以先转换成eclipse工程->借助maven或者gradle插件来转换

转换完成后相应的导入jar具体修复。

http://blog.csdn.net/earbao/article/details/41550387

http://wm-self-e-gmail-com.iteye.com/blog/1698724