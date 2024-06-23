---
title: openjdk
author: "-"
date: 2017-04-21T00:26:31+00:00
url: jdk
categories:
  - Java
tags:
  - reprint
---
## openjdk

[http://openjdk.java.net/projects/jdk/](http://openjdk.java.net/projects/jdk/)

[https://jdk.java.net](https://jdk.java.net)

## windows install openjdk

```Bash
winget install Microsoft.OpenJDK.21
```

## archlinux install openjdk

```bash
# openjdk
sudo pacman -S jdk-openjdk
sudo pacman -S openjdk-src

# jdk8
sudo pacman -S jdk8-openjdk openjdk8-src
sudo pacman -S jdk11-openjdk

# 查看已经安装的 jdk
archlinux-java status
sudo archlinux-java set java-11-openjdk
sudo pacman -S jdk17-openjdk openjdk17-src
```

### 切换jdk版本

```bash
archlinux-java help
archlinux-java status
archlinux-java set  java-14-openjdk
```

### 查看当前 java 版本

```bash
java -version
sudo archlinux-java status
```

## ubuntu openjdk

```bash
sudo apt install openjdk-21-jdk
sudo apt install openjdk-8-jdk
sudo apt install openjdk-8-source
# openjdk 17, depends libc6 (>= 2.33)
sudo sudo apt update && sudo apt install openjdk-17-jdk openjdk-17-source

# 默认目录
ls -l /usr/lib/jvm/

# 查看
sudo update-java-alternatives -l
# 切换 jdk
sudo update-alternatives --config java

```

## 手动安装 openjdk

### download jdk

[JDK](https://jdk.java.net/22)

### AdoptOpenJDK

AdoptOpenJDK 是一个由OpenJDK构建，并以免费软件的形式提供社区版的 OpenJDK 二进制包。它至少提供 4 年的免费长期支持(LTS)。

### AdoptOpenJDK mirror

[https://mirrors.tuna.tsinghua.edu.cn/AdoptOpenJDK/16/jdk/x64/linux](https://mirrors.tuna.tsinghua.edu.cn/AdoptOpenJDK/16/jdk/x64/linux)

#### jdk 8

[https://mirrors.tuna.tsinghua.edu.cn/Adoptium/8/jdk/x64/windows/](https://mirrors.tuna.tsinghua.edu.cn/Adoptium/8/jdk/x64/windows/)

[https://mirrors.tuna.tsinghua.edu.cn/Adoptium/8/jdk/x64/linux](https://mirrors.tuna.tsinghua.edu.cn/Adoptium/8/jdk/x64/linux)

open a terminal.
  
sh jdk-6u25-linux-i586.bin

sudo gedit /etc/environment
  
add /***/jdk1.6.0_25/bin to path

add ...
  
JAVA_HOME=/***/jdk1.6.0_25
  
CLASSPATH=.:/***/jdk1.6.0_25/lib

sudo update-alternatives -install /usr/bin/java java /***/jdk1.6.0_25/bin/java 300
  
sudo update-alternatives -install /usr/bin/javac javac /***/jdk1.6.0_25/bin/javac 300

udo update-alternatives -config java

## Eclipse Temurin, Adoptium

Eclipse Temurin

Eclipse Temurin 项目是最初 AdoptOpenJDK 任务的延续。Eclipse Temurin 是 Eclipse 基金会中的 Adoptium 项目所构建的二进制文件。Adoptium 还支持和推广由 Adoptium 工作组成员组织提供的版本，Adoptium 工作组成员组织战略成员包括阿里云、Azul、华为、Karakun、微软和 Red Hat。

Eclipse Temurin 是开源许可的运行时二进制文件，与其 AdoptOpenJDK 前身不同，是经过 Java SE TCK 测试并兼容在整个 Java 生态系统中通用。

Eclipse Adaptium 还提供了工件，包括作为代码的开源基础设施、全面的持续集成构建和测试场，以及大量的质量保证测试。

Azul 和 IBM 为 Eclipse Temurin 二进制文件提供商业支持。

[https://wiki.archlinux.org/index.php/java](https://wiki.archlinux.org/index.php/java)  
[https://archlinux.org/packages/extra/x86_64/jdk8-openjdk/](https://archlinux.org/packages/extra/x86_64/jdk8-openjdk/)  

### redhat build of openjdk

[https://developers.redhat.com/products/openjdk/download?sc_cid=701f2000000RWTnAAO](https://developers.redhat.com/products/openjdk/download?sc_cid=701f2000000RWTnAAO)

### jvm specs

[https://docs.oracle.com/javase/specs/index.html](https://docs.oracle.com/javase/specs/index.html)

### jdk source code

[https://github.com/openjdk/jdk](https://github.com/openjdk/jdk)

### /usr/lib/jvm/java-8-openjdk-amd64/jre/lib/ext/libatk-wrapper.so

Java ATK Wrapper is a implementation of ATK by using JNI technic.
It converts Java Swing events into ATK events, and sends these events to
ATK-Bridge.
[https://developer.gnome.org/accessibility-devel-guide/stable/dev-start-5.html.zh_CN](https://developer.gnome.org/accessibility-devel-guide/stable/dev-start-5.html.zh_CN)

[https://blog.csdn.net/oschina_40188932/article/details/78833754](https://blog.csdn.net/oschina_40188932/article/details/78833754)

## openjdk archive

[https://jdk.java.net/archive](https://jdk.java.net/archive)

## macos openjdk

```bash
brew install openjdk
```
