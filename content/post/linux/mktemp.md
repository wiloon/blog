---
title: "mktemp: 安全创建临时文件与目录"
author: "-"
date: 2026-08-27T09:19:02+08:00
lastmod: 2026-08-27T09:19:02+08:00
url: mktemp
categories:
  - Linux
tags:
  - shell
  - coreutils
  - remix
  - AI-assisted
---

## mktemp

`mktemp` 用来**安全地**创建临时文件或临时目录，并把路径打印到标准输出。名字里带随机段，避免多个进程同时写死 `/tmp/foo` 时互相踩踏或被抢占。

脚本里需要临时落盘时，优先用 `mktemp`，不要手写固定路径。

### 基本用法

不传参数时，默认在 `$TMPDIR`（未设置则为 `/tmp`）下创建文件，模板类似 `tmp.XXXXXXXXXX`：

```bash
tmp=$(mktemp)
echo "path=$tmp"
echo hello > "$tmp"
rm -f "$tmp"
```

输出示例：

```text
/tmp/tmp.aB3kX9pQ2r
```

### 自定义模板

模板最后一个路径分量里至少要有 **3 个连续的 `X`**，`X` 会被替换成随机字符：

```bash
# file under /tmp
f=$(mktemp /tmp/myapp.XXXXXX)
# with suffix
f=$(mktemp --suffix=.log /tmp/myapp.XXXXXX)
```

### 创建临时目录

`-d` / `--directory` 创建目录而不是文件：

```bash
workdir=$(mktemp -d)
# or
workdir=$(mktemp -d /tmp/build.XXXXXX)
```

权限：文件一般为 `u+rw`，目录一般为 `u+rwx`（再受 umask 约束）。

### 指定父目录

`-p DIR` / `--tmpdir[=DIR]`：相对某个目录解释模板。未写 `DIR` 时用 `$TMPDIR`，再否则 `/tmp`：

```bash
f=$(mktemp -p /var/tmp myapp.XXXXXX)
d=$(mktemp -d --tmpdir="$HOME/tmp" work.XXXXXX)
```

### 脚本里的常见写法

创建后记得清理。可用 `trap` 在退出时删除：

```bash
#!/usr/bin/env bash
set -euo pipefail

tmp=$(mktemp)
trap 'rm -f "$tmp"' EXIT

printf 'data\n' > "$tmp"
# ... use "$tmp"
```

临时目录同理：

```bash
workdir=$(mktemp -d)
trap 'rm -rf "$workdir"' EXIT
```

### 注意

| 选项 | 说明 |
| ---- | ---- |
| `-u` / `--dry-run` | 只打印名字、不创建实体，存在竞态，一般不要用 |
| `-q` / `--quiet` | 创建失败时少打诊断信息 |
| `-t` | 旧用法，已废弃，改用 `-p` / `--tmpdir` |

GNU coreutils 文档：`info '(coreutils) mktemp invocation'` 或 [mktemp invocation](https://www.gnu.org/software/coreutils/manual/html_node/mktemp-invocation.html)。
