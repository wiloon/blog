---
title: chrome command
author: "-"
date: 2022-01-22 20:05:13
url: /?p=11277
categories:
  - chrome
tags:
  - reprint
---
## chrome command

```bash
# linux 启动浏览器并打开 URL
google-chrome-beta gmail.com
google-chrome-beta http://localhost:8080
```

<https://stackoverflow.com/questions/28162697/how-can-i-open-google-chrome-from-the-terminal-with-the-url-localhost3000>

Chrome 有很多的特性在界面菜单中是没有体现的,你可以通过 chrome:// 命令来访问。本文介绍 12 个非常有用的 chrome:// 命令:

  1. chrome://flags

可用来启用或者关闭某些 chrome 的体验特性

  1. chrome://dns

该命令将显示浏览器预抓取的主机名列表

  1. chrome://downloads

该命令同时也可以从菜单中的下载来访问,其快捷键是 Ctrl + J

  1. chrome://extensions

该命令等同于菜单 - 工具 - 扩展

  1. chrome://bookmarks

改名了等同于菜单-书签-书签管理器,快捷键 Ctrl+Shift+O

  1. chrome://history

该命令可从菜单-历史直接访问,快捷键 Ctrl+H

  1. chrome://memory

该命令将重定向到 "chrome://memory-redirect/". 它将显示浏览器使用内存的情况,以及系统中运行的其他浏览器,包括 firefox。同时还显示浏览器进程的详细信息。

  1. chrome://net-internals

该命令显示网络相关信息,用来捕获浏览器生成的网络事件,可导出数据,可查看DNS主机解析缓存。

其中一个很重要的功能就是"测试",如果你无法访问某个网址,那么可以使用 "chrome://net-internals" -> 点击"Tests" tab -> 输入网址,并点击开始测试,Chrome 将报告具体的问题所在。

  1. chrome://quota-internals

该命令用来显示浏览器所使用磁盘空间配额的情况。

  1. chrome://sessions

该命令用来显示当前运行的浏览器的会话信息数以及详细列表

  1. chrome://settings

该命令可通过菜单-选项直接访问,可用来控制浏览器各项设置值

  1. chrome://sync-internals

用来显示 chrome 的同步状态

最后,如果你想查看 chrome 所有的命令,可使用 chrome://about/

另外,请注意,上面提及的所有命令也可使用 about:xxx 命令,将会自动重定向到 chrome://,例如:

about:dns
  
chrome://dns
