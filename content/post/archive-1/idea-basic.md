---
title: idea basic
author: "-"
date: 2013-01-14T07:37:05+00:00
url: idea
categories:
  - IDE
tags:
  - reprint
---
## idea basic

生成.ipr文件: mvn idea:project
生成.iws文件: mvn idea:workspace
生成.iml文件: mvn idea:module

<https://www.jetbrains.com/idea/download/download-thanks.html?platform=linux&code=IIC>

### settings repository

    mkdir local-jetbrain-setting-repo
    cd local-jetbrain-setting-repo
    git init --bare
    # configure IntelliJ to save settings to git repo URL: "/path/to/local-jetbrain-setting-repo"
    git remote add origin git@github.com:wiloon/jetbrain-idea-setting.git
    git push origin master

### fetch

    git fetch origin master

### keys

|||
|-|-|
|列编辑|Alt+Shift+Insert,ctrl+alt+i |
|Expand All|Ctrl+Shift+= |

CTRL+SHIFT+N 查找文件
  
duplicate line and block
  
ctl+alt+Y sychronize
  
ctl+alt+S setting

---

### settings repository

    mkdir local-jetbrain-setting-repo
    cd local-jetbrain-setting-repo
    git init --bare
    # configure IntelliJ to save settings to git repo URL: "/path/to/local-jetbrain-setting-repo"
    git branch -m main # 默认创建
    git remote add origin git@github.com:wiloon/jetbrain-idea-setting.git
    git push origin main

### 解决 Intellij IDEA Cannot Resolve Symbol ‘XXX’ 问题

清除缓存

  点击菜单中的 "File" -> "Invalidate Caches / Restart"，然后点击对话框中的 "Invalidate and Restart"，清空 cache 并且重启。

### IDEA内存设置
linux

修改idea.vmoptions或idea64.vmoptions


windows

修改IntelliJ IDEA 7.0/bin下idea.exe.vmoptions


  
 -server
 -Xverify:none
 -Xms300M
 -Xmx512M
 -XX:+UseParNewGC
 -XX:PermSize=128m
 -ea
  
  
    -server 使用server jvm。酌情使用，有些doc说IDEA加该选项可以提高速度。
 -Xverify: none 关闭Java字节码验证，从而加快了类装入的速度，并使得在仅为验证目的而启动的过程中无需装入类，缩短了启动时间。
 -Xms: 是另一个设置内存的参数,用它来设置程序初始化的时候内存栈的大小，增加这个值的话你的程序的启动性能会得到提高。不过同样有前面的限制，以及受到xmx的限制。
 -Xmx: 是java的一个选项，用来设置你的应用程序能够使用的最大内存数 (看好，致使你的应用程序，不是整个jvm) ,如果你的程序要花很大内存的话，那就需要修改缺省的设置，比如配置tomcat的时候，如果流量啊程序啊都很大的话就需要加大这个值了，不过有一点是要记住的，不要大得超过你的机器的内存，那样你的机器会受不了的，到时候就死翘翘了。。
 -XX: PermSize 永久区的大小。
 -XX:+UseParNewGC 使用并行收集算法。
  
  
内存大的可以改idea.exe.vmoptions文件为: 

-Xms256m
-Xmx384m
-XX:MaxPermSize=128m
-XX:NewRatio=4
-Xss128k
-Dsun.awt.keepWorkingSetOnMinimize=true
-server
  
还有是idea.properties   可以修改一些配置，比如缓冲区设置到C盘外的其他盘下
除了对idea启动的内存分配外，还有

1. 你的C盘空闲是否足够，因为idea会在c盘你的用户目录下建立缓存。如果你的c盘空间小，运转起来会比较累。
2. 你的project是否臃肿。因为默认的idea会将所有文件都当成project的文件，而其实我们需要在idea里编辑的基本都是程序文件。而 class文件、jar文件、doc文件等等都是不需要的。打开module setting界面，切换到source选项把不属于程序文件的都exclude掉，大大降低idea的负荷。

### Coverage

Run Test选择 Run “test()”with coverage

http://hi.baidu.com/geeree/blog/item/1eeb29fab2c35f9d58ee9075.html

## native keychain is not available

```bash
pacman -S gnome-keyring

```

## idea 中文乱码

```bash
pacman -S wqy-microhei
# 重启 idea

```

## idea maven proxy

```bash
File> settings> Build,Execution,Deployment>Build Tools> maven> importing> vm options for importer:

# 192.168.50.9:1080 socks5 proxy
-DproxySet=true -DproxyHost=192.168.50.9 -DproxyPort=1080

```
