---
title: jdk, openjdk
author: "-"
date: 2017-04-21T00:26:31+00:00
url: jdk
categories:
  - java
tags:
  - reprint
---
## jdk, openjdk

<http://openjdk.java.net/projects/jdk/>

## archlinux

```bash
sudo pacman -S jdk-openjdk
sudo pacman -S openjdk-src
# jdk8
sudo pacman -S jdk8-openjdk openjdk8-src
archlinux-java status
sudo archlinux-java set java-11-openjdk
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

## ubuntu

```bash
sudo apt install openjdk-8-jdk
sudo apt install openjdk-8-source
sudo apt install openjdk-17-jdk
sudo apt install openjdk-17-source

# 默认目录
ls -l /usr/lib/jvm/

# 查看
sudo update-java-alternatives -l
# 切换jdk
sudo update-alternatives --config java

```

## 手动安装

### download jdk

    https://jdk.java.net/archive/
    https://jdk.java.net/17/

### AdoptOpenJDK

AdoptOpenJDK 是一个由OpenJDK构建，并以免费软件的形式提供社区版的 OpenJDK 二进制包。它至少提供 4 年的免费长期支持(LTS)。

### AdoptOpenJDK mirror

    https://mirrors.tuna.tsinghua.edu.cn/AdoptOpenJDK/16/jdk/x64/linux/

#### jdk 8
<https://mirrors.tuna.tsinghua.edu.cn/AdoptOpenJDK/8/jdk/x64/linux/OpenJDK8U-jdk_x64_linux_hotspot_8u312b07.tar.gz>

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

---

<https://jdk.java.net/archive/>  
<https://wiki.archlinux.org/index.php/java>  
<https://archlinux.org/packages/extra/x86_64/jdk8-openjdk/>  

### redhat build of openjdk

    https://developers.redhat.com/products/openjdk/download?sc_cid=701f2000000RWTnAAO

### jvm specs
<https://docs.oracle.com/javase/specs/index.html>

### jdk source code
<https://github.com/openjdk/jdk>

### /usr/lib/jvm/java-8-openjdk-amd64/jre/lib/ext/libatk-wrapper.so

Java ATK Wrapper is a implementation of ATK by using JNI technic.
It converts Java Swing events into ATK events, and sends these events to
ATK-Bridge.
<https://developer.gnome.org/accessibility-devel-guide/stable/dev-start-5.html.zh_CN>

<https://blog.csdn.net/oschina_40188932/article/details/78833754>
