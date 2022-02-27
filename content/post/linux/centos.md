---
title: centos basic
author: "-"
date: 2012-01-25T01:22:34+00:00
url: centos
categories:
  - Linux

tags:
  - reprint
---
## centos basic

centos 7 minimal 安装之后 磁盘占用 1.4G

- yum repo

    curl -o /etc/yum.repos.d/CentOS-Base.repo https://mirrors.aliyun.com/repo/Centos-7.repo

## dhcp

    vim /etc/sysconfig/network-scripts/ifcfg-eth0

    bootproto=dhcp
    onboot=yes

## Linux centos livecd bin netinstall 各版本的区别
CentOS-5.5-x86_64-LiveCD.iso 光盘系统
  
CentOS-5.5-x86_64-bin-DVD 64位安装盘
  
CentOS-5.5-x86_64-netinstall 64位网络安装盘

LiveCD一般用来修复系统使用，有容量很小，不用安装，可以自启动等特性，可以直接使用光盘启动的系统。 bin DVD也具有同样的功能，但是体积较大，需要安装到硬盘使用。 netinstall和bin都可以用来安装系统，不同的是，netinstall根据你选择的软件列表从网上下载，然后进行系统安装； bin DVD本身包含了软件，不需要依赖于网络经行安装。