---
title: Gradle, 目录
author: "-"
date: 2013-12-20T15:52:04+00:00
url: /?p=6053
categories:
  - Inbox
tags:
  - Gradle

---
## Gradle, 目录

Gradle 是以 Groovy 语言为基础，面向Java应用为主。基于DSL (领域特定语言) 语法的自动化构建工具。

* build (ignore)
* build.gradle (commit)
* .gradle: (ignore) 目录自动生成, 是gradle 的缓存文件.
* gradle: (commit) gradle/wrapper/gradle-wrapper.jar, Gradle官方建议我们在所有Gradle项目中都创建Wrapper文件，方便没有安装Gradle的用户使用。
* gradlew (commit),Gradlew是包装器，自动下载包装器里定义好的gradle 版本，保证编译环境统一，gradle 是用本地的gradle版本。
* gradlew.bat (commit): for windows
* out: (ignore)
* src: (commit) source code

The wrapper is something you should check into version control. By distributing the wrapper with your project, anyone can work with it without needing to install Gradle beforehand. Even better, users of the build ar

for web project

apply plugin: 'war'

## Gradle 修改缓存文件夹.gradle路径
export GRADLE_USER_HOME=/Users/lshare/.gradle

http://blog.csdn.net/yanzi1225627/article/details/52024632

背景

Android Studio的gradle在缓存处理上有时候会莫名其妙的出问题,必要时需要手动删除缓存,然后重新编译。有时也有出于其他考虑指定gradle缓存路径。

一针见血的设置方法(本文采用)

在gradle的安装目录,编辑bin文件夹下的gradle文件,然后找到如下语句:

# Add default JVM options here. You can also use JAVA_OPTS and GRADLE_OPTS to pass JVM options to this

在这句话的下面加上如下这一句:

GRADLE_OPTS=-Dgradle.user.home=/yourpath/gradle/gradle_cache

即设置GRADLE_OPTS这个变量即可.这种修改方法尤其适合需要用gradle脚本就行编译的环境中,本文就采用这种方法。

其他方法

方法1

通过修改AndroidStudio的设置项,找到gradle相关的设置:

直接修改Service directory path即可。这种方法适合只使用AndroidStudio进行编译的环境。

方法2,修改gradle.properties文件

在其中增加一句:

gradle.user.home=D:/Cache/.gradle

缺点:每个项目都要这么加一次.

方法3,设置GRADLE_USER_HOME环境变量

在/etc/profile或~/.bash_profile增加如下:

export GRADLE_USER_HOME=D:/Cache/.gradle

方法4,通过gradle自带参数

gradle -g D:/Cache/.gradle build build

可以通过gradle -help查看各参数的含义。

总结

个人推荐修改bin/gradle文件的方法 或 方法3.