---
title: kde config
author: "-"
date: 2019-04-07T03:31:52+00:00
url: kde/config
categories:
  - Desktop
tags:
  - reprint
---
## kde config

### 快捷键

|功能|key|
|-|-|
|krunner|alt+space|

### 快捷键设置

System Settings>shortcuts

## 多显示器 任务栏

<https://superuser.com/questions/905591/kde-taskbar-task-manager-only-on-vga-screen-not-dvi-screen/906725>
  
Right-click on the panel -> Panel Settings then drag the Screen Edge bar to the bottom of the screen to move the panel. Then right click on the panel -> Add Widgets -> Double-click on Task Manager. Then right-click somewhere near the middle of the panel -> Task Manager Settings -> Only show tasks from the current screen

### Baloo

为了在 Plasma 桌面上使用 Baloo 进行搜索，启动 krunner  (默认快捷键 ALT+F2) 并键入查询。若要在 Dophin (文件管理器) 内搜索，按CTRL+F。

balooctl stop   #停止 baloo
balooctl disable  #禁用baloo
balooctl status  #查看baloo的状态

编辑 ~/.config/baloofilerc

<https://community.kde.org/Baloo/Configuration>

---

## 任务栏

用 task manager widget 替换 icon only task manager widget

icon only task manager widget 任务栏只显示图标，同一个应用打开了多个窗口时不能区分不同的窗口。

task manager widget 会在任务栏上显示 window title
