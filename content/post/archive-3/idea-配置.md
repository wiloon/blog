---
title: idea config, 配置
author: "-"
date: 2019-04-14T05:34:17.000+00:00
url: "/?p=14170"
categories:
- Uncategorized
tags:
  - reprint
---
## idea config, 配置
### intellij idea 设置显示空格

View>Active Editor>show whitespaces

### 在IDEA里输入中文，fcitx
    vim /sbin/idea
    export XMODIFIERS="@im=fcitx"
    export GTK_IM_MODULE="fcitx"
    export QT_IM_MODULE="fcitx"

https://blog.csdn.net/shiyibodec/article/details/73549501

### java compiler

File > Settings > Build, Execution, Deployment > Compiler > Java Compiler

Change Target bytecode version to 1.8 of the module that you are working for.

https://yangbingdong.com/2017/note-of-learning-idea-under-ubuntu/

### font

JetBrain推出了一个新的字体 JetBrain Mono. 号称是最适合程序员的编码的字体

### terminal 字体

Setting->Editor->Color Scheme->Console Font

### openjdk source

Go to Project Structure dialog, select the "SDKs" node, select your JDK,

select the "Sourcepath" tab, press the "Add" button and select src.zip (it's

actually added there by default, so I'm not sure why it wasn't picked up

automatically for you). You don't need to unpack the archive or add it as

a source root.

### sql语法检查

勾掉Unresolved refereence

Settings>Editor>inspections>SQL

### java system property, system env

Run configuration> vm option : java system property
environment variable : system env

### hidpi --

https://intellij-support.jetbrains.com/hc/en-us/articles/360007994999-HiDPI-configuration

Settings > Appearance and Behavior > Appearance > Use custom font

勾选use custom font 并设置字号

设置字号 Settings > Editor>Font

https://intellij-support.jetbrains.com/hc/en-us/community/posts/206295629-Attaching-jdk-src-to-Intellij

https://www.jianshu.com/p/e20eb9645ce9