---
title: nodejs basic
author: "-"
date: 2025-12-05T16:30:00+08:00
url: /?p=13672
categories:
  - Inbox
tags:
  - reprint
  - remix
  - AI-assisted
---
## nodejs basic

## version

- current v14.21.3
- latest v21.6.2

## Node.js 版本管理工具对比

### nvm vs fnm

| 特性 | nvm | fnm |
|------|-----|-----|
| **性能** | 较慢 (shell 脚本) | 快速 (Rust 编写) |
| **启动时间** | 明显延迟 (每次启动 shell) | 几乎无延迟 |
| **自动切换** | 需手动配置 hook | 内置支持 `--use-on-cd` |
| **配置文件** | `.nvmrc` | `.nvmrc` 或 `.node-version` |
| **跨平台** | macOS/Linux | macOS/Linux/Windows |
| **Windows 支持** | 需要 nvm-windows (独立项目) | 原生支持 |
| **项目隔离** | 支持 (通过 .nvmrc) | 支持 (自动检测) |
| **安装速度** | 较慢 | 快速 |
| **内存占用** | 较高 | 较低 |
| **成熟度** | 非常成熟 (2010年) | 较新 (2019年) |
| **社区** | 庞大 | 增长中 |

**推荐场景:**
- **使用 nvm**: 需要最成熟稳定的方案,或团队已在使用
- **使用 fnm**: 追求性能,需要 Windows 支持,或新项目

## nvm, Node Version Manager

