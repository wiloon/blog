---
title: gradle application plugin 打可执行jar, gradle executable/runnable jar
author: "-"
date: 2016-01-18T09:26:01+00:00
url: /?p=8674
categories:
  - Inbox
tags:
  - reprint
---
## gradle application plugin 打可执行jar, gradle executable/runnable jar
https://docs.gradle.org/current/userguide/application_plugin.html

edit build.gradle

apply plugin: 'application'
  
application {
      
applicationDefaultJvmArgs = ["-Xms512m", "-Xmx1600m"]
  
}
  
mainClassName = "org.gradle.sample.Main"

gradle distZip

applicationDefaultJvmArgs 用于配置jvm 参数