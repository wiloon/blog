---
title: chrome os, crostini, 开发环境
author: "-"
date: 2020-02-17T05:36:02+00:00
url: /?p=15562
categories:
  - chrome
tags:
  - reprint
---
## chrome os, crostini, 开发环境
crostini 的Debian 对snap 支持不全， 不能使用snap 应用

### terminal

https://snugug.com/musings/developing-on-chrome-os/

### terminal, tilix

crostini默认的terminal在使用oh my zsh时，光标显示不正常。
  
安装tilix,从chromeos启动tilix使用terminal

```bash
sudo pacman -S tilix
# 在chromeos中启动tilix使用shell
```

### 或者使用Secure Shell App

### idea 慢的问题

File->Settings->Plugins.
  
Click marketplace, search for "Choose Runtime"
Install official Choose Runtime addon from JetBrains
Wait for install and click to restart IDE.
Once back in project, press shift twice to open the search window
Search for Runtime. Select "Choose Runtime"
Change to "jbrsdk-8u-232-linux-x64-b1638.6.tar.gz", which should be the very last one at the bottom of the list.
  
Click install, restart IDE, enjoy!

https://www.reddit.com/r/Crostini/comments/e67tij/pycharmwebstormjetbrains_ide_fix/
  
https://github.com/gnunn1/tilix
  
https://www.reddit.com/r/Crostini/comments/8gku8y/psa_you_can_install_a_better_terminal_emulator/