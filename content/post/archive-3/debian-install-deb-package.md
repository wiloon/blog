---
title: dpkg
author: "-"
date: 2020-03-22T07:48:28+00:00
url: dpkg
categories:
  - Linux
tags:
  - reprint
---
## dpkg

## Ubuntu 查看软件包是否安装

```bash
# 显示包含此软件包的所有位置
dpkg -S softwarename


# -s status, 查看软件包状态
dpkg -s <package-name>

# 可以加通配符*
dpkg-query -l <package-name> 

# 列出软件包的位置, 安装路径
dpkg -L <package-name>

# 列出哪些软件包被安装
dpkg --get-selections | grep <package-name>*

# 查看版本
dpkg -l softwarename
```

## debian install deb package

deb 包
  
deb包是debian，ubuntu等LINUX发行版的软件安装包，是类似于rpm的软件包，而非debian,ubuntu系统不推荐使用deb软件包，因为要解决软件包依赖问题，安装也比较麻烦。
  
安装方法有两种:
  
一般在此类发行版中可以直接双击安装。
  
手动安装。如果您喜欢使用终端，您需要管理员权限来安装一个 .deb 文件。
  
打开终端后，输入: sudo dpkg -i package_file.deb
  
但是在包含有依赖关系的安装包手动安装的过程中会出现安装不成功的问题，这时只需输入命令: sudo apt-get -f install 待命令执行完成，软件也就安装成功了。
  
卸载安装包时，在终端中，输入:sudo dpkg -r package_name
  
————————————————
  
版权声明: 本文为CSDN博主「wangmg0118」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
  
原文链接: [https://blog.csdn.net/wangmg0118/article/details/72026739](https://blog.csdn.net/wangmg0118/article/details/72026739)

[https://blog.csdn.net/HelloJinYe/article/details/109112976](https://blog.csdn.net/HelloJinYe/article/details/109112976)
