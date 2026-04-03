---
title: Shell 创建文件并写入内容
author: "-"
date: 2026-04-03T12:30:02+08:00
url: shell-create-file-write
categories:
  - shell
tags:
  - reprint
  - remix
  - AI-assisted
---

## 选型总结

| 场景 | 推荐方式 |
|---|---|
| 单行字符串 | `printf '%s\n' "..." > file` |
| 多行内容 | `cat > file << 'EOF' ... EOF` |
| 追加内容 | `>> file` |
| 需要 root 写入 | `echo "..." \| sudo tee file` |
| 脚本内变量展开 | heredoc 不加引号：`<< EOF` |
| 禁止变量展开 | heredoc 加单引号：`<< 'EOF'` |

## 单行字符串：推荐 `printf`

```bash
printf '%s\n' 'Hello, World!' > foo.txt
```

### printf 简介

`printf` 在 Linux/Unix 系统上普遍可用，有两种形式：

- **内建命令**（built-in）：bash、zsh、dash 等 shell 均内置，不依赖外部程序
- **外部命令**：`/usr/bin/printf`，由 `coreutils` 包提供，几乎所有发行版默认安装

`printf` 的作用是格式化输出，语法来自 C 语言的 `printf()`：

```bash
printf FORMAT [ARGUMENTS...]
```

常用格式占位符：

| 占位符 | 含义 |
|---|---|
| `%s` | 字符串 |
| `%d` | 整数 |
| `%f` | 浮点数 |
| `\n` | 换行 |
| `\t` | Tab |

`echo` 在 bash 里需要加 `-e` 才能解析 `\n`，而 sh/dash 的 `echo` 行为又不同，跨 shell 不可靠；`printf` 行为在所有 shell 里一致，脚本中优先使用 `printf`。

### 引号选择

字符串内容用**单引号**包裹：在交互式 shell（zsh/bash）中，双引号内的 `!` 会触发历史展开（history expansion），导致引号未闭合、shell 进入等待状态（`dquote>`）。没有变量展开需求时，用单引号可以避免这个问题。

## 多行内容：推荐 heredoc

```bash
cat > file.txt << 'EOF'
Hello, World!
Line 2
$PWD 会原样保留，不展开
EOF
```

heredoc（here document）的优势是写在脚本里的格式与写入文件的格式完全一致，不需要手动处理换行。

### 单引号与双引号的区别

heredoc 起始标识符加单引号 `'EOF'`，禁止变量展开，内容原样写入：

```bash
cat > file.txt << 'EOF'
Your working directory is $PWD.
EOF
# 文件内容：Your working directory is $PWD.
```

不加引号 `EOF`，`$VAR`、`$(cmd)` 会被 shell 展开：

```bash
cat > file.txt << EOF
Your working directory is $PWD.
EOF
# 文件内容：Your working directory is /home/user
```

同理，`echo` 也遵循相同规则：

```bash
echo 'Your working directory is $PWD.' >> file.txt   # $PWD 不展开
echo "Your working directory is $PWD."  >> file.txt  # $PWD 展开
```

## 追加内容

```bash
printf '%s\n' "new line" >> file.txt
```

`>` 覆盖写入，`>>` 追加写入。

## 需要 sudo 权限写入：用 `tee`

直接用 `sudo echo > /etc/file` 因为重定向在 sudo 提权前就已解析，会导致权限错误。正确做法是用 `tee`：

```bash
# 覆盖写入
echo "content" | sudo tee /etc/config.conf > /dev/null

# 追加写入
echo "content" | sudo tee -a /etc/config.conf > /dev/null

# 多行内容
sudo tee /etc/config.conf > /dev/null << 'EOF'
[setting]
key = value
EOF
```

`> /dev/null` 是为了抑制 `tee` 同时输出到终端的内容。

## 参考

- [https://blog.shengbin.me/posts/create-text-file-in-shell-scripts](https://blog.shengbin.me/posts/create-text-file-in-shell-scripts)
