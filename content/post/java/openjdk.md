---
title: jdk, openjdk
author: "-"
date: 2017-04-21T00:26:31+00:00
url: jdk

---
## jdk, openjdk
### archlinux 
```bash
sudo pacman -S jdk-openjdk
sudo pacman -S openjdk-src
# jdk8
sudo pacman -S jdk8-openjdk openjdk8-src
archlinux-java status
sudo archlinux-java set java-11-openjdk
```

### ubuntu
    sudo apt install openjdk-8-jdk
    sudo apt install openjdk-8-source
    sudo apt install openjdk-16-jdk
    sudo apt install openjdk-16-source

    # 切换jdk
    sudo update-java-alternatives -l
    sudo update-java-alternatives -s <jname>
    sudo update-java-alternatives -s java-1.8.0-openjdk-amd64

## 手动安装
### download jdk
    https://jdk.java.net/archive/
    https://jdk.java.net/17/

### AdoptOpenJDK
AdoptOpenJDK是一个由OpenJDK构建，并以免费软件的形式提供社区版的 OpenJDK 二进制包。它至少提供 4 年的免费长期支持(LTS)。

### AdoptOpenJDK mirror
    https://mirrors.tuna.tsinghua.edu.cn/AdoptOpenJDK/16/jdk/x64/linux/

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

https://jdk.java.net/archive/  
https://wiki.archlinux.org/index.php/java  
https://archlinux.org/packages/extra/x86_64/jdk8-openjdk/  

### redhat build of openjdk
    https://developers.redhat.com/products/openjdk/download?sc_cid=701f2000000RWTnAAO


### jvm specs
https://docs.oracle.com/javase/specs/index.html

### jdk source code
https://github.com/openjdk/jdk