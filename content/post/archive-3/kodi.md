---
title: kodi, openelec
author: "-"
date: 2022-10-14 17:47:44
draft: true
url: kodi
categories:
  - Inbox
tags:
  - reprint
---
## kodi, openelec

### LibreELEC

官网地址 <https://github.com/LibreELEC/LibreELEC.tv> LibreELEC 是从OpenELEC早期版本独立出来的一个分支. 与OpenELEC相比更精简, 更新更快(monthly updates), 官网文档详细, 更容易安装, 目前Kodi主页上的Friends列表, 只有LibreELEC, 没有OpenELEC. 目前大部分用户更倾向于使用LibreELEC.

### CoreELEC

官网地址 <https://coreelec.org/>
Github地址 <https://github.com/CoreELEC/CoreELEC>
CoreELEC 是LibreELEC的一个分支, 专注于在Amlogic芯片方案上运行的Kodi. 如果你的盒子使用的是Amlogic系列芯片, 推荐使用这个.

### Kodi

官网地址 <https://kodi.tv/>

首先是Kodi(曾经也叫XBMC), 是一个可以跨多平台运行的影音娱乐中心软件. 由XMBC/Kodi基金会资助开发. 是当前各种ELEC项目的鼻祖.
<https://github.com/taxigps/xbmc-addons-chinese>

### OpenELEC

官网地址 <https://openelec.tv/>

OpenELEC(Open Embedded Linux Entertainment Center)是一个基于JeOS(Just Enough Operating System)的精简Linux, 用于将电脑变为可以运行Kodi的家庭媒体娱乐中心, 其功能包括影片管理和播放, TV播放, 相片浏览, 音乐播放. 因为不基于任何发行版, 所以OpenELEC的硬件驱动并不完整, 其优点在于提供了完整的管理界面, 普通用户完全可以通过界面管理系统而不需要使用命令行.

### OSMC

官网地址 <https://osmc.tv/> OSMC 是一个基于Debian发行版的Kodi运行环境. 因为其基于Debian, 所以软件资源相当丰富. 相对应的, 运行OSMC需要的硬件要求相对LibreELEC要高. OSMC跟EmuELEC其实没什么关系, 但是既然都提到这么多了, 也顺带介绍一下.

### EmuELEC

Github地址 <https://github.com/EmuELEC/EmuELEC>
终于介绍到主角了. EmuELEC基于CoreELEC和Lakka, 专注于在Amlogic芯片方案上运行的游戏模拟器, 主要是RetroArch, 附带一些PSP这类游戏的独立模拟器, 界面基于EmulationStation, 在游戏中可以调出RetroArch界面. EmuELEC相当于树莓派上RetroPie的Amlogic版. EmuELEC以前叫SX05RE, 从版本2.5开始, 改名为emuELEC, 专注于游戏功能, 不再集成Kodi. 常用的WiFi设置, 蓝牙设置等功能已经集成到主界面, 不需要通过Kodi来设置.
