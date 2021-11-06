---
title: "joplin"
author: "-"
date: ""
url: ""
categories:
  - inbox
tags:
  - inbox
---
## "joplin"

### archlinux install joplin
    yay -S joplin-desktop
#### direct install
    wget -O - https://raw.githubusercontent.com/laurent22/joplin/dev/Joplin_install_and_update.sh | bash
### vscode install joplin plugin
    安装 chrome 扩展: Joplin Web Clipper

### enable web clipper service
    joplin desktop > setting>web clipper > enable web clipper service

### vscode
打开vscode setting 搜索joplin, 填写 
#### joplin: Port
web clipper 端口， 
#### jplin路径 ，
 token，
  重启vscode 

## typora
打开Joplin，然后点击菜单栏的工具，在弹出的菜单中选择选项

Tools>Options>General>Text editor command>Path
填写typora 可执行文件的位置。