[https://github.com/nvm-sh/nvm](https://github.com/nvm-sh/nvm)

```bash
# macos install nvm
brew install nvm

# ubuntu 24.04 install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash

# archlinux
pacman -S nvm

# Due to the way nvm is designed, you have to source it before you can use it:
source /usr/share/nvm/init-nvm.sh
echo 'source /usr/share/nvm/init-nvm.sh' >> ~/.zshrc

# 列出远程 Node.js 版本
nvm ls-remote
nvm install --lts
nvm install 16
nvm use 14
nvm list-remote --lts

# 项目级版本管理 - 创建 .nvmrc 文件
echo "16.20.0" > .nvmrc
nvm use  # 读取 .nvmrc 自动切换

# 配置自动切换 (添加到 ~/.zshrc)
autoload -U add-zsh-hook
load-nvmrc() {
  local node_version="$(nvm version)"
  local nvmrc_path="$(nvm_find_nvmrc)"

  if [ -n "$nvmrc_path" ]; then
    local nvmrc_node_version=$(nvm version "$(cat "${nvmrc_path}")")

    if [ "$nvmrc_node_version" = "N/A" ]; then
      nvm install
    elif [ "$nvmrc_node_version" != "$node_version" ]; then
      nvm use
    fi
  elif [ "$node_version" != "$(nvm version default)" ]; then
    echo "Reverting to nvm default version"
    nvm use default
  fi
}
add-zsh-hook chpwd load-nvmrc
load-nvmrc

```

### ubuntu install nvm

```Bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
nmv install 16
```

## fnm (Fast Node Manager)

[https://github.com/Schniz/fnm](https://github.com/Schniz/fnm)

fnm 是用 Rust 编写的快速 Node.js 版本管理器,比 nvm 性能更好,支持自动项目级版本切换。

```bash
# 安装 fnm
# macOS
brew install fnm

# Linux (通用)
curl -fsSL https://fnm.vercel.app/install | bash

# Arch Linux
pacman -S fnm

# 配置 shell (添加到 ~/.zshrc)
eval "$(fnm env --use-on-cd)"

# 基本使用
fnm list-remote          # 列出可用版本
fnm install 16.20.0      # 安装指定版本
fnm install --lts        # 安装 LTS 版本
fnm use 16.20.0          # 切换版本
fnm list                 # 列出已安装版本
fnm default 16.20.0      # 设置默认版本

# 项目级版本管理
# 在项目根目录创建 .node-version 或 .nvmrc
echo "16.20.0" > .node-version

# 配置了 --use-on-cd 后,cd 进入目录会自动切换
cd your-project  # 自动切换到 16.20.0

# 如果版本未安装,先安装
fnm install

# 卸载版本
fnm uninstall 14.0.0
```

### fnm 优势

1. **极快的性能** - Rust 编写,启动几乎无延迟
2. **自动切换** - `--use-on-cd` 自动检测项目配置
3. **跨平台** - 原生支持 Windows/macOS/Linux
4. **兼容 nvm** - 支持 `.nvmrc` 文件
5. **零配置** - 开箱即用的项目隔离

## nodejs downgrade

no need to downgrade, use nvm

```bash
npm install -g n
n 17.9.1
# close and reopen new terminal
node -v
```

### js nodejs npm 的关系

- 前端Javascript与Nodejs的异同
- nodeJs和JavaScript的异同
- nodejs和npm关系

前端的JavaScript其实是由ECMAScript、DOM、BOM组合而成。

#### JavaScript

- ECMAScript(语言基础,如: 语法、数据类型结构以及一些内置对象)
- DOM (一些操作页面元素的方法)
- BOM (一些操作浏览器的方法)
上面是JavaScript的组成部分,那么Nodejs呢？

#### Nodejs

- ECMAScript(语言基础,如: 语法、数据类型结构以及一些内置对象)
- os(操作系统)
- file(文件系统)
- net(网络系统)
- database(数据库)
分析: 很容易看出,前端和后端的js相同点就是,他们的语言基础都是ECMAScript,只是他们所扩展的东西不同,前端需要操作页面元素,于是扩展了DOM,也需要操作浏览器,于是就扩展了BOM。而服务端的js则也是基于ECMAScript扩展出了服务端所需要的一些API,稍微了解后台的童鞋肯定知道,后台语音有操作系统的能力,于是扩展os,需要有操作文件的能力,于是扩展出file文件系统、需要操作网络,于是扩展出net网络系统,需要操作数据,于是要扩展出database的能力。

#### 总结

其实npm是nodejs的包管理器 (package manager) 。
something like java and maven...
我们在node.js上开发时,会用到很多别人已经写好的javascript代码,如果每当我们需要别人的代码时,都根据名字搜索一下,下载源码,解压,再使用,会非常麻烦。于是就出现了包管理器npm。大家把自己写好的源码上传到npm官网上,如果要用某个或某些个,直接通过npm安装就可以了,不用管那个源码在哪里。并且如果我们要使用模块A,而模块A又依赖模块B,模块B又依赖模块C和D,此时npm会根据依赖关系,把所有依赖的包都下载下来并且管理起来。试想如果这些工作全靠我们自己去完成会多么麻烦

npm 本来是 Node.js 的包管理工具,但随着 JS 这几年的蓬勃发展,现在的 npm 已经成了几乎所有跟 JS 相关的工具和软件包的管理工具了,并且还在不断发展完善中。

### install nodejs

#### archlinux

```bash
pacman -S nodejs
```

#### debian/ubuntu

[https://github.com/nodesource/distributions/blob/master/README.md#debinstall](https://github.com/nodesource/distributions/blob/master/README.md#debinstall)  

```bash
    curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash -
    sudo apt-get install -y nodejs
    sudo apt-get install gcc g++ make
    # install yarn 
    curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
    echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
    sudo apt-get update && sudo apt-get install yarn
```

- windows

```bash
    choco install nodejs-lts
```

### list version

```bash
node -v
```

作者: 合肥懒皮
链接: [https://www.jianshu.com/p/857ef827fbd4](https://www.jianshu.com/p/857ef827fbd4)
来源: 简书
著作权归作者所有。商业转载请联系作者获得授权,非商业转载请注明出处。

[http://www.alloyteam.com/2016/03/master-npm/](http://www.alloyteam.com/2016/03/master-npm/)

## 用 node 运行 js

```bash
node foo.js
```
