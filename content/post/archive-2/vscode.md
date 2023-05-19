---
title: vscode basic，vscode, visual studio code
author: "-"
date: 2018-09-01T03:34:42+00:00
url: vscode
categories:
  - Editor
tags:
  - reprint
  - vscode
---
## vscode basic，vscode, visual studio code

### debian install visual studio code

#### install from repo

<https://linuxize.com/post/how-to-install-visual-studio-code-on-debian-9/>

#### download deb

<https://code.visualstudio.com/>#

## vscode 列编辑

Alt+Shift+鼠标左键拖动, 选中拖动的区域内容

<https://blog.csdn.net/u011127019/article/details/74039598>

### vscode remote ssh, A> ssh> B

1. A 安装插件 "Remote - SSH"
2. 在 B 主机上配置ssh 公钥
3. 私钥放在 `C:\Users\user0\.ssh` 里
4. A, 点击 vscode左下角,选择 remote-ssh: connect to host

### 字体

打开 VSCode,Windows 下按 Ctrl + ,,macOS 下按 Cmd + ,,进入设定。在上方搜索框搜索 editor.fontFamily,在

Editor: Font Family
Controls the font family.
下方的框框填入 font-family 即可。

默认的是 Consolas, 'Courier New', monospace。

#### 改成

```r
Consolas,'Courier New','微软雅黑',monospace
```

我喜欢萍方所以就 Consolas, 'Courier New', monospace,"萍方-简"。

还可以 Consolas, 'Courier New', monospace,DengXian 和 Consolas, 'Courier New', "微软雅黑", monospace 这样。

## vscode plugin, 扩展

### JSON Tools

JSON 格式化工具, 快捷键 `ctl+alt+m`

### Filter Line

按关键字过滤

### Word Count

字数统计

### remote development

windows 编辑 wsl 文件

### markdownlint

markdown 语法检查

### Markdown All in One

```r
ctrl+shift+i - 表格格式化
ctrl+b: 粗体
命令: Format Document: 格式化表格
```

### Markdown Preview Github Styling

### REST Client

vscode 发http请求
同一个文档 中不同的请求用 "###" 分隔

### Insert Date String

插入当前日期时间

#### vscode > PlantUML - Simple Viewer

能点击图上的文字反查代码

config plant uml rander server
File> Preferences> Extensions> PlantUML config> Rander: server
File> Preferences> Extensions> PlantUML config> Server: <http://plantuml.wiloon.com>

### hexdump

hex viewer

## vscode 扩展 离线安装

- 下载 .vsix 文件
- 安装

```r
code --install-extension jsynowiec.vscode-insertdatestring-2.3.1.vsix
```

### 显示空格

打开setting, 在搜索框中输入renderControlCharacters,选中勾选框,即可显示tab.  
在搜索框中输入renderWhitespace,选择all,即可显示空格.  

### vscode + wsl 版本更新

有新版本时, vscode左下角会有提示,点击更新 windows里安装的vscode, vscode打开 wsl里的目录时,会自动更新wsl里安装的vscode.

<https://code.visualstudio.com/docs/remote/ssh-tutorial>  
<https://www.justhx.com/partly-technical/optiumise-chinese-characters-in-vscode>  
<https://blog.csdn.net/bmzk123/article/details/86501706>  

## 修改语言

按键盘上的 Ctrl+Shift+P，之后在 VScode   的顶部会弹出一个搜索框
在弹出的搜索框中输入 configure language，即可进入语言设置，选择你想要的即可。中文选择 zh-cn，英文选择 en，如果没有可以选择  install additional languages 进行下载

## vscode 快捷键

```json
{
  "key": "ctrl+,",
  "command": "workbench.action.openSettings"
},
{
  "key": "ctrl+shift+e",
  "command": "workbench.action.quickOpen"
},
{
  "key": "ctrl+`",
  "command": "workbench.action.terminal.toggleTerminal",
  "when": "terminal.active"
},
{
  "key": "ctrl+shift+p",
  "command": "workbench.action.showCommands"
},
{
  "key": "ctrl+alt+d",
  "command": "plantuml.preview"
},
{
  "key": "ctrl+shift+d",
  "command": "editor.action.duplicateSelection"
},
{
  "key": "ctrl+p",
  "command": "workbench.action.quickOpen"
}
```
