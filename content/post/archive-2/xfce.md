---
title: xfce
author: "-"
date: 2022-07-12 17:33:53
url: xfce
categories:
  - Linux
tags:
  - reprint
---
## xfce

## disable taskbar items grouping

Right click on the taskbar, select Panel -> Panel Preferences
Select the Items tab , select Window Buttons in the list, click the Edit button on the right side
Change Window grouping to Never

## xfce 快捷键

```bash
ctrl+F1    #切换工作区
```

列出已经配置的快捷键

```bash
xfconf-query -c xfce4-keyboard-shortcuts -l -v|grep thunar
```

修改

Applications> Settings> keyboard> application shortcuts

## passwordless login, xfce 免密码登录

<https://wiki.archlinux.org/title/LightDM#Enabling_interactive_passwordless_login>

<https://github.com/sgerrand/xfce4-terminal-colors-solarized>
  
/home/user0/.config/xfce4/terminal/terminalrc

```bash
colorCursor=#93a1a1
ColorForeground=#839496
ColorBackground=#002b36
ColorPalette=#073642;#dc322f;#859900;#b58900;#268bd2;#d33682;#2aa198;#eee8d5;#002b36;#cb4b16;#586e75;#657b83;#839496;#6c71c4;#93a1a1;#fdf6e3
```

<https://ethanschoonover.com/solarized/>
  
<https://github.com/altercation/solarized>

## archlinux 登录后启动xfce4

<https://wiki.archlinux.org/index.php/xinitrc>

```bash
vim  ~/.xinitrc
exec startxfce4

vim .bashrc
# change the last line to
# add as last line in .bashrc
[[ -z $DISPLAY && $XDG_VTNR -eq 1 ]] && exec startx
```
