---
title: chezmoi
author: "-"
date: 2026-05-05T15:31:10+08:00
lastmod: 2026-07-13T12:49:50+08:00
url: chezmoi
categories:
  - Linux
tags:
  - dotfiles
  - chezmoi
  - remix
  - AI-assisted
---

chezmoi（发音近似 shay-mwah，音标 /ʃeɪ mwɑ/，法语 *chez moi*「在我家」）是一个跨平台的 dotfiles 管理工具，使用 Go 编写，支持模板、加密 secret、多机器差异配置。

## 安装

```bash
# Arch Linux
pacman -S chezmoi

# macOS
brew install chezmoi

# 通用安装脚本
sh -c "$(curl -fsLS get.chezmoi.io)"
```

## 初始化

```bash
# 初始化（本地，不关联远程仓库）
chezmoi init

# 初始化并关联远程 git 仓库（自动 clone 到 ~/.local/share/chezmoi/）
chezmoi init git@github.com:用户名/仓库名.git

# 用 GitHub 用户名简写（默认找 dotfiles 仓库）
chezmoi init <github-username>
```

`chezmoi init` 可以在**任意目录**执行，source 目录固定克隆到 `~/.local/share/chezmoi/`，不需要手动指定位置。

## 日常改配置流程

改已托管的配置时，记住三层：

1. **source**：`~/.local/share/chezmoi`（git 仓库，真相源）
1. **destination**：home 下的实际文件（如 `~/.zshrc`）
1. **远程**：source 对应的 git remote

`chezmoi edit` 只改 source，不会自动写入 home，也不会 push。完整顺序：

```bash
# 1. 编辑 source（用 $EDITOR 打开对应模板/文件）
chezmoi edit ~/.zshrc

# 2. 先看差异，再应用到本机 home
chezmoi diff
chezmoi apply
# 或只 apply 某一个目标：
# chezmoi apply ~/.zshrc
# chezmoi apply ~/.config/kitty/kitty.conf --force

# 3. 提交并推送到远程（chezmoi git 封装，任意目录可执行）
chezmoi git status
chezmoi git add .
chezmoi git -- commit -m "update zshrc"
chezmoi git push
```

也可以编辑后立刻 apply：

```bash
chezmoi edit --apply ~/.zshrc
```

`--apply` 只覆盖本机 destination，**仍然需要**后面的 `chezmoi git ... push` 才能同步到远程。

另一台机器拉取并应用：

```bash
chezmoi update   # git pull source + apply
```

没有单独的 `chezmoi push`；推远程就是 `chezmoi git push`（或 `chezmoi cd` 后普通 git）。`chezmoi update` 只负责拉远程并 apply。

## 添加文件

```bash
# 将文件纳入 chezmoi 管理
chezmoi add ~/.bashrc
chezmoi add ~/.config/nvim/init.lua

# 添加整个目录（递归）
chezmoi add ~/.config/somedir

# 添加时标记为模板
chezmoi add --template ~/.gitconfig
```

路径包含空格时加引号：

```bash
chezmoi add "/Users/wiloon/Library/Application Support/Code/User/globalStorage/github.copilot-chat/memory-tool/memories"
```

如果是先直接改了 home 里的文件，再用 `chezmoi re-add` 把变更写回 source，然后同样走上面的 commit / push。

## 查看差异

```bash
# 查看 source 与 destination 的差异
chezmoi diff
```

## 应用更改

```bash
# 将 source directory 中的变更应用到 home 目录
chezmoi apply

# 预览（不实际写入）
chezmoi apply --dry-run
```

## 编辑文件

```bash
# 直接编辑 source 中的文件（用 $EDITOR 打开）
chezmoi edit ~/.bashrc

# 编辑后立即 apply
chezmoi edit --apply ~/.bashrc
```

## 状态检查

```bash
# 查看哪些文件有变动
chezmoi status
```

## 模板

chezmoi 使用 Go 的 `text/template` 语法，可以根据机器的不同生成不同内容。

```bash
# 查看可用变量
chezmoi data
```

模板示例 `~/.local/share/chezmoi/dot_gitconfig.tmpl`：

```ini
[user]
    name = {{ .name }}
    email = {{ .email }}
{{- if eq .chezmoi.os "linux" }}
    # Linux specific config
{{- end }}
```

## 加密 secret

chezmoi 支持通过 age、gpg、gopass、1Password、Bitwarden 等管理敏感文件。

```bash
# 使用 age 加密
chezmoi add --encrypt ~/.ssh/id_rsa
```

## 路径映射机制

chezmoi 以 `~`（home 目录）为根，将所有路径转换为相对路径存入 source directory。规则：

| 原始路径 | source directory 里的路径 |
| ---- | ---- |
| `~/.bashrc` | `dot_bashrc` |
| `~/.agents/skills/` | `dot_agents/skills/` |
| `~/Library/Application Support/foo/` | `Library/Application Support/foo/` |

