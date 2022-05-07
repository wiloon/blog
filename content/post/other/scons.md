---
title: SCons
author: "-"
date: 2013-02-12T14:51:01+00:00
url: /?p=5134
categories:
  - Linux

tags:
  - reprint
---
## SCons

  一、概述

        scons是一个Python写的自动化构建工具,和GNU make相比优点明显: 
 1、 移植性: python能运行的地方,就能运行scons
 2、 扩展性: 理论上scons只是提供了python的类,scons使用者可以在这个类的基础上做所有python能做的事情。比如想把一个已经使用了Makefile大型工程切换到scons,就可以保留原来的Makefile,并用python解析Makefile中的编译选项、源/目标文件等,作为参数传递给scons,完成编译。
 3、 智能: Scons继承了autoconf/automake的功能,自动解析系统的include路径、typedef等；"以全局的观点来看所有的依赖关系"
  
    二、scons文件
  
  
    scons中可能出现的文件: 
 SConstruct,Sconstruct,sconstruct,SConscript
  
    scons将在当前目录以下次序 SConstruct,Sconstruct,sconstruct 来搜索配置文件,从读取的第一个文件中读取相关配置。
 在配置文件SConstruct中可以使用函数SConscript()函数来定附属的配置文件。按惯例,这些附属配置文件被命名为"SConscript",当然也可以使用任意其它名字。
  
    三、scons的命令行参数
  
  
    执行SConstruct中脚本
  
  
    ```bash
  
  
    scons
  
  
    ```
  
  
    scons -c   clean
 scons -Q  只显示编译信息,去除多余的打印信息
 scons -Q   -implicit-cache hello 保存依赖关系
 -implicit-deps-changed   强制更新依赖关系
 -implicit-deps-unchanged  强制使用原先的依赖关系,即使已经改变
  