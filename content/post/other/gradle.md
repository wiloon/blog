---
title: Gradle, 目录
author: "-"
date: 2013-12-20T15:52:04+00:00
url: /?p=6053
categories:
  - Uncategorized
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