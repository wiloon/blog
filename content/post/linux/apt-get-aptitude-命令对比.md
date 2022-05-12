---
title: Apt-get, aptitude 命令对比
author: "-"
date: 2011-12-11T03:46:11+00:00
url: /?p=1845
categories:
  - Linux
tags:$
  - reprint
---
## Apt-get, aptitude 命令对比

出自Guoshuang Wiki

[http://wiki.guoshuang.com/Apt-get_%E5%92%8C_aptitude_%E5%91%BD%E4%BB%A4%E5%AF%B9%E6%AF%94%E5%8F%82%E8%80%83][1]

        Apt-get commands
      
      
      
        Aptitude commands
      
      
      
      
    
    
    
      
        apt-get install package
      
      
      
        aptitude install package
      
      
      
        install package 安装软件包
      
    
    
    
      
        apt-get install package--reinstall
      
      
      
      
      
      
        reinstall package 重新安装
      
    
    
    
      
        apt-get -f install
      
      
      
      
      
      
        force install 强制安装
      
    
    
    
      
        apt-get remove package
      
      
      
        aptitude remove package
      
      
      
        remove package 删除软件包
      
    
    
    
      
        apt-get remove package--purge
      
      
      
        aptitude purge package
      
      
      
        remove package, include configuration files 删除软件及其配置文件
      
    
    
    
      
        apt-get autoremove
      
      
      
      
      
      
        auto remove unused packages 自动删除没用的软件包
      
    
    
    
      
        apt-get update
      
      
      
        aptitude update
      
      
      
        update the list of available packages 升级软件更新列表
      
    
    
    
      
        apt-get upgrade
      
      
      
        aptitude upgrade
      
      
      
        upgrade packages 升级软件包
      
    
    
    
      
        apt-get dist-upgrade
      
      
      
        aptitude dist-upgrade
      
      
      
        upgrade to a new release 升级到下一个发行版
      
    
    
    
      
        apt-get build-dep package
      
      
      
      
      
      
        install build dependency 安装编译依赖库
      
    
    
    
      
        apt-get source package
      
      
      
      
      
      
        download source 下载源代码
      
    
    
    
      
        apt-get clean && apt-get autoclean
      
      
      
        aptitude clean && aptitude autoclean
      
      
      
        remove unused package files 删除没用的软件包
      
    
    
    
      
        apt-cache search package
      
      
      
        aptitude search package
      
      
      
        search packages 在 cache 中搜索软件包
      
    
    
    
      
        apt-cache show package
      
      
      
      
      
      
        get more information 显示软件包信息
      
    
  

 [1]: http://wiki.guoshuang.com/Apt-get_%E5%92%8C_aptitude_%E5%91%BD%E4%BB%A4%E5%AF%B9%E6%AF%94%E5%8F%82%E8%80%83