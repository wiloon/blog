---
title: macOS Basics
author: "-"
date: 2012-11-20T01:19:09+00:00
url: /?p=4723
categories:
  - Inbox
tags:
  - reprint
---
## macOS Basic

```bash
brew install maven
diskutil list
```

## 快捷键

- 截屏: Command + Shift + 3
- 显示隐藏文件: Command + Shift + .
- 将光标移动到行首：control + a
- 将光标移动到行尾：control + e
- 清除屏幕：control + l
- 搜索以前使用命令：control + r
- 清除当前行：control + u
- 清除至当前行尾：control + k
- 单词为单位移动：option + 方向键

## terimnal 快捷键

Ctrl + d        删除一个字符，相当于通常的Delete键（命令行若无所有字符，则相当于exit；处理多行标准输入时也表示eof）
Ctrl + h        退格删除一个字符，相当于通常的Backspace键
Ctrl + u        删除光标之前到行首的字符
Ctrl + k        删除光标之前到行尾的字符
Ctrl + c        取消当前行输入的命令，相当于Ctrl + Break
Ctrl + a        光标移动到行首（Ahead of line），相当于通常的Home键
Ctrl + e        光标移动到行尾（End of line）
Ctrl + f        光标向前(Forward)移动一个字符位置
Ctrl + b        光标往回(Backward)移动一个字符位置
Ctrl + l        清屏，相当于执行clear命令
Ctrl + p        调出命令历史中的前一条（Previous）命令，相当于通常的上箭头
Ctrl + n        调出命令历史中的下一条（Next）命令，相当于通常的上箭头
Ctrl + r        显示：号提示，根据用户输入查找相关历史命令（reverse-i-search）
Ctrl + w        删除从光标位置前到当前所处单词（Word）的开头
Ctrl + y        粘贴最后一次被删除的单词

## .DS_Store

.DS_Store [英文全称 **Desktop Services Store**](1) 是一种由苹果公司的 Mac OS X 操作系统所创造的隐藏文件, 目的在于存贮文件夹的自定义属性,例如文件们的图标位置或者是背景色的选择。

## 重启 ipad

音量加 音量减 长按电源键直到重启

## brew

- brew 会把软件安装在用户主目录里, 不需要 sudo
- brew 装的主要是 command line tool。
- brew cask装的大多是有gui界面的app以及驱动，brew cask是brew的一个官方源。

[https://brew.sh/](https://brew.sh/)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install ansible
brew list ansible

# 更新自己
brew update

# 查看所有需要更新的包
brew outdated

# 更新某一个包
brew upgrade package0

# 更新所有包
brew upgrade

brew install --cask obsidian
```

### all casks packages

[https://formulae.brew.sh/cask/](https://formulae.brew.sh/cask/)