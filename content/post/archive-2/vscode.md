---
title: vscode basic， vscode, visual studio code
author: "-"
date: 2018-09-01T03:34:42+00:00
url: vscode

categories:
  - inbox
tags:
  - reprint
---
## vscode basic， vscode, visual studio code

### debian install visual studio code

#### install from repo

https://linuxize.com/post/how-to-install-visual-studio-code-on-debian-9/

#### download deb

https://code.visualstudio.com/#

### vscode 列编辑

Alt+Shift+鼠标左键拖动,选中拖动的区域内容

https://blog.csdn.net/u011127019/article/details/74039598

### remote ssh, A >ssh> B

1. A 安装插件 remote - ssh
2. 在目标linux(B)上配置ssh密钥
3. A, 点击vscode左下角,选择 remote-ssh: connect to host

### 快捷键

#### Settings

    Ctrl + ,

#### terminal

    Ctrl + `

#### 命令框,查找文件

    Ctrl + Shift + p

### 字体

打开 VSCode,Windows 下按 Ctrl + ,,macOS 下按 Cmd + ,,进入设定。在上方搜索框搜索 editor.fontFamily,在

Editor: Font Family
Controls the font family.
下方的框框填入 font-family 即可。

默认的是 Consolas, 'Courier New', monospace。

#### 改成

    Consolas,'Courier New','微软雅黑',monospace

我喜欢萍方所以就 Consolas, 'Courier New', monospace,"萍方-简"。

还可以 Consolas, 'Courier New', monospace,DengXian 和 Consolas, 'Courier New', "微软雅黑", monospace 这样。

## vscode plugin

### Filter Line

按关键字过滤

### Word Count

字数统计

### remote development

windows 编辑 wsl 文件

### markdownlint

markdown 语法检查

### Markdown All in One

    ctrl+shift+i - 表格格式化
    ctrl+b: 粗体
    命令: Format Document: 格式化表格

## vscode 扩展 离线安装

- 下载 .vsix 文件
- 安装

    code --install-extension jsynowiec.vscode-insertdatestring-2.3.1.vsix

### Settings Sync

配置同步

File> Preference> Settings Sync

### Markdown Preview Github Styling

### REST Client

vscode 发http请求
同一个文档 中不同的请求用 "###" 分隔

### Insert Date String

插入当前日期时间

#### vscode > PlantUML

config plant uml rander server
File>Preferences>Extensions>PlantUML config>Rander: server
File>Preferences>Extensions>PlantUML config>Server: http://plantuml.wiloon.com

### hexdump

hex viewer

### 显示空格
打开setting,在搜索框中输入renderControlCharacters,选中勾选框,即可显示tab.  
在搜索框中输入renderWhitespace,选择all,即可显示空格.  

### vscode + wsl 版本更新 
有新版本时, vscode左下角会有提示,点击更新 windows里安装的vscode, vscode打开 wsl里的目录时,会自动更新wsl里安装的vscode.

---

>https://code.visualstudio.com/docs/remote/ssh-tutorial  
>https://www.justhx.com/partly-technical/optiumise-chinese-characters-in-vscode  
>https://blog.csdn.net/bmzk123/article/details/86501706  

 