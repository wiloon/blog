---
author: "-"
date: "2021-01-01 23:23:06" 
title: "rust basic"
categories:
  - inbox
tags:
  - reprint
---
## "rust basic"

Rust 是一种 预编译静态类型（ahead-of-time compiled）语言

## Rustup Rust 的工具链管理器

Rustup 是一个命令行应用，能够下载并在不同版本的 Rust 工具链中进行切换 —— 如编译器 rustc 和标准库，该应用所支持的平台数量不少。事实上，rustc 本身就支持大约 56 个平台，而 rustup 实际上能够为其中14个平台管理编译器，为30个平台管理标准库。

Rust 1.8 中引入的 Rustup，是一个针对 Rust 语言的工具链管理器（toolchain manager），其目标是让交叉编译 Rust 代码更加简单。Mozilla 工程师 Brian Anderson 近期与我们分享了关于此的更多细节。

此外，rustup 能够追踪工具链的具体版本，包括 Rust 的 nightly 版本、beta 版本和发行版本。举个例子，你可以用 rustup 检查程序在下一个 Rust 发行版下的行为。但是之前，你需要安装当前平台下的 Rust beta 版本的工具链，然后利用该工具链运行单元测试。使用 rustup 之后，可以通过执行类似下面的代码完成：

$ rustup install beta
$ rustup run beta cargo test
再举一个例子，Anderson 介绍了如何使用 rustup 为使用 musl 标准库（而非大家常用的glibc标准库）的 Linux 版本创建静态二进制文件：

$ rustup target add x86_64-unknown-linux-musl
$ cargo run --target=x86_64-unknown-linux-musl
Features
管理安装多个官方版本的 Rust 二进制程序。
配置基于目录的 Rust 工具链。
安装和更新来自 Rust 的发布通道: nightly, beta 和 stable。
接收来自发布通道更新的通知。
从官方安装历史版本的 nightly 工具链。
通过指定 stable 版本来安装。
安装额外的 std 用于交叉编译。
安装自定义的工具链。
独立每个安装的 Cargo metadata。
校验下载的 hash 值。
校验签名 (如果 GPG 存在)。
断点续传。
只依赖 bash, curl 和常见 unix 工具。
支持 Linux, OS X, Windows(via MSYS2)。
cmd
rustup -h
使用 rust help <command> 来查看子命令的帮助。
rustup doc --book 会打开英文版的 The Rust Programming Language。

常用命令

```Bash
# 显示当前安装的工具链信息。
rustup show
# 检查安装更新。
rustup update
```

rustup default <toolchain> 配置默认工具链。

rustup toolchain [SUBCOMMAND] 配置工具链

rustup toolchain install <toolchain> 安装工具链。
rustup toolchain uninstall <toolchain> 卸载工具链。
rustup toolchain link <toolchain-name> "<toolchain-path>" 设置自定义工具链。

## Cargo.toml

Cargo.toml是Rust项目的配置文件，它定义了项目的元数据、依赖关系、构建选项和其他重要信息。该文件必须位于项目根目录下。

### windows install rust

```Bash
# winget
winget install Rustlang.Rustup
winget install Rustlang.Rust.MSVC
```

#### wsl, ubuntu install rust

`curl --proto '=https' --tlsv1.2 -sSf [https://sh.rustup.rs](https://sh.rustup.rs) | sh`

### archlinux install rust

rustup self update will not work when installed this way, the package needs to be updated by pacman.

```Bash
sudo pacman -S rustup
rustup default stable
```

### 查看版本

`    rustc --version`

### 更新rust 版本

`    rustup update`

### RUSTUP_HOME

`    /home/wiloon/.rustup`

### CARGO_HOME

`    /home/wiloon/.cargo`

### env

```Bash
  /home/wiloon/.profile
  /home/wiloon/.bashrc
  /home/wiloon/.zshenv
```

### commands

    rustup update
    cargo build
    cargo run
    cargo test
    cargo doc
    cargo publish
    cargo --version
    cargo new hello-rust
    cargo run

### vscode plugin rust

- rust-anlyzer (RA)
- Rust 语言服务器 (RLS)

### hello world

    cargo new hello-rust

---

[https://kaisery.github.io/trpl-zh-cn/ch01-01-installation.html](https://kaisery.github.io/trpl-zh-cn/ch01-01-installation.html)

https://kaisery.github.io/trpl-zh-cn/ch01-02-hello-world.html

## books

https://course.rs/into-rust.html

https://zh.practice.rs/why-exercise.html



