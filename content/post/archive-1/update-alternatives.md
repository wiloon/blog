---
title: update-alternatives
author: "-"
date: 2012-12-07T14:26:28+00:00
url: /?p=4844
categories:
  - Linux
tags:
  - reprint
---
## update-alternatives
update-alternatives是dpkg的实用工具，用来维护系统命令的符号链接，以决定系统默认使用什么命令。在Debian系统中，我们可能会同时安装有很多功能类似的程序和可选配置，如Web浏览器程序(firefox，konqueror)、窗口管理器(wmaker、metacity)和鼠标的不同主题等。这样，用户在使用系统时就可进行选择，以满足自已的需求。但对于普通用户来说，在这些程序间进行选择配置会较困难。update-alternatives工具就是为了解决这个问题，帮助用户能方便地选择自已喜欢程序和配置系统功能。