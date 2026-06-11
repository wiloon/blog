---
title: macOS Basics
author: "-"
date: 2026-01-10T20:30:00+08:00
lastmod: 2026-06-11T11:18:29+08:00
url: macos/basic
categories:
  - Inbox
tags:
  - remix
  - AI-assisted
aliases:
  - /p4723/
---
## macOS Basic

```bash
# uninstal
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/uninstall.sh)"
# install
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

brew install maven
diskutil list
```

## 快捷键

- 截屏: Command + Shift + 3
- 显示/隐藏 Dock: Option + Command + D
- 显示隐藏文件: Command + Shift + .
- 将光标移动到行首：control + a
- 将光标移动到行尾：control + e
- 清除屏幕：control + l
- 搜索以前使用命令：control + r
- 清除当前行：control + u
- 清除至当前行尾：control + k
- 单词为单位移动：option + 方向键

## 锁屏

- Touch ID：带有 Touch ID 的 MacBook 或妙控键盘，轻按指纹识别键即可瞬间锁屏，比快捷键更快速。
- `Command (⌘) + Control (⌃) + Q`：立即锁定屏幕。

## 窗口切换

macOS 的设计逻辑：`Command + Tab` 是在**应用程序**之间切换，而不是在**窗口**之间切换。

- `Command (⌘) + ~`：切换同一应用程序的多个窗口（~ 是 Tab 键上方的波浪号键）。

### 调度中心 (Mission Control)

一眼看到所有打开的窗口并选择：

- 触控板：三指（或四指）向上轻扫。

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

.DS_Store Desktop Services Store 是一种由苹果公司的 Mac OS X 操作系统所创造的隐藏文件, 目的在于存贮文件夹的自定义属性,
例如文件们的图标位置或者是背景色的选择。

## 重启 ipad

音量加 音量减 长按电源键直到重启

## brew

详见 [brew 使用指南](../macos/brew.md)。

## macos build linux bin

https://www.baifachuan.com/posts/4862a3b1.html

linux_syscall.c:67:13: error: call to undeclared function 'setresgid'; ISO C99 and later do not support implicit function declarations [-Wimplicit-function-declaration]

```Bash
brew install FiloSottile/musl-cross/musl-cross
CGO_ENABLED=1 GOOS=linux GOARCH=amd64 CC=x86_64-linux-musl-gcc  CXX=x86_64-linux-musl-g++  go build -o ${package_name} enx-api.go
```

## sudo 免密码配置

### 方法：创建单独的配置文件（推荐）

1. 创建新文件：

```bash
sudo visudo -f /etc/sudoers.d/nopasswd
```

2. 添加内容（将 `your_username` 替换为你的用户名）：

```
your_username ALL=(ALL) NOPASSWD: ALL
```

3. 保存退出（按 `Esc` 然后输入 `:wq` 回车）

### 验证配置

执行任意 sudo 命令测试：

```bash
sudo echo "test"
```

如果不再要求输入密码，说明配置成功。

### 安全建议

- **针对特定命令免密**：如果只需要某个命令免密，可以使用：
  ```
  your_username ALL=(ALL) NOPASSWD: /usr/bin/nerdctl
  ```
- **生产环境慎用**：完全免密配置会降低系统安全性，建议仅在开发环境使用
- **检查用户名**：确保用户名拼写正确，错误配置可能导致无法使用 sudo
