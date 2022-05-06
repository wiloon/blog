---
author: "-"
date: "2020-06-27T04:11:36Z"
title: "chrome basic"
categories:
  - chrome
tags:
  - reprint
---
## "chrome basic"

### 不使用页面缓存进行刷新

    Shift+F5

### 清除dns缓存

    chrome://net-internals/#dns

### chrome://flags

### chrome 导出 netlogs

    chrome://net-export/

### 分析 netlogs

    https://netlog-viewer.appspot.com/

## Chrome 清除某个特定网站下的缓存

<https://www.cnblogs.com/Chesky/p/chrome_disabling_cache.html>

打开开发者工具 (F12), 选择 Network——Disable cache 即可。需要清除某网站缓存时 F12 打开开发者工具就会自动清除这个网站的缓存,而不必清除所有网站的缓存了。

## huge CPU usage of gnome-keyring-daemon when starting Google Chrome

    google-chrome --password-store:basic

How to prevent the huge CPU usage of gnome-keyring-daemon when starting Google Chrome
  
<https://www.andreafortuna.org/technology/linux/how-to-prevent-the-huge-cpu-usage-of-gnome-keyring-daemon-when-starting-google-chrome/embed/#?secret=NSkQcrRM22>
