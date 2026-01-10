---
title: macOS Basics
author: "-"
date: 2026-01-10T20:30:00+08:00
url: macos/basic
categories:
  - Inbox
tags:
  - reprint
  - remix
  - AI-assisted
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

.DS_Store Desktop Services Store 是一种由苹果公司的 Mac OS X 操作系统所创造的隐藏文件, 目的在于存贮文件夹的自定义属性,
例如文件们的图标位置或者是背景色的选择。

## 重启 ipad

音量加 音量减 长按电源键直到重启

## brew

https://brew.sh/

- brew 会把软件安装在用户主目录里, 不需要 sudo
- brew 装的主要是 command line tool。
- brew cask 装的大多是有 gui 界面的 app 以及驱动，brew cask 是 brew 的一个官方源。

```bash
# 搜索
brew search foo
brew search golang

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install ansible

# uninstall package
brew uninstall packageName
brew list ansible

# 看看有哪些过期的包
brew update

# 查看所有需要更新的包
brew outdated

# 更新某一个包
brew upgrade package0

# 更新所有包
brew upgrade

brew install --cask obsidian

brew config
brew doctor
```

### brew update install 慢

网络问题, 换国内的源

```Bash

# 步骤一
cd "$(brew --repo)"
# 查看源
git remote -v
# 更新源
git remote set-url origin https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/brew.git

# 步骤二
cd "$(brew --repo)/Library/Taps/homebrew/homebrew-core"
git remote set-url origin https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/homebrew-core.git

#步骤三
brew update
```

恢复默认源

```Bash
cd "$(brew --repo)"
git remote set-url origin https://github.com/Homebrew/brew.git
 
cd "$(brew --repo)/Library/Taps/homebrew/homebrew-core"
git remote set-url origin https://github.com/Homebrew/homebrew-core
 
brew update
```

### all casks package

[https://formulae.brew.sh/cask/](https://formulae.brew.sh/cask/)

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