换机器时，chezmoi 会把 source 里的路径展开到新机器的 `~` 下，路径完全一致。如果目标目录不存在，`chezmoi apply` 会自动创建。

## 同步到新机器

```bash
# 从远程仓库初始化并 apply（一步完成）
chezmoi init --apply git@github.com:用户名/仓库名.git

# 或分两步
chezmoi init git@github.com:用户名/仓库名.git
chezmoi apply
```

## 推送到远程仓库

chezmoi 封装了 git 命令，可在**任意目录**执行，等价于在 `~/.local/share/chezmoi` 里跑 git：

```bash
chezmoi git add .
chezmoi git -- commit -m "update dotfiles"
chezmoi git push
```

注意：`chezmoi git commit -m` 会报错，因为 `-m` 被 chezmoi 自身解析。需要用 `--` 隔开：

```bash
# wrong: -m is parsed by chezmoi
chezmoi git commit -m "message"

# correct
chezmoi git -- commit -m "message"
```

也可以 `chezmoi cd` 进入 source 目录后再用普通 git。

## 更新已追踪的文件

本地 destination 有变化后，重新同步到 source 目录：

```bash
chezmoi re-add
```

## 常用目录和文件

| 路径 | 说明 |
| ---- | ---- |
| `~/.local/share/chezmoi` | source directory，存放托管文件 |
| `~/.config/chezmoi/chezmoi.toml` | 配置文件 |

## 文件命名规则

chezmoi 用前缀约定来描述目标文件的属性：

| 前缀 | 含义 |
| ---- | ---- |
| `dot_` | 对应目标中的 `.`（隐藏文件） |
| `private_` | 权限 `0600` |
| `executable_` | 权限 `0755` |
| `.tmpl` 后缀 | 模板文件 |

## chezmoi 与 git 的区别

git 只负责版本控制和同步，chezmoi 在 apply 阶段提供了一整套转换管道：

| 功能 | 说明 |
| ---- | ---- |
| 模板渲染 | apply 时把 `.tmpl` 文件渲染成最终内容，不同机器生成不同结果 |
| 加密/解密 | source 存加密文件，apply 时自动解密写入目标路径 |
| 文件属性管理 | 通过 `private_`/`executable_` 前缀自动设置权限（`0600`/`0755`） |
| 幂等 apply | 只修改有差异的文件，不会无故覆盖 |
| 脚本钩子 | `run_once_*.sh`、`run_onchange_*.sh`——首次或内容变化时自动执行 |
| 外部文件拉取 | `.chezmoiexternal.toml` 可从 URL / git repo / archive 拉取文件 |
| 路径编码 | source 目录用命名约定编码目标路径（`dot_` = `.`），仓库里不存在真正的隐藏文件 |

## 跨平台路径差异

同一类配置文件在不同平台路径可能完全不同，以 VS Code `settings.json` 为例：

| 平台 | 路径 |
| ---- | ---- |
| Linux | `~/.config/Code/User/settings.json` |
| macOS | `~/Library/Application Support/Code/User/settings.json` |
| Windows | `%APPDATA%\Code\User\settings.json` |

chezmoi 有两种常用方案：

### 方案一：`.chezmoiignore` 按平台过滤

source 里分别存各平台的路径，然后用模板语法按平台忽略不需要的文件：

```text
# ~/.local/share/chezmoi/.chezmoiignore
{{- if ne .chezmoi.os "linux" }}
.config/Code/User/settings.json
{{- end }}
{{- if ne .chezmoi.os "darwin" }}
Library/Application Support/Code/User/settings.json
{{- end }}
```

### 方案二：`run_once_` 脚本创建软链接（推荐）

source 只存一份文件（如 Linux 路径），其他平台用一次性脚本建立软链接：

```bash
# run_once_setup-vscode-macos.sh.tmpl
{{- if eq .chezmoi.os "darwin" -}}
#!/bin/bash
mkdir -p "$HOME/Library/Application Support/Code/User"
ln -sf "$HOME/.config/Code/User/settings.json" \
       "$HOME/Library/Application Support/Code/User/settings.json"
{{- end -}}
```

文件名前缀 `run_once_` 表示该脚本只在首次 `chezmoi apply` 时执行一次。如果脚本内容变化，则重新执行一次（使用 `run_onchange_` 前缀）。

## 参考

- 官网：<https://www.chezmoi.io>
- GitHub：<https://github.com/twpayne/chezmoi>

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | ---- | ---- |
| 2026-07-13 | 补充「日常改配置流程」（edit → apply → git push → 他机 update）；补充发音 shay-mwah /ʃeɪ mwɑ/；修正安装标题杂字符 | 流程原先分散；缺发音说明 |
